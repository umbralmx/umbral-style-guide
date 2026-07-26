# `.github/workflows/`

| | |
|---|---|
| `build.yml` | Builds tokens, rules, logos, guide partials and the skill; runs the contrast and logo gates; verifies independently in Python; fails if committed output is stale |
| `lint.yml` | Runs `umbral-lint` over the repo with GitHub annotations, plus a worked example of how a downstream repo consumes it |

## What can fail the build

1. **The contrast gate** — a token missing the threshold for its declared role (text 4.5:1, marks
   3:1; furniture exempt by explicit declaration).
2. **Rule validation** — a duplicate ID, a dangling `see_also`, an ID prefix contradicting its
   category, or a rule newer than 1.0 with no `evidence`.
3. **Independent verification** — the Python re-derivation disagreeing with the JS build.
4. **Stale output** — `tokens/build/`, `rules/rules.json`, `guide/CHECKLIST.md` or
   `guide/_includes/` differing after a rebuild. That means someone hand-edited a generated file
   (UMB-PRO-001) or forgot to rebuild.

Later phases add workflows for Pages deployment and releases.
