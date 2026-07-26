#!/usr/bin/env python3
"""Independently verify the Umbral rule set.

`build/rules.mjs` validates and generates in JavaScript. This re-parses the YAML in
Python, re-validates against the schema with a different validator, and checks that
the generated artifacts actually agree with the source — the same two-implementation
discipline used for the tokens.

It also checks coverage against the minimum rule list in KICKOFF-PROMPT.md §5, so a
rule cannot quietly go missing between the plan and the normative layer.

Run: python3 tools/verify_rules.py    (exit 1 on any failure)
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml
from jsonschema import Draft202012Validator

SRC = pathlib.Path("rules/rules.yaml")
SCHEMA = pathlib.Path("rules/rules.schema.json")
BUILT = pathlib.Path("rules/rules.json")
CHECKLIST = pathlib.Path("guide/CHECKLIST.md")
INCLUDES = pathlib.Path("guide/_includes/rules")

failures: list[str] = []
checks = 0


def check(ok: bool, msg: str) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(msg)


if not BUILT.exists():
    sys.exit("rules/rules.json missing — run `npm run build:rules` first")

doc = yaml.safe_load(SRC.read_text())
schema = json.loads(SCHEMA.read_text())
built = json.loads(BUILT.read_text())
rules = doc["rules"]
by_id = {r["id"]: r for r in rules}

# ── 1. schema, via a different validator than the build uses ──────────────
for err in Draft202012Validator(schema).iter_errors(doc):
    check(False, f"schema {'/'.join(map(str, err.absolute_path)) or '/'}: {err.message}")
check(True, "schema validated")

# ── 2. the generated JSON actually matches the source ─────────────────────
check(built["version"] == doc["version"],
      f"rules.json version {built['version']} != rules.yaml {doc['version']}")
check(len(built["rules"]) == len(rules),
      f"rules.json has {len(built['rules'])} rules, rules.yaml has {len(rules)}")
check([r["id"] for r in built["rules"]] == [r["id"] for r in rules],
      "rules.json rule order/ids differ from rules.yaml")
check(built["counts"]["total"] == len(rules), "rules.json total count is wrong")

sev_counts: dict[str, int] = {"error": 0, "warning": 0, "info": 0}
for r in rules:
    sev_counts[r["severity"]] += 1
check(built["counts"]["bySeverity"] == sev_counts,
      f"rules.json severity counts {built['counts']['bySeverity']} != {sev_counts}")

# ── 3. invariants ─────────────────────────────────────────────────────────
ids = [r["id"] for r in rules]
check(len(ids) == len(set(ids)), "duplicate rule ids")

check_ids = [r["check"]["id"] for r in rules if r["check"].get("id")]
check(len(check_ids) == len(set(check_ids)), "duplicate check ids")

PREFIX = {
    "brand": "BRD", "color": "COL", "type": "TYP", "layout": "LAY", "chart": "CHT",
    "voice": "VOZ", "numbers": "NUM", "data": "DAT", "a11y": "A11Y", "method": "MET",
    "process": "PRO",
}
for r in rules:
    check(r["id"].startswith(f"UMB-{PREFIX[r['category']]}-"),
          f"{r['id']} does not match its category {r['category']}")
    check(r["category"] in doc["categories"], f"{r['id']} category has no label")
    for ref in r.get("see_also", []):
        check(ref in by_id, f"{r['id']} references missing rule {ref}")
    if r["check"]["type"] == "automated":
        check(bool(r["check"].get("tool")), f"{r['id']} automated with no tool")
        check(bool(r["check"].get("id")), f"{r['id']} automated with no check id")
    # Spanish title and English mirror must both be real, and must differ
    check(r["title"] != r["title_en"], f"{r['id']} title_en is identical to title")

# ── 4. every rule has a generated callout, and no callout is orphaned ─────
# README.md in this folder is generated documentation, not a rule callout
callouts = ({p.stem for p in INCLUDES.glob("*.md")} - {"README"}) if INCLUDES.exists() else set()
check(callouts == set(ids),
      f"callouts differ from rules: missing {sorted(set(ids) - callouts)}, "
      f"orphaned {sorted(callouts - set(ids))}")
for r in rules:
    p = INCLUDES / f"{r['id']}.md"
    if p.exists():
        text = p.read_text()
        check("GENERATED from rules/rules.yaml" in text, f"{r['id']} callout has no header")
        check(r["title"] in text, f"{r['id']} callout does not contain its title")

# ── 5. the checklist carries exactly the human-judgement error rules ──────
human = sorted(r["id"] for r in rules
               if r["severity"] == "error" and r["check"]["type"] != "automated")
listed = sorted(line.split("**")[1] for line in CHECKLIST.read_text().splitlines()
                if line.startswith("- [ ] **"))
check(listed == human,
      f"CHECKLIST.md lists {len(listed)} rules, expected the {len(human)} "
      f"non-automated error rules; diff {set(listed) ^ set(human)}")

# ── 6. coverage of the minimum rule list in KICKOFF-PROMPT.md §5 ──────────
# Each entry: a description from the kickoff, and the rule(s) that must cover it.
KICKOFF_MINIMUM = {
    "color token usage": ["UMB-COL-002"],
    "the signal rule": ["UMB-COL-004"],
    "no pure black/white": ["UMB-COL-001"],
    "no gradients": ["UMB-COL-003"],
    "display type weight 500 never 700": ["UMB-TYP-001"],
    "approved font stack only": ["UMB-TYP-002"],
    "radius <= 2px": ["UMB-LAY-001"],
    "no shadows": ["UMB-LAY-002"],
    "measure <= 65ch": ["UMB-LAY-003"],
    "chart finding-title": ["UMB-CHT-001"],
    "chart subtitle": ["UMB-CHT-002"],
    "chart source + license": ["UMB-CHT-003", "UMB-DAT-004"],
    "horizontal gridlines only": ["UMB-CHT-004"],
    "no pie/3D/dual-axis": ["UMB-CHT-010"],
    "no truncated axis without note": ["UMB-CHT-009"],
    "<= 5 series": ["UMB-CHT-006"],
    "direct labels not legend boxes": ["UMB-CHT-005"],
    "uncertainty on projections/estimates": ["UMB-CHT-011"],
    "y-axis from zero for bars": ["UMB-CHT-008"],
    "causal verbs need identification strategy": ["UMB-MET-001"],
    "every dataset has SOURCE.md": ["UMB-DAT-001"],
    "every chart ships its CSV": ["UMB-A11Y-004"],
    "lang set": ["UMB-A11Y-001"],
    "non-color encoding present": ["UMB-A11Y-005"],
    "AA contrast": ["UMB-COL-005"],
    "Spanish first": ["UMB-VOZ-001"],
}
for topic, required in KICKOFF_MINIMUM.items():
    for rid in required:
        check(rid in by_id, f"KICKOFF §5 requires a rule for '{topic}' — {rid} is missing")

# ── 7. every automated check is claimed by exactly one tool we ship ───────
# Kept in step with rules.schema.json. tools/verify_lint.py additionally checks
# that each named tool has an implementation file that mentions the check id.
TOOLS = {"umbral-lint", "token-build", "verify-tokens", "verify-guide", "logo-build"}
for r in rules:
    if r["check"]["type"] == "automated":
        check(r["check"]["tool"] in TOOLS,
              f"{r['id']} names unknown tool {r['check']['tool']!r}")

# ── report ────────────────────────────────────────────────────────────────
auto = sum(1 for r in rules if r["check"]["type"] == "automated")
print(f"verify_rules: {checks} checks, {len(failures)} failed")
print(f"  {len(rules)} rules · {sev_counts['error']} error / {sev_counts['warning']} warning / "
      f"{sev_counts['info']} info · {auto} automated · "
      f"{len(KICKOFF_MINIMUM)} kickoff topics covered")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("all rule checks pass")
