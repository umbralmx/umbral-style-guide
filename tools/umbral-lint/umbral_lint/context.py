"""Shared state: the rule set, the token values, and the file walk.

The linter never hard-codes a severity or a fix hint. Both come from
`rules/rules.json`, so a rule moving from `warning` to `error` changes the linter's
behaviour without touching the linter — which is the point of having a normative
layer at all.
"""
from __future__ import annotations

import fnmatch
import json
import pathlib
import re
from dataclasses import dataclass, field

# Where the normative layer might be, in order of preference:
#   1. an explicit --rules / --tokens path
#   2. the repo being linted, if it *is* the style guide
#   3. the copy bundled with the installed skill
#   4. the copy vendored next to this package
SEARCH = [
    ("rules/rules.json", "tokens/build/tokens.json"),
    (".claude/skills/umbral-brand/assets/rules.json",
     ".claude/skills/umbral-brand/assets/tokens.json"),
    ("skills/umbral-brand/assets/rules.json",
     "skills/umbral-brand/assets/tokens.json"),
]

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", ".tox",
    ".pytest_cache", ".ruff_cache", "dist", "build", "_site", ".quarto",
    ".next", "target", "vendor", "_inbox",
}

CSS_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".vue", ".svelte", ".jsx", ".tsx"}
CODE_EXT = {".py", ".r", ".js", ".mjs", ".cjs", ".ts", ".ipynb"}
TEXT_EXT = {".md", ".qmd", ".rmd", ".txt", ".yml", ".yaml", ".toml"}
ALL_EXT = CSS_EXT | MARKUP_EXT | CODE_EXT | TEXT_EXT


@dataclass
class Finding:
    check: str
    file: pathlib.Path
    line: int
    message: str
    rule: str = ""
    severity: str = "error"
    fix: str = ""

    def as_dict(self, root: pathlib.Path) -> dict:
        try:
            rel = self.file.relative_to(root)
        except ValueError:
            rel = self.file
        return {
            "rule": self.rule, "check": self.check, "severity": self.severity,
            "file": str(rel), "line": self.line,
            "message": self.message, "fix": self.fix,
        }


# Suppression. A style guide has to quote the things it forbids, so the tool that
# checks it needs a way to be told "this line is an example, not a violation".
#   # umbral-lint: ignore            — all checks
#   # umbral-lint: ignore[no-emoji]  — one check
#   # umbral-lint: ignore-file       — the whole file
#
# On its own line the comment covers the following BLOCK, up to the next blank
# line. Trailing on a line of content, it covers that line only. The block form is
# what makes a markdown table or a fenced example suppressible without a comment
# per row.
IGNORE_LINE = re.compile(r"umbral-lint:\s*ignore(?:\[([\w,\s-]+)\])?")
IGNORE_FILE = re.compile(r"umbral-lint:\s*ignore-file(?:\[([\w,\s-]+)\])?")


