# `umbral_lint/`

The package.

| | |
|---|---|
| `cli.py` | Argument parsing, the run, the exit code |
| `context.py` | Rule lookup, token values, the file walk, suppression |
| `report.py` | Human, JSON and GitHub Actions output |
| `checks/` | The checks themselves |

## `context.py` is where the interesting decisions live

**Severity is never hard-coded.** `Context.report()` looks the check id up in `rules/rules.json` and
takes the severity and fix hint from there, so the normative layer stays in charge.

**Comment stripping is deliberately fussy.** `//` is only a comment when it isn't the `//` of a URL
scheme, and `#` is only a comment when it isn't a hex colour. Getting either wrong doesn't produce
noise — it silently *disables* checks, which is worse.

**Suppression has two scopes.** A trailing `umbral-lint: ignore` covers its line; one on its own
line covers the block up to the next blank line, which is what makes a markdown table or a fenced
example suppressible without a comment per row.
