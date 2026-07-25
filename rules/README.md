# `rules/` — the normative layer

`rules.yaml` is the only place a rule is authored. `rules.json`, `guide/CHECKLIST.md` and
`guide/_includes/rules/*.md` are generated from it by `npm run build:rules` and must never be
edited by hand (UMB-PRO-001).

The point of this layer is **UMB-PRO-002**: prose never states a rule `rules.yaml` does not also
state. Guide chapters include the generated callout rather than restating the rule in their own
words, so a chapter cannot drift from the norm — which is exactly what happened in v1.0, where the
brand book and `umbral-engineering.md` disagreed about the third series colour and the version that
failed contrast is the one that won in the Python tooling.

## What is here

| File | |
|---|---|
| `rules.yaml` | **NORMATIVE.** Every rule, with a stable ID. |
| `rules.schema.json` | JSON Schema (draft 2020-12). Shape only. |
| `rules.json` | Generated. What `umbral-lint`, the skill and CI read. |

## Adding a rule

1. Append it to `rules.yaml`. Take the next free number in its category — **IDs are never reused
   and never renumbered**, because prose, CI output and past PR reviews all cite them.
2. Write the `rationale`. If you cannot say *why*, it is a preference, not a rule, and it does not
   belong here.
3. Pick a `severity` honestly. `error` blocks a release, so a rule nobody will actually enforce
   should ship at `warning`.
4. Pick a `check.type`:
   - `automated` — a tool decides. Requires `tool` and a unique `check.id`. The check has to
     actually exist, or be planned in Phase 5.
   - `manual` — a human follows a stated procedure. Say what it is in `check.note`.
   - `review` — judgement, cited in PR review.
5. Add `evidence` if the rule is new since 1.0. The build **fails** without it — a rule that
   appeared from nowhere is a rule nobody can argue with later.
6. `npm run build:rules && python3 tools/verify_rules.py`
7. Commit `rules.yaml` **and** the generated output together, along with the guide chapter
   (UMB-PRO-005).

## What the build enforces beyond the schema

- IDs are unique, and the prefix matches the category (`UMB-COL-*` must be `category: color`).
- `check.id` values are unique across the whole set — two rules cannot claim the same check.
- Every `see_also` resolves to a rule that exists.
- Every rule newer than 1.0 records its `evidence`.
- An `automated` check names a tool that is actually shipped.

`tools/verify_rules.py` re-checks all of this in Python with a different schema validator, and
additionally verifies that the generated artifacts match the source and that every topic in the
minimum rule list of `KICKOFF-PROMPT.md` §5 is covered.

## Severity and semver

Per `CLAUDE.md` §4 and UMB-PRO-004:

| Change | Bump |
|---|---|
| A rule moves to `error`, or a token value changes | **major** |
| A new rule at `warning`, a new ramp, a new surface chapter | **minor** |
| Prose and example fixes | **patch** |

## A note on the `process` category

KICKOFF §5 lists ten categories; `process` is an eleventh, added in 1.1. It holds rules about how
the system is built rather than about what it produces (`UMB-PRO-001` … `UMB-PRO-005`).

It exists because the most consequential defects found in the Phase 0 audit were not design
mistakes. They were process failures — a value stated in two places that stopped agreeing, and a
claim about accessibility that nothing checked. Those failures needed IDs so they could be cited
and enforced like any other rule.