@dataclass
class Context:
    root: pathlib.Path
    rules: dict
    tokens: dict
    findings: list[Finding] = field(default_factory=list)
    ignore_globs: list[str] = field(default_factory=list)
    _by_check: dict = field(default_factory=dict)
    _suppress: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        for r in self.rules.get("rules", []):
            cid = r.get("check", {}).get("id")
            if cid:
                self._by_check[cid] = r
        self.ignore_globs.extend(self._read_ignore_file())

    def _read_ignore_file(self) -> list[str]:
        base = self.root if self.root.is_dir() else self.root.parent
        for candidate in (base, *base.parents):
            f = candidate / ".umbral-lintignore"
            if f.exists():
                return [ln.strip() for ln in f.read_text().splitlines()
                        if ln.strip() and not ln.strip().startswith("#")]
            if (candidate / ".git").exists():
                break
        return []

    def _ignored_path(self, path: pathlib.Path) -> bool:
        try:
            rel = path.relative_to(self.root if self.root.is_dir() else self.root.parent)
        except ValueError:
            rel = path
        s = rel.as_posix()
        return any(fnmatch.fnmatch(s, g) or s.startswith(g.rstrip("*").rstrip("/") + "/")
                   for g in self.ignore_globs)

    def suppressions(self, path: pathlib.Path) -> tuple[set, dict]:
        """(file-level ignores, {line: set-of-checks}). Empty set means "all"."""
        key = str(path)
        if key in self._suppress:
            return self._suppress[key]
        file_level: set = set()
        per_line: dict = {}
        pending: list = []
        whole_file = False
        try:
            for i, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
                mf = IGNORE_FILE.search(raw)
                if mf:
                    whole_file = True
                    if mf.group(1):
                        file_level |= {c.strip() for c in mf.group(1).split(",")}
                    continue
                m = IGNORE_LINE.search(raw)
                if m:
                    ids = {c.strip() for c in m.group(1).split(",")} if m.group(1) else set()
                    per_line[i] = ids
                    stripped = raw.strip()
                    standalone = stripped.startswith(("#", "//", "<!--", "/*", "*", "%"))
                    if standalone:
                        pending.append(ids)
                    else:
                        continue
                elif pending:
                    if raw.strip() == "":
                        pending.clear()
                    else:
                        for ids in pending:
                            per_line.setdefault(i, set())
                            if not ids:
                                per_line[i] = set()
                            else:
                                per_line[i] |= ids
        except OSError:
            pass
        out = ((file_level if file_level else {"*"}) if whole_file else set(), per_line)
        self._suppress[key] = out
        return out

    # ── rule lookup ───────────────────────────────────────────────────────
    def rule_for(self, check_id: str) -> dict | None:
        return self._by_check.get(check_id)

    def severity(self, check_id: str) -> str:
        r = self.rule_for(check_id)
        return r["severity"] if r else "error"

    def report(self, check_id: str, path: pathlib.Path, line: int,
               message: str, fix: str = "") -> None:
        if self._ignored_path(path):
            return
        if path.is_file():
            file_level, per_line = self.suppressions(path)
            if "*" in file_level or check_id in file_level:
                return
            ids = per_line.get(line)
            if ids is not None and (not ids or check_id in ids):
                return
        r = self.rule_for(check_id)
        self.findings.append(Finding(
            check=check_id, file=path, line=line, message=message,
            rule=r["id"] if r else "", severity=self.severity(check_id),
            fix=fix or (r["do"] if r else ""),
        ))

    # ── token helpers ─────────────────────────────────────────────────────
    @property
    def token_hex(self) -> dict[str, str]:
        """hex -> "name (mode)" for every semantic token value."""
        if not hasattr(self, "_hex"):
            out: dict[str, str] = {}
            for mode, vals in self.tokens.get("mode", {}).items():
                for name, v in vals.items():
                    if isinstance(v, str) and v.startswith("#"):
                        out.setdefault(v.lower(), f"{name} ({mode})")
            self._hex = out          # noqa: attribute defined outside __init__
        return self._hex

    @property
    def font_families(self) -> set[str]:
        f = self.tokens.get("font", {})
        return {str(f.get(k, "")).lower() for k in ("display", "body", "mono") if f.get(k)}

    # ── the walk ──────────────────────────────────────────────────────────
    def files(self, exts: set[str] | None = None):
        exts = exts or ALL_EXT
        if self.root.is_file():
            if self.root.suffix in exts and not self._ignored_path(self.root):
                yield self.root
            return
        for p in sorted(self.root.rglob("*")):
            if not p.is_file() or p.suffix not in exts:
                continue
            if any(part in SKIP_DIRS for part in p.relative_to(self.root).parts):
                continue
            if self._ignored_path(p):
                continue
            yield p


def load(root: pathlib.Path, rules_path: pathlib.Path | None,
         tokens_path: pathlib.Path | None) -> Context:
    """Find the normative layer, or explain clearly why we cannot."""
    if rules_path and tokens_path:
        return Context(root, json.loads(rules_path.read_text()),
                       json.loads(tokens_path.read_text()))

    here = pathlib.Path(__file__).resolve()
    bases = [root, root.parent, *here.parents[:5]]
    for base in bases:
        for rj, tj in SEARCH:
            rp, tp = base / rj, base / tj
            if rp.exists() and tp.exists():
                return Context(root, json.loads(rp.read_text()),
                               json.loads(tp.read_text()))

    raise SystemExit(
        "umbral-lint: cannot find rules.json and tokens.json.\n"
        "  Pass --rules and --tokens, or install the skill into .claude/skills/,\n"
        "  or fetch them:\n"
        "    https://raw.githubusercontent.com/umbralmx/umbral-style-guide/"
        "v1.1.0/rules/rules.json"
    )


# ── shared parsing helpers ────────────────────────────────────────────────
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def code_lines(text: str) -> list[tuple[int, str]]:
    """(line_no, code) with comments blanked, preserving line numbering.

    `//` is only a comment when it is not the `//` of a URL scheme, and `#` is only
    a comment when it is not a hex colour. Getting either wrong silently disables
    checks — the URL case hid the font-CDN check during development.
    """
    text = _BLOCK_COMMENT.sub(lambda m: "\n" * m.group().count("\n"), text)
    text = _HTML_COMMENT.sub(lambda m: "\n" * m.group().count("\n"), text)
    out = []
    for i, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"(?<!:)//.*$", "", raw)
        line = re.sub(r"(?<![:\w])#(?![0-9A-Fa-f]{3,8}\b).*$", "", line)
        out.append((i, line))
    return out


def declarations(line: str):
    """Yield (property, value) for CSS-ish declarations on a line."""
    for m in re.finditer(r"([-\w]+)\s*:\s*([^;{}\n]+)", line):
        yield m.group(1).strip().lower(), m.group(2).strip()


TOKEN_FILE = re.compile(
    r"(^|/)(tokens\.(css|json|py|R|scss|js|mjs)|_tokens\.scss|[\w.-]+\.tokens\.json"
    r"|contrast\.json|plotly-umbral-[\w-]+\.json|umbral-[\w-]+\.mplstyle"
    r"|altair-umbral\.py|streamlit-config\.toml|_brand\.yml)$")


def is_token_file(p: pathlib.Path) -> bool:
    """Token files are where values are supposed to live."""
    s = p.as_posix()
    return bool(TOKEN_FILE.search(s)) or "/tokens/" in s or s.startswith("tokens/")
