# `_inbox/`

The **v1.0 source material**, kept for reference. Nothing here is normative any more.

| | |
|---|---|
| `umbral brand book.pdf` | v1.0, July 2026. Text extracted to `audit/brandbook-v1.0.txt`. |
| `CLAUDE.md` | The old brand-level agent contract |
| `umbral-engineering.md` | The old implementation handoff |
| `tokens.json`, `tokens.css` | The v1.0 tokens |
| `umbral-{isotype,lockup}-{light,dark}.svg`, `umbral-favicon.svg` | The v1.0 logo files |

## Treat these as input, not gospel

The [Phase 0 audit](../audit/2026-07-conformance.md) §3.5 documents what's wrong with them:

- `umbral-engineering.md` §4 claims both modes meet WCAG AA. Four token pairs didn't.
- Its §1 asks for self-hosted fonts in prose and ships a Google Fonts link in the code block of the
  same section.
- Its `mplstyle` uses a 2.37:1 token for axis labels *and* as the third data series.
- The brand book's Streamlit page has mangled config keys (`sc-camel-primary-color`) and sets
  `font = "sans serif"`, which is why `pautamx` renders Source Sans today.
- The logo SVGs carry three different bar ratios and the lockup crosses on the wrong side.

The colour values were verified byte-identical to what the live products actually shipped, so
they're trustworthy as a record of v1.0 — it's the *documents* that disagreed with each other.

The corrected versions live in `tokens/`, `rules/` and `guide/`.
