# `audit/`

Conformance audits of the live Umbral products, and the decisions they forced.

| | |
|---|---|
| `2026-07-conformance.md` | The Phase 0 audit. Why this repo exists. |
| `open-questions.md` | Nine decisions, with evidence. Eight decided, one open. |
| `brandbook-v1.0.txt` | Extracted text of the v1.0 brand book, so Phase 3 could migrate the Spanish verbatim |
| `scripts/` | The measurement scripts, so every number is reproducible |

## What the July 2026 audit found

Measured live in a browser, not read from source: **44% of visible text on the main site failed WCAG
AA**, and the two dashboards painted 10 and 17 elements in `signal` against a rule that allows one.

The important finding wasn't the count. It was that almost nothing was sloppiness — the defects
traced back to specific lines in the v1.0 documents that had been followed correctly. That's the
argument for generating prose and code from one normative layer instead of maintaining both.

## `open-questions.md`

Per `CLAUDE.md` §4: where a v1.0 rule looks wrong, it gets recorded here with evidence rather than
quietly changed. If a rule is right but inconvenient, the rule wins.

**OQ-009 is still open** — measured against dichromacy simulation, v1.0's "vary hue only" rule can't
produce five separable categorical colours. Phase 1 shipped the lightness-varying version and logged
the reasoning so it's cheap to reverse.
