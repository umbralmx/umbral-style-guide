# `umbral_lint/checks/`

| | Covers |
|---|---|
| `style.py` | Colour, type, layout — CSS and markup |
| `content.py` | Markup accessibility, charts, prose, terminology |
| `repo.py` | `SOURCE.md`, licences, hand-edited generated files |
| `__init__.py` | `IMPLEMENTED` — the registry, and the contract with `rules.yaml` |

## `IMPLEMENTED` is a contract

Every key must be claimed by exactly one rule, and every rule claiming
`tool: umbral-lint` must appear as a key. `tools/verify_lint.py` checks both directions and fails
CI otherwise.

Adding a check means: implement it, add it to `IMPLEMENTED` with a one-line description, and move
its rule in `rules/rules.yaml` from `review` to `automated`.

## The one that matters most

`content.py`'s `terminology` check reads the «Nunca» column of `guide/15-terminologia.md` — «levantón»,
«ajuste de cuentas», «sicario», «ejecutado». Umbral publishes on disappearances, and those words
attribute motive and guilt without evidence. It is the one prose check worth automating rather than
leaving to review.
