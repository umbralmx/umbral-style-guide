#!/usr/bin/env python3
"""Every folder in the repo explains what it is for.

A folder with no README is a folder whose purpose lives only in someone's head.
This keeps that from happening as later phases add packages/, skills/, site/ and
examples/.

Run: python3 tools/verify_readmes.py    (exit 1 on any failure)
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(".")

SKIP = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".pytest_cache", ".ruff_cache", "dist", ".quarto", "_site",
}

# Folders that only ever hold sibling files of one kind, where a README would be
# noise. Keep this list short and justified.
EXEMPT = {
    pathlib.Path(".github"),          # covered by .github/workflows/README.md
}

MIN_CHARS = 120

failures: list[str] = []
checked = 0


def interesting(p: pathlib.Path) -> bool:
    return not any(part in SKIP or part.startswith(".") and part != ".github"
                   for part in p.parts)


folders = sorted(
    d for d in ROOT.rglob("*")
    if d.is_dir() and interesting(d.relative_to(ROOT)) and d.name not in SKIP
)

for d in folders:
    rel = d.relative_to(ROOT)
    if rel in EXEMPT:
        continue
    # a folder with no files of its own and only subfolders still gets one
    checked += 1
    readme = d / "README.md"
    if not readme.exists():
        failures.append(f"{rel}/ has no README.md")
        continue
    text = readme.read_text().strip()
    if len(text) < MIN_CHARS:
        failures.append(f"{rel}/README.md is {len(text)} chars — say what the folder is for")
    if not text.startswith("#"):
        failures.append(f"{rel}/README.md does not start with a heading")

# the root README is the human entry point and has a higher bar
root_readme = ROOT / "README.md"
checked += 1
if not root_readme.exists():
    failures.append("README.md missing at the repo root")
else:
    t = root_readme.read_text()
    for want in ("guide/", "rules/", "tokens/", "CC BY 4.0", "MIT"):
        if want not in t:
            failures.append(f"root README.md does not mention {want}")

print(f"verify_readmes: {checked} folders checked, {len(failures)} failed")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("every folder documents itself")
