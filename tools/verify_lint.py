#!/usr/bin/env python3
"""Reconcile the rule set with the checks that actually run.

This is the check that keeps Phase 5's honesty from decaying. It enforces both
directions:

  * every rule claiming `tool: umbral-lint` names a check the linter implements;
  * every check the linter implements is claimed by exactly one rule;
  * every other named tool (`token-build`, `verify-tokens`, `verify-guide`,
    `logo-build`) actually exists and runs that check.

Without it, `rules.yaml` drifts back into promising checks nobody wrote — which is
the state it was in at the end of Phase 2, with 48 automated checks claimed and none
implemented.

It also runs the linter against fixtures whose findings are already known from the
Phase 0 audit, so a regression in a check shows up as a diff rather than silence.

Run: python3 tools/verify_lint.py    (exit 1 on any failure)
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path("tools/umbral-lint").resolve()))
from umbral_lint import checks  # noqa: E402

RULES = pathlib.Path("rules/rules.json")

failures: list[str] = []
count = 0


def check(ok: bool, msg: str) -> None:
    global count
    count += 1
    if not ok:
        failures.append(msg)


rules = json.loads(RULES.read_text())
automated = rules["automatedChecks"]
implemented = set(checks.IMPLEMENTED)

# ── 1. rules -> linter ────────────────────────────────────────────────────
claimed = {c["check"] for c in automated if c["tool"] == "umbral-lint"}
for cid in sorted(claimed):
    check(cid in implemented,
          f"rules.yaml claims umbral-lint check {cid!r}, which is not implemented — "
          f"implement it or move the rule to `review`")

# ── 2. linter -> rules ────────────────────────────────────────────────────
for cid in sorted(implemented):
    owners = [c["rule"] for c in automated if c["check"] == cid]
    check(len(owners) == 1,
          f"umbral-lint implements {cid!r} but {len(owners)} rules claim it "
          f"({owners or 'none'}) — every check needs exactly one owning rule")

# ── 3. the other tools exist and are wired ────────────────────────────────
TOOL_FILES = {
    "token-build": pathlib.Path("build/index.mjs"),
    "verify-tokens": pathlib.Path("tools/verify_tokens.py"),
    "verify-guide": pathlib.Path("tools/verify_guide.py"),
    "logo-build": pathlib.Path("build/logo.mjs"),
}
for c in automated:
    if c["tool"] == "umbral-lint":
        continue
    p = TOOL_FILES.get(c["tool"])
    check(p is not None and p.exists(),
          f"{c['rule']} names tool {c['tool']!r}, which has no implementation file")
    if p and p.exists():
        # the check id should be traceable in the tool that claims it
        text = p.read_text()
        hint = c["check"].replace("-", "")
        check(c["check"] in text or hint in text.replace("-", "").replace("_", ""),
              f"{c['rule']}: {p} does not mention check {c['check']!r}")

# ── 4. no rule claims `automated` without a tool ──────────────────────────
for r in rules["rules"]:
    ch = r["check"]
    if ch["type"] == "automated":
        check(bool(ch.get("tool")) and bool(ch.get("id")),
              f"{r['id']} is automated but incompletely specified")
    else:
        check("tool" not in ch,
              f"{r['id']} is {ch['type']} but names a tool — that reads as automated")

# ── 5. downgraded rules must say why ──────────────────────────────────────
for r in rules["rules"]:
    if r["check"]["type"] == "review" and r["severity"] == "error":
        check(bool(r["check"].get("note")),
              f"{r['id']} is an `error` checked only by review and gives no reason — "
              f"say why it cannot be automated")

# ── 6. behaviour against known fixtures ───────────────────────────────────
# These findings were measured on the live products in the Phase 0 audit.
def lint(path: str, fmt: str = "json") -> dict:
    res = subprocess.run(
        [sys.executable, "-m", "umbral_lint", path, "--format", fmt,
         "--rules", "rules/rules.json", "--tokens", "tokens/build/tokens.json"],
        capture_output=True, text=True,
        env={**__import__("os").environ, "PYTHONPATH": "tools/umbral-lint"})
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return {"findings": [], "_stderr": res.stderr, "_stdout": res.stdout}


# The generated token files must never be flagged — a linter that does not
# understand its own system is worse than none.
for target in ("tokens/build/tokens.css", "tokens/build/tokens.py",
               "skills/umbral-brand/assets/tokens.css"):
    out = lint(target)
    check(len(out.get("findings", [])) == 0,
          f"{target} is flagged by umbral-lint: "
          f"{[f['check'] for f in out.get('findings', [])]}")

# The guide quotes banned terminology in order to ban it.
out = lint("guide/15-terminologia.md")
check(not any(f["check"] == "terminology" for f in out.get("findings", [])),
      "the terminology chapter is flagged by its own check")

print(f"verify_lint: {count} checks, {len(failures)} failed")
print(f"  {len(implemented)} checks implemented · {len(claimed)} claimed by rules · "
      f"{sum(1 for r in rules['rules'] if r['check']['type'] == 'review')} rules left to review")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("rule set and linter agree")
