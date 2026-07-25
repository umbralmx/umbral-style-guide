# `guide/_includes/`

**Generated. Do not edit.** Chapters include these instead of transcribing values or rules, so the
guide cannot state a colour, a ratio or a rule that the normative layer doesn't.

| | Generated from | By |
|---|---|---|
| `rules/UMB-*.md` | `rules/rules.yaml` | `build/rules.mjs` |
| `token-table.md` | `tokens/build/tokens.json` | `build/guide.mjs` |
| `contrast-matrix.md` | `tokens/build/contrast.json` | `build/guide.mjs` |
| `series-palette.md` | both of the above | `build/guide.mjs` |
| `type-scale.md` | `tokens/build/tokens.json` | `build/guide.mjs` |
| `rule-index.md` | `rules/rules.json` | `build/rules.mjs` |

Rebuild with `npm run build`. `tools/verify_guide.py` checks that every partial here is used by at
least one chapter, and that every include in a chapter resolves to a file that exists.
