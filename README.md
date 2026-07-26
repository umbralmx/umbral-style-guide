# umbral-style-guide

The design system and editorial style guide for **Umbral** (`umbral_`) — an independent,
Spanish-first, open-source data lab publishing on disappearances, crime and public spending in
Mexico.

This repo is the single source of truth for three different consumers:

| You are… | Read |
|---|---|
| A human — designer, writer, contributor | [`guide/`](guide/) — the style guide, Spanish first |
| A machine — build tool, CI, linter | [`tokens/build/`](tokens/build/), [`rules/rules.json`](rules/) |
| An agent — Claude Code in another repo | [`skills/umbral-brand/`](skills/umbral-brand/) |

Content is **CC BY 4.0**, code is **MIT**.

## The one idea

A value or a rule is authored in exactly one place, and everything else is generated from it.

```
rules/rules.yaml  +  tokens/src/*.tokens.json      ← the only place a decision is made
        ↓ build
tokens/build/*  ·  rules/rules.json                ← generated, committed, never hand-edited
        ↓ consumed by
guide/  ·  site/  ·  packages/  ·  skills/  ·  tools/umbral-lint
```

This exists because of what the [July 2026 audit](audit/2026-07-conformance.md) found. Umbral's v1.0
brand was good and was applied carefully — and **44% of the text on the main site still failed
WCAG AA**. Almost none of it was sloppiness. The defects were instructions being followed correctly:

- The engineering doc asked for self-hosted fonts in prose and shipped a Google Fonts `<link>` in
  the code block of the same section. The site copied the code block.
- The brand book and the engineering doc disagreed about the third series colour, and the version
  that failed contrast is the one that won in the Python tooling.
- The docs claimed both modes met WCAG AA. Four token pairs did not, and nothing checked.

So the fix is structural: state a value once, generate the rest, and fail the build when a token
stops meeting its accessibility obligation.

## Quick start

```bash
npm install
npm run build      # tokens, rules, logos, guide partials, the agent skill
npm run verify     # re-derives everything independently in Python
npm run lint       # umbral-lint over this repo
```

The build **fails** if any token misses the contrast threshold for its declared role.

## Using it in another repo

Pin a version. Never point at `main` — a token change would land without warning.

```bash
curl -O https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.1.0/tokens/build/tokens.css
```

Available build targets: `tokens.css` · `tokens.json` · `_tokens.scss` · `tokens.py` · `tokens.R` ·
`umbral-{laboratorio,instrumento}.mplstyle` · `plotly-umbral-*.json` · `altair-umbral.py` ·
`streamlit-config.toml` · `_brand.yml` (Quarto) · `contrast.json`.

## What's in here

| Folder | |
|---|---|
| [`guide/`](guide/) | The style guide itself. Spanish. 15 chapters + 8 surface guides. |
| [`rules/`](rules/) | `rules.yaml` — 69 rules with stable IDs. The normative layer. |
| [`tokens/`](tokens/) | `src/` is authored; `build/` is generated for 11 targets. |
| [`audit/`](audit/) | Conformance audits of the live products, and open questions. |
| [`build/`](build/) | The generators. |
| [`tools/`](tools/) | `umbral-lint`, plus the independent verification scripts. |
| [`packages/`](packages/) | `umbral-viz` (Python) and `umbral-plot` (JS). |
| [`skills/`](skills/) | The agent skill. Install into `.claude/skills/`. |
| [`dist/`](dist/) | `CLAUDE.snippet.md` — paste into a downstream repo's `CLAUDE.md`. |
| [`assets/`](assets/) | Logo variants, generated from one parametric spec. |
| [`docs/`](docs/) | ADRs for the decisions that are hardest to reverse. |
| [`_inbox/`](_inbox/) | The v1.0 source material, kept for reference. |

## Two conventions worth knowing

**Never hand-edit anything under `tokens/build/`, `rules/rules.json`, or `guide/_includes/`.**
Change the source and rebuild. CI diffs the committed output and fails if it's stale.

**Semver applies to the design system, not just the code.** A token value change or a rule becoming
`error` is a **major**. A new rule at `warning` is a **minor**. Prose fixes are a **patch**.

## Status

| Phase | |
|---|---|
| 0 · Audit | done |
| 1 · Tokens | done |
| 2 · Rules | done |
| 3 · Guide prose | done |
| 4 · Agent skill + snippet | done |
| 5 · `umbral-lint` | done |
| 6 · Packages (`umbral-viz`, `umbral-plot`) | done |
| 7 · Site + release | next |
| 8 · Retrofit the four products | |

Open decisions live in [`audit/open-questions.md`](audit/open-questions.md).
