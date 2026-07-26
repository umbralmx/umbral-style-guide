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
npm run build      # tokens, rules, logos, fonts, guide, skill, packages, site
npm run verify     # re-derives everything independently in Python
npm run lint       # umbral-lint over this repo
npm run site       # build and render the Quarto site
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

## Making an AI follow this guide in another project

Three steps, in order of how much they buy you. Step 1 alone gets you most of the way.

### 1. Install the skill

This is the important one. Once installed, Claude loads the brand system automatically whenever it
touches anything Umbral — you don't have to remember to ask.

```bash
mkdir -p .claude/skills
curl -L https://github.com/umbralmx/umbral-style-guide/releases/download/v1.1.0/umbral-brand-v1.1.0.skill -o /tmp/umbral.skill
unzip -q /tmp/umbral.skill -d .claude/skills/umbral-brand
```

For every project at once, use `~/.claude/skills/` instead of `.claude/skills/`. On claude.ai,
upload the `.skill` file directly.

> **If you already have a v1.0 skill installed, delete it first.** It bundles the old token values
> and will keep handing out colours that fail contrast:
> `rm -rf ~/.claude/skills/umbral-brand`

### 2. Paste the snippet into the project's `CLAUDE.md`

```bash
curl -O https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.1.0/dist/CLAUDE.snippet.md
cat CLAUDE.snippet.md >> CLAUDE.md
```

~40 lines: the pinned tag, the raw token URLs, the two modes, and the rules broken most often. It
covers the case where the skill isn't installed, and it tells a human collaborator the same things.

### 3. Add the linter to CI

```yaml
- run: pip install "git+https://github.com/umbralmx/umbral-style-guide@v1.1.0#subdirectory=tools/umbral-lint"
- run: umbral-lint . --format github
```

Findings appear inline on the PR diff. Severities come from the rule set, so what blocks a merge is
decided centrally rather than per repo.

### How to actually prompt it

With the skill installed you usually don't need to say anything — mentioning Umbral, a product name,
or asking for a chart is enough to trigger it. When you do want to be explicit:

> Build the dashboard following the Umbral style guide. Read the skill's `references/charts.md`
> before writing any chart code.

Two prompts worth knowing:

> **Review this against the Umbral guide and cite rule IDs.**
> Gets you findings you can look up, argue with, and check in CI — not vibes.

> **Which rules does this break, and which of them are `error`?**
> Separates what blocks a release from what's merely worth discussing.

And one instruction worth repeating, because it's the failure this whole system exists to prevent:

> Never type a hex, font name or spacing value from memory. Read it from the tokens.

If the model tells you a rule looks wrong, that's useful — it goes in `audit/open-questions.md` with
its evidence, not into a silent change. If a rule is right but inconvenient, the rule wins.

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
| [`site/`](site/) | The published guide. Quarto — see [ADR-0002](docs/adr/0002-site-generator.md). |
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
| 7 · Site + release | done |
| 8 · Retrofit the four products | next |

Open decisions live in [`audit/open-questions.md`](audit/open-questions.md); released changes in
[`CHANGELOG.md`](CHANGELOG.md).
