# `umbral-lint`

Conformance checker for Umbral repos. Python, no dependencies — it has to run wherever the notebooks
and dashboards already run.

```bash
pip install -e tools/umbral-lint
umbral-lint .                       # or: npm run lint
umbral-lint . --format github       # annotations in CI
umbral-lint --list-checks
```

## It implements 29 of the 45 checks the rules claim

The other 16 are `review` — human judgement — or belong to another tool. That split is enforced:
`tools/verify_lint.py` fails if a rule claims a check the linter doesn't implement, **or** if the
linter implements one no rule claims.

That reconciliation exists because at the end of Phase 2 `rules.yaml` claimed 48 automated checks
and zero were written. A rule promising a check nobody runs is worse than one honestly marked
`review`.

## Severities come from the rules, not from here

The linter reads `rules/rules.json` for every severity and fix hint. A rule moving from `warning` to
`error` changes what blocks a release without touching this code.

It finds the rules automatically — in the repo being linted, in an installed
`.claude/skills/umbral-brand/assets/`, or via `--rules` / `--tokens`.

## It parses, it does not grep

Measured against `cabildo-libre`, the most conformant product in the portfolio, naive substring
matching produced **eleven hits and all eleven were false**:

| Looks like | Actually |
|---|---|
| `Inter` | `cursor: pointer` |
| `white` | `white-space: nowrap` |
| `gradient` | a single-colour `linear-gradient` drawing a 1px rule |
| `box-shadow` | `inset 4px 0 0 var(--u-signal)` — a rule, not a shadow |

So the checks parse declarations, track balanced parens, and skip comments. Three bugs found while
building it are worth knowing about, because each silently disabled a check:

- `//` in a comment-stripper also matches the `//` in `https://` — which hid the font-CDN check.
- `[^)]*` inside `linear-gradient(var(--x), var(--x))` stops at the *inner* paren, making a
  one-colour gradient look like two stops.
- `TODO` matched case-insensitively hits «todo», the ordinary Spanish word for "all" — 40 false
  positives on Spanish prose.

## Suppression

A style guide has to quote what it forbids.

```html
<!-- umbral-lint: ignore[no-emoji] -->     covers the following block, to the next blank line
```
```python
x = "#128273"  # umbral-lint: ignore[hardcoded-value]   trailing: this line only
# umbral-lint: ignore-file[hardcoded-value]             the whole file
```

Path-level exclusions go in `.umbral-lintignore` at the repo root. Every entry in this repo's copy
carries a reason.

## Exit codes

`0` clean · `1` findings at or above `--max-severity` (default `error`) · `2` bad invocation.
