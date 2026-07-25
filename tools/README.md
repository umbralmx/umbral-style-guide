# `tools/`

Independent verification. Python, run via `npm run verify`.

| | Checks |
|---|---|
| `verify_tokens.py` | Re-derives every contrast ratio, ramp monotonicity, that the Phase 0 failures are actually fixed, and that no hex is authored twice |
| `verify_rules.py` | Re-validates `rules.yaml` with a different schema validator, that the generated artifacts match the source, and that every topic in KICKOFF §5 is covered |
| `verify_guide.py` | That every rule naming a chapter is included by it, and that no chapter restates a rule's text instead of including its callout |
| `verify_readmes.py` | That every folder has a README explaining what it's for |

These deliberately re-implement what `build/` already did, in a different language. The point is
that a mistake has to be made twice to reach the published system — the defect that motivated this
repo was an accessibility claim nothing ever checked.

`umbral-lint`, the CLI that checks *other* repos, arrives in Phase 5. These scripts check this one.

```bash
npm run verify        # all four
```
