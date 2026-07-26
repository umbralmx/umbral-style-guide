"""Output formats: human, JSON, and GitHub Actions annotations."""
from __future__ import annotations

import json
import pathlib

from .context import Finding

ORDER = {"error": 0, "warning": 1, "info": 2}
MARK = {"error": "■", "warning": "▲", "info": "·"}


def _sorted(findings: list[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda f: (ORDER.get(f.severity, 3), str(f.file), f.line))


def human(findings: list[Finding], root: pathlib.Path, checked: int) -> str:
    if not findings:
        return (f"umbral-lint: {checked} files checked, clean\n")

    out: list[str] = []
    current = None
    for f in _sorted(findings):
        try:
            rel = f.file.relative_to(root)
        except ValueError:
            rel = f.file
        if str(rel) != current:
            current = str(rel)
            out.append(f"\n{current}")
        out.append(f"  {MARK.get(f.severity, '?')} {f.line:>5}  "
                   f"{f.rule or f.check:<14} {f.message}")
        if f.fix:
            out.append(f"           {'':14} → {f.fix}")

    counts = {s: sum(1 for f in findings if f.severity == s)
              for s in ("error", "warning", "info")}
    out.append("")
    out.append(f"umbral-lint: {checked} files checked · "
               f"{counts['error']} error · {counts['warning']} warning · {counts['info']} info")
    if counts["error"]:
        out.append("Errors block the release. See rules/rules.yaml for the rule text.")
    return "\n".join(out) + "\n"


def as_json(findings: list[Finding], root: pathlib.Path, checked: int) -> str:
    counts = {s: sum(1 for f in findings if f.severity == s)
              for s in ("error", "warning", "info")}
    return json.dumps({
        "tool": "umbral-lint",
        "filesChecked": checked,
        "counts": counts,
        "findings": [f.as_dict(root) for f in _sorted(findings)],
    }, indent=2, ensure_ascii=False) + "\n"


def github(findings: list[Finding], root: pathlib.Path, checked: int) -> str:
    level = {"error": "error", "warning": "warning", "info": "notice"}
    lines = []
    for f in _sorted(findings):
        try:
            rel = f.file.relative_to(root)
        except ValueError:
            rel = f.file
        msg = f"{f.rule or f.check}: {f.message}"
        if f.fix:
            msg += f" — {f.fix}"
        msg = msg.replace("\n", " ").replace("%", "%25").replace("\r", "")
        lines.append(f"::{level.get(f.severity, 'error')} "
                     f"file={rel},line={f.line},title=umbral-lint::{msg}")
    counts = sum(1 for f in findings if f.severity == "error")
    lines.append(f"::notice title=umbral-lint::{checked} files checked, {counts} error(s)")
    return "\n".join(lines) + "\n"


FORMATS = {"human": human, "json": as_json, "github": github}
