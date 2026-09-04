#!/usr/bin/env python3
"""Verify the agent skill against the normative layer.

The v1.0 skill is the reason this check exists. It restated token values in prose
and bundled its own copies, so it kept handing out colours that failed contrast long
after the repo knew they were wrong — and nothing noticed, because nothing compared
the two.

Checks:
  * the pinned assets are byte-identical to what the build produced;
  * SKILL.md has valid frontmatter and a description pushy enough to trigger;
  * SKILL.md cites only rule IDs that exist;
  * every hex appearing in SKILL.md is a current token value;
  * the scripts run and agree with the normative contrast matrix;
  * dist/CLAUDE.snippet.md is pinned to a tag, not to main.

Run: python3 tools/verify_skill.py    (exit 1 on any failure)
"""
from __future__ import annotations

import filecmp
import json
import pathlib
import re
import subprocess
import sys

SKILL = pathlib.Path("skills/umbral-brand")
REF = SKILL / "references"
AST = SKILL / "assets"
SNIPPET = pathlib.Path("dist/CLAUDE.snippet.md")

failures: list[str] = []
checks = 0


def check(ok: bool, msg: str) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(msg)


if not SKILL.exists():
    sys.exit("skills/umbral-brand/ missing — run `npm run build:skill` first")

tokens = json.loads((AST / "tokens.json").read_text())
rules = json.loads((AST / "rules.json").read_text())
by_id = {r["id"] for r in rules["rules"]}
skill_md = (SKILL / "SKILL.md").read_text()

# ── 1. pinned assets match the build exactly ──────────────────────────────
PAIRS = [
    ("tokens/build/tokens.json", "tokens.json"),
    ("tokens/build/tokens.css", "tokens.css"),
    ("tokens/build/tokens.py", "tokens.py"),
    ("tokens/build/contrast.json", "contrast.json"),
    ("tokens/build/streamlit-config.toml", "streamlit-config.toml"),
    ("tokens/build/_brand.yml", "_brand.yml"),
    ("rules/rules.json", "rules.json"),
]
for src, dst in PAIRS:
    p, q = pathlib.Path(src), AST / dst
    check(q.exists(), f"skill asset {dst} missing")
    if q.exists():
        check(filecmp.cmp(p, q, shallow=False),
              f"skill asset {dst} differs from {src} — run `npm run build:skill`")

for svg in pathlib.Path("assets/logo").glob("*.svg"):
    q = AST / svg.name
    check(q.exists() and filecmp.cmp(svg, q, shallow=False),
          f"skill logo {svg.name} differs from assets/logo/")

# ── 2. frontmatter ────────────────────────────────────────────────────────
m = re.match(r"^---\n(.*?)\n---\n", skill_md, re.S)
check(m is not None, "SKILL.md has no YAML frontmatter")
if m:
    fm = m.group(1)
    check(re.search(r"^name:\s*umbral-brand\s*$", fm, re.M) is not None,
          "SKILL.md frontmatter name is not `umbral-brand`")
    dm = re.search(r"^description:\s*(.+)$", fm, re.M | re.S)
    check(dm is not None, "SKILL.md frontmatter has no description")
    if dm:
        desc = dm.group(1)
        # it must trigger on the product names, not just the word "brand"
        for word in ["umbral", "desaparecidosmx", "pautamx", "cabildo-libre",
                     "Streamlit", "Quarto", "laboratorio", "instrumento"]:
            check(word.lower() in desc.lower(),
                  f"SKILL.md description does not mention {word!r} — it will under-trigger")
        check(len(desc) > 400, "SKILL.md description is too terse to trigger reliably")

# ── 3. body length — progressive disclosure, not a dump ───────────────────
body_lines = len(skill_md.splitlines())
check(body_lines < 500, f"SKILL.md is {body_lines} lines; keep it under 500 (KICKOFF §6)")

# ── 4. every rule ID cited exists ─────────────────────────────────────────
for text, where in [(skill_md, "SKILL.md")] + [
        (p.read_text(), f"references/{p.name}") for p in REF.glob("*.md")]:
    for rid in set(re.findall(r"\bUMB-[A-Z0-9]+-\d{3}\b", text)):
        check(rid in by_id, f"{where} cites {rid}, which is not a rule")

# ── 5. every hex in the skill is a current token value ────────────────────
live = {v.lower() for mode in tokens["mode"].values()
        for v in mode.values() if isinstance(v, str) and v.startswith("#")}
live |= {v.lower() for mode in tokens["ramp"].values()
         for ramp in mode.values() for v in ramp}
for text, where in [(skill_md, "SKILL.md"), (SNIPPET.read_text(), "CLAUDE.snippet.md")]:
    for hexv in set(re.findall(r"#[0-9a-fA-F]{6}\b", text)):
        check(hexv.lower() in live,
              f"{where} contains {hexv}, which is not a current token value")

# ── 6. the scripts work and agree with the normative matrix ───────────────
res = subprocess.run(
    [sys.executable, "scripts/check_contrast.py", "--audit"],
    cwd=SKILL, capture_output=True, text=True)
check(res.returncode == 0, f"check_contrast.py --audit exited {res.returncode}")
report = json.loads((AST / "contrast.json").read_text())
check(f"{report['summary']['pairsChecked']} pairs checked" in res.stdout,
      "check_contrast.py --audit disagrees with contrast.json")

res = subprocess.run(
    [sys.executable, "scripts/lint.py", "assets/tokens.css"],
    cwd=SKILL, capture_output=True, text=True)
check(res.returncode == 0 and "clean" in res.stdout,
      "lint.py flags the token file it ships — it should understand its own system")

res = subprocess.run(
    [sys.executable, "scripts/apply_theme.py", "--colors"],
    cwd=SKILL, capture_output=True, text=True)
check(res.returncode == 0, "apply_theme.py --colors failed")
check(tokens["mode"]["laboratorio"]["signal"] in res.stdout,
      "apply_theme.py --colors does not report the signal token")

# ── 7. the snippet is pinned ──────────────────────────────────────────────
snip = SNIPPET.read_text()
check(f"v{rules['version']}" in snip,
      f"CLAUDE.snippet.md is not pinned to v{rules['version']}")
check("/main/" not in snip and "@main" not in snip,
      "CLAUDE.snippet.md points at main — a token change would land unannounced")
check(len(snip.splitlines()) < 80, "CLAUDE.snippet.md is longer than a snippet should be")

# ── 8. references are all present and generated ───────────────────────────
for name in ["color", "charts", "voice-and-numbers", "surfaces", "components",
             "terminology", "checklist"]:
    p = REF / f"{name}.md"
    check(p.exists(), f"references/{name}.md missing (KICKOFF §6)")
    if p.exists():
        check("GENERATED" in p.read_text()[:400],
              f"references/{name}.md has no generated-file header")

print(f"verify_skill: {checks} checks, {len(failures)} failed")
print(f"  SKILL.md {body_lines} lines · {len(list(REF.glob('*.md'))) - 1} references · "
      f"{len(list(AST.iterdir())) - 1} pinned assets · snippet pinned to v{rules['version']}")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("all skill checks pass")
