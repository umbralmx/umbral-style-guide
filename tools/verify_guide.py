#!/usr/bin/env python3
"""Verify the guide against the normative layer.

This is what makes UMB-PRO-002 — "prose never states a rule rules.yaml does not
also state" — mechanical rather than aspirational:

  * every rule that names a chapter is actually included by that chapter;
  * every rule referenced by a chapter exists;
  * chapters include the generated callout instead of restating the rule;
  * every generated partial a chapter includes actually exists.

Run: python3 tools/verify_guide.py    (exit 1 on any failure)
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

GUIDE = pathlib.Path("guide")
RULES = pathlib.Path("rules/rules.json")

failures: list[str] = []
checks = 0


def check(ok: bool, msg: str) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(msg)


if not RULES.exists():
    sys.exit("rules/rules.json missing — run `npm run build:rules` first")

rules = json.loads(RULES.read_text())["rules"]
by_id = {r["id"]: r for r in rules}

# READMEs describe folders; they are not guide chapters and carry no front matter.
chapters = sorted(p for p in GUIDE.rglob("*.md")
                  if "_includes" not in p.parts
                  and p.name not in {"CHECKLIST.md", "README.md"})
check(len(chapters) > 0, "no guide chapters found")

INCLUDE = re.compile(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}")
RULE_REF = re.compile(r"\bUMB-[A-Z0-9]+-\d{3}\b")

text_of = {p: p.read_text() for p in chapters}
includes_of = {p: set(INCLUDE.findall(t)) for p, t in text_of.items()}

# ── 1. every include resolves to a file that exists ───────────────────────
for p, incs in includes_of.items():
    for inc in incs:
        target = GUIDE / inc
        check(target.exists(), f"{p}: includes {inc}, which does not exist")

# ── 2. every rule naming a chapter is included by that chapter ────────────
# `guide: "02-color"` must resolve to guide/02-color.md or guide/<dir>/<name>.md
def chapter_path(slug: str) -> pathlib.Path | None:
    direct = GUIDE / f"{slug}.md"
    if direct.exists():
        return direct
    hits = [p for p in chapters if p.stem == slug.split("/")[-1]]
    return hits[0] if len(hits) == 1 else None


for r in rules:
    slug = r.get("guide")
    if not slug:
        continue
    p = chapter_path(slug)
    check(p is not None, f"{r['id']} names chapter '{slug}', which has no file")
    if p is None:
        continue
    want = f"_includes/rules/{r['id']}.md"
    check(want in includes_of[p],
          f"{r['id']} names chapter '{slug}' but {p.name} does not include its callout")

# ── 3. every rule ID mentioned in prose exists ────────────────────────────
for p, t in text_of.items():
    for rid in set(RULE_REF.findall(t)):
        check(rid in by_id, f"{p}: mentions {rid}, which is not a rule")

# ── 4. chapters must not restate a rule's normative text ──────────────────
# If a chapter contains a rule's exact title as prose without including the
# callout, the two can drift — which is the failure this repo exists to remove.
for p, t in text_of.items():
    body = INCLUDE.sub("", t)
    for r in rules:
        if r["title"] in body:
            check(f"_includes/rules/{r['id']}.md" in includes_of[p],
                  f"{p.name} states the text of {r['id']} without including its callout")

# ── 5. front matter and language ──────────────────────────────────────────
for p, t in text_of.items():
    check(t.startswith("---\n"), f"{p.name} has no YAML front matter")
    check("lang: es" in t.split("---")[1] if t.startswith("---\n") else False,
          f"{p.name} does not declare lang: es")

# ── 6. every chapter promised by the kickoff structure exists ─────────────
EXPECTED = [
    "00-principios", "01-marca", "02-color", "03-tipografia", "04-layout",
    "05-voz", "06-numeros", "07-vocabulario-visual", "08-anatomia-grafica",
    "09-incertidumbre", "10-mapas", "11-accesibilidad", "12-datos-procedencia",
    "13-interpretabilidad", "15-terminologia",
]
SURFACES = ["web", "streamlit", "quarto", "notebook", "social", "slides", "github", "email"]
stems = {p.stem for p in chapters}
for name in EXPECTED:
    check(name in stems, f"KICKOFF §4 expects guide/{name}.md — missing")
for name in SURFACES:
    check((GUIDE / "14-superficies" / f"{name}.md").exists(),
          f"KICKOFF §4 expects guide/14-superficies/{name}.md — missing")

# ── 7. every generated partial is used by at least one chapter ────────────
used = {inc for incs in includes_of.values() for inc in incs}
for partial in (GUIDE / "_includes").glob("*.md"):
    if partial.name == "README.md":
        continue
    rel = f"_includes/{partial.name}"
    check(rel in used, f"{rel} is generated but no chapter includes it")

# ── report ────────────────────────────────────────────────────────────────
covered = sum(1 for r in rules if r.get("guide"))
included = len({inc for incs in includes_of.values() for inc in incs if "rules/" in inc})
print(f"verify_guide: {checks} checks, {len(failures)} failed")
print(f"  {len(chapters)} chapters · {included}/{len(rules)} rule callouts included · "
      f"{covered} rules name a chapter")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("all guide checks pass")
