# `guide/_includes/`

**Everything in this folder except this README is generated. Do not edit the partials.**

A chapter includes a partial instead of transcribing a value or a rule. That is what stops the
guide stating a colour, a ratio or a rule the normative layer does not.

| | Generated from | By |
|---|---|---|
| `rules/UMB-*.md` | `rules/rules.yaml` | `build/rules.mjs` |
| `token-table.md` | `tokens/build/tokens.json` | `build/guide.mjs` |
| `contrast-matrix.md` | `tokens/build/contrast.json` | `build/guide.mjs` |
| `series-palette.md` | both of the above | `build/guide.mjs` |
| `type-scale.md` | `tokens/build/tokens.json` | `build/guide.mjs` |
| `rule-index.md` | `rules/rules.json` | `build/rules.mjs` |

Rebuild with `npm run build`.

`tools/verify_guide.py` checks two things. Every partial here is used by at least one chapter. And
every include in a chapter resolves to a file that exists.
