# Kickoff prompt — `umbral-style-guide`

> Paste this whole file as your first message to Claude Code in an empty clone of
> `github.com/umbralmx/umbral-style-guide`. Drop `CLAUDE.md` (the companion file) at the repo root
> first, plus the existing `assets/` (logo SVGs, tokens.json, tokens.css, the brand book PDF) into
> `_inbox/`. Then say: *"Read CLAUDE.md and KICKOFF-PROMPT.md, then start Phase 0."*

---

## 0. What we are building and why

Umbral (`umbral_`) is an independent, Spanish-first, open-source data lab. We already have a brand
book, tokens, logo files and four shipped products. What we do **not** have is a single normative
source that (a) a human can read like The Economist / FT / Urban Institute style guides, (b) a
linter can enforce, and (c) an AI agent working in any other Umbral repo can load and obey.

This repo becomes that source. It is a **design system + editorial style guide + machine-readable
rule set + agent skill**, published under CC BY 4.0 (content) and MIT (code).

Three consumers, one source of truth:

| Consumer | Surface they read |
|---|---|
| Humans (Jay, collaborators, contributors) | `guide/` prose → published site at `umbralmx.github.io/umbral-style-guide` |
| Machines (build tools, CI, linters) | `tokens/build/*`, `rules/rules.json` |
| Agents (Claude Code in other repos, Claude Design, Claude.ai) | `skills/umbral-brand/` + `dist/CLAUDE.snippet.md` |

**Non-negotiable architecture principle:** prose never states a rule that `rules/rules.yaml` does not
also state, and no file anywhere hard-codes a value that exists as a token. Prose and code are both
*generated from or validated against* the normative layer.

## 1. Existing material (in `_inbox/`)

- `Umbral_Brand_Book-print.pdf` / `umbral_brand_book.pdf` — v1.0, July 2026 (the two are the same content)
- `CLAUDE.md` (old, brand-level), `umbral-engineering.md`
- `tokens.json`, `tokens.css`
- `umbral-{isotype,lockup}-{light,dark}.svg`, `umbral-favicon.svg`

Treat these as **v1.0 input, not gospel.** Section 3 lists confirmed defects to fix. Migrate their
content into the new structure; do not simply copy them in.

## 2. Live products to audit (Phase 0)

Fetch and inspect each. Produce `audit/2026-07-conformance.md`: a table of every deviation from the
v1.0 brand book, keyed to the rule IDs you create in Phase 2, with severity and a one-line fix.

- https://umbralmx.github.io/ — main site (light mode expected)
- https://desaparecidosmx.streamlit.app/ — Streamlit, dark mode
- https://pautamx.streamlit.app/ — Streamlit, dark mode
- https://umbralmx.github.io/cabildo-libre/ — project microsite

For each, record: fonts actually loading, hex values actually rendered, chart title/source-line
presence, `lang` attribute, contrast of the smallest text, whether the underlying CSV is downloadable,
and how many elements use `signal`. This audit is what proves the guide is worth writing.

## 3. Known defects in v1.0 — fix these, don't propagate them

These are the reason we are upgrading rather than just reformatting.

**3.1 Contrast failures (highest priority).** The engineering doc claims both modes meet WCAG AA.
Hand-computed sRGB contrast ratios say otherwise. Verify all of these with a script before acting,
then fix by adjusting the token, not by dropping the requirement:

| Pair | Approx. ratio | Needs |
|---|---|---|
| `caption` `#9AA19B` on `base` `#F2F3F1` (light) | ~2.2:1 | ≥ 4.5:1 — this is axis-label and source-line **text** |
| `caption` `#5C6670` on `base` `#101418` (dark) | ~3.2:1 | ≥ 4.5:1 |
| `muted` `#6E756F` on `base` (light) | ~4.25:1 | ≥ 4.5:1 (just short) |
| `signal` `#128273` on `base` (light) | ~4.2:1 | ≥ 4.5:1 as text; passes 3:1 as a graphical mark |

Proposed resolution — **split the roles instead of one token doing double duty**:
- keep `signal` as the *mark* color (3:1 graphical threshold applies), add `signal-text` (a darker
  OKLCH-matched variant) for any text or link that must read at 4.5:1;
- darken `caption` in both modes until it clears 4.5:1 against **both** `base` and `panel`;
- publish a generated contrast matrix (`guide/02-color.md` includes it, `tokens/build/contrast.json`
  holds it) so this can never silently regress. CI fails on any pair below threshold.

**3.2 Streamlit config keys are mangled.** The brand book shows `sc-camel-primary-color`,
`sc-camel-background-color`, etc. Those are not real Streamlit keys — they are a camelCase artifact
from the PDF export. The correct `.streamlit/config.toml` keys are `primaryColor`,
`backgroundColor`, `secondaryBackgroundColor`, `textColor`, `font`. Two of our four products are
Streamlit apps, so ship this as a generated, tested file, not a code snippet in a PDF.

**3.3 No sequential or diverging color scales.** We define exactly three categorical series
(`signal`, `model`, `alert`). Every one of our real projects needs choropleths and heatmaps.
Derive and freeze: a sequential ramp anchored on `signal`, a second anchored on `model`, and a
diverging `alert`→neutral→`signal` ramp, all in OKLCH with perceptually even lightness steps, both
modes, checked for deuteranopia/protanopia/tritanopia. Include a `missing data` fill and a
`suppressed / below reporting threshold` hatch pattern — mandatory for disappearance and crime data.

**3.4 No numeric, date, or unit style.** This is the largest missing chunk relative to the Economist/
FT guides, which are mostly *this*. Specify for es-MX and en: thousands separator, decimal marker,
percent spacing, rounding and significant figures, when to use rate-per-100k vs count, currency
(MXN vs USD, when to state the year of real pesos), date formats (ISO in data, `junio 2026` in prose),
ranges, "más de"/"casi" usage, null vs zero vs suppressed.

**3.5 No terminology and sensitive-language glossary.** We publish on desapariciones and crime. The
difference between *persona desaparecida*, *persona no localizada*, and *desaparecido* is editorial,
legal, and ethical. Write `guide/15-terminologia.md` as a bilingual controlled vocabulary with a
"prefer / avoid / never" column and a short rationale per entry. This is the single most
credibility-relevant page in the guide.

**3.6 Fonts are not actually shipped.** The engineering doc says self-host; nothing self-hosts.
Vendor Space Grotesk and IBM Plex (both OFL) into `assets/fonts/`, subset to `latin` + `latin-ext`,
generate `@font-face` CSS, include the license files, and document the offline/government-network
rationale.

**3.7 No versioning or distribution story.** Downstream repos currently copy-paste. Fix with §5.

**3.8 Missing surfaces.** Quarto (Jay's primary document tool), notebooks, GitHub repo presentation
(README/social preview/topics), and OG/social-card metadata all need specs.

## 4. Target repo structure

```
umbral-style-guide/
├── CLAUDE.md                    ← agent contract for working *on* this repo
├── README.md                    ← human entry; what this is, how to consume it
├── CHANGELOG.md                 ← semver for the design system
├── LICENSE-CODE (MIT)  LICENSE-CONTENT (CC BY 4.0)
│
├── guide/                       ← the human-readable style guide, Spanish first
│   ├── 00-principios.md
│   ├── 01-marca.md              logo, isotipo, clear space, misuse gallery
│   ├── 02-color.md              modes, tokens, ramps, generated contrast matrix
│   ├── 03-tipografia.md
│   ├── 04-layout.md             grid, measure, spacing scale, rules-not-shadows
│   ├── 05-voz.md                voice, headline construction, hedging
│   ├── 06-numeros.md            NEW — numeric/date/unit style (§3.4)
│   ├── 07-vocabulario-visual.md NEW — chart chooser: intent → chart type → template
│   ├── 08-anatomia-grafica.md   title/subtitle/source frame, gridlines, labels
│   ├── 09-incertidumbre.md      bands, dashed futures, the `hoy` rule, CI reporting
│   ├── 10-mapas.md              NEW — choropleth rules, CVEGEO keys, rate vs count, small-n
│   ├── 11-accesibilidad.md
│   ├── 12-datos-procedencia.md  SOURCE.md spec, snapshots, licensing, reproducibility
│   ├── 13-interpretabilidad.md  causal vs descriptive language, defensible claims
│   ├── 14-superficies/          web.md · streamlit.md · quarto.md · notebook.md ·
│   │                            social.md · slides.md · github.md · email.md
│   └── 15-terminologia.md       NEW — bilingual controlled vocabulary (§3.5)
│
├── rules/
│   ├── rules.yaml               ← NORMATIVE. every rule, with a stable ID
│   ├── rules.schema.json
│   └── rules.json               generated
│
├── tokens/
│   ├── src/*.tokens.json        W3C DTCG format; primitives → semantic layers
│   └── build/                   generated, git-committed:
│       tokens.css · tokens.json · _tokens.scss · tokens.py · tokens.R ·
│       umbral.mplstyle · plotly-umbral.json · altair-umbral.py ·
│       streamlit-config.toml · _brand.yml (Quarto) · contrast.json
│
├── assets/
│   ├── logo/                    svg + png @1x/2x/3x, favicon set, og-image templates
│   ├── fonts/                   self-hosted subsets + OFL licenses
│   └── templates/               social 1080², slide 1920×1080, chart frame SVG
│
├── packages/
│   ├── umbral-viz/              Python: mplstyle loader, plotly template, altair theme,
│   │                            streamlit helpers (kpi, panel, chart frame, csv button)
│   └── umbral-plot/             JS/TS: Observable Plot theme + uncertainty helpers + CSS
│
├── skills/umbral-brand/         ← the Agent Skill (see §6)
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
├── tools/umbral-lint/           ← CLI conformance checker (see §7)
├── examples/                    correct-vs-incorrect gallery, one per surface
├── audit/                       product conformance audits over time
├── site/                        published guide (Quarto or Astro — see §8)
└── .github/workflows/           build · lint · contrast-check · pages · release
```

## 5. The normative layer: `rules/rules.yaml`

This is the keystone. Every rule gets a stable ID that prose cites, CI enforces, the skill quotes,
and a PR review can reference. Schema per rule:

```yaml
- id: UMB-COL-004
  title: "El color signal se usa en un solo elemento por vista"
  title_en: "signal is used on exactly one element per view"
  category: color            # brand|color|type|layout|chart|voice|numbers|data|a11y|method
  severity: error            # error | warning | info
  applies_to: [web, streamlit, slides, social, quarto, notebook]
  rationale: >
    La jerarquía visual de Umbral depende de que exista un único punto de atención…
  do: "Una serie, una cifra o un elemento de UI en signal."
  dont: "Signal en el logo, el botón y la serie principal a la vez."
  check:
    type: automated          # automated | manual | review
    tool: umbral-lint
    id: signal-count
  since: "1.0"
  supersedes: null
```

Rules to encode at minimum (expand from the v1.0 docs + §3): color token usage and the signal rule;
no pure black/white; no gradients; display type weight 500 never 700; approved font stack only;
radius ≤ 2px; no shadows; measure ≤ 65ch; chart must have finding-title + subtitle + source + license;
horizontal gridlines only; no pie/3D/dual-axis/untruncated-axis-without-note; ≤ 5 series; direct
labels not legend boxes; uncertainty visible on every projection or estimate; y-axis from zero for
bars; causal verbs only with an identification strategy; every dataset has SOURCE.md; every chart
ships its CSV; `lang` set; non-color encoding present; AA contrast; Spanish first.

Generate `guide/` rule callouts from `rules.yaml` at build time (an include/shortcode), so the prose
can never drift from the normative list. Generate a printable one-page `guide/CHECKLIST.md` too.

## 6. The Agent Skill: `skills/umbral-brand/`

Standard skill anatomy — `SKILL.md` with YAML frontmatter (`name`, `description`), body under ~500
lines, plus `references/` loaded on demand and `scripts/` for deterministic work.

The description must be pushy about triggering, roughly:

> `Applies the Umbral (umbral_) brand and data-visualization style system: color tokens and the two
> modes (laboratorio/instrumento), Space Grotesk/IBM Plex typography, chart anatomy, uncertainty
> visualization, Spanish-first editorial voice, numeric style, and accessibility rules. Use this
> skill whenever building or reviewing anything Umbral-branded — websites, Streamlit dashboards,
> Quarto documents, notebooks, charts, slides, social cards, READMEs — and whenever the user
> mentions umbral, umbralmx, desaparecidosmx, pautamx, cabildo-libre, tokens, signal color, modo
> laboratorio or modo instrumento, even if they don't say "brand" or "style guide".`

Body: how to pick the mode for the surface, the token table, the ten hardest rules, and a decision
procedure ("before writing any chart code, read `references/charts.md`"). Progressive disclosure:

```
references/  color.md · charts.md · voice-and-numbers.md · surfaces.md ·
             terminology.md · checklist.md
scripts/     check_contrast.py   — any pair of hexes → ratio + pass/fail
             apply_theme.py      — inject the right theme into a matplotlib/plotly/altair session
             lint.py             — thin wrapper over tools/umbral-lint
assets/      tokens.json (pinned copy), mplstyle, streamlit config, font @font-face css
```

Ship it two ways: as a folder in this repo for Claude Code (`.claude/skills/` symlink or copy in
downstream repos), and as a packaged `.skill` file in each GitHub release for claude.ai upload.

Also generate `dist/CLAUDE.snippet.md` — ~40 lines, the minimum any downstream repo's `CLAUDE.md`
needs, pinned to a version tag, pointing at the skill and the raw token URLs.

## 7. `tools/umbral-lint`

A CLI (Python; it must run in the same environments as the notebooks) that walks a repo and reports
rule violations with `file:line`, rule ID, severity, and fix hint. Exit non-zero on `error`.
Output formats: human, JSON, and GitHub Actions annotations. Checks to implement first, in order of
value-per-effort:

1. Hard-coded hex that matches a token value (should be `var(--u-…)` / `tokens[…]`) — trivially
   detectable, catches the most common real drift.
2. Banned font families (`Inter`, `Roboto`, `Arial`, `Helvetica`) in CSS/HTML/py.
3. `font-weight: 700` (or `bold`) on display selectors.
4. `border-radius` > 2px; any `box-shadow`.
5. Pure `#fff` / `#000` / `white` / `black`.
6. Charts without a source line — heuristic: a `Plot.plot(`, `px.`/`go.Figure`, or `plt.` call in a
   file with no `Fuente:` string nearby.
7. `signal` count per rendered view (HTML/SVG output only).
8. Missing `lang` attribute; missing `alt`/`aria-label` on figures.
9. Contrast: parse `tokens/build/contrast.json`, fail on any pair below threshold.
10. `SOURCE.md` missing for any directory under `data/raw/`.

Ship a GitHub Action (`umbralmx/umbral-lint-action`) so every Umbral repo can add five lines of YAML.

## 8. The published site

`site/` builds to GitHub Pages. Use **Quarto** if it can carry the interaction we need (Jay already
lives in Quarto, and it lets the guide itself be a reproducibility demo); otherwise Astro. Either
way the site must be a *demonstration* of the system, not a description of it: every color swatch,
type specimen, contrast ratio, and example chart is generated from `tokens/build/`, and at least one
page renders a real chart from a real Umbral dataset with a live mode toggle.

Include the FT-style *vocabulario visual* page as an interactive chart chooser, and a
correct-vs-incorrect gallery — the Urban Institute guide's most-cited feature is precisely the
side-by-side "before / after".

## 9. Build order

- **Phase 0 — Audit.** Fetch the four products, write `audit/2026-07-conformance.md`. Also run the
  contrast computations in §3.1 and confirm or correct my numbers. Report back before continuing.
- **Phase 1 — Tokens.** DTCG source, Style Dictionary build to all targets in §4, contrast matrix,
  new `signal-text` and corrected `caption`/`muted`, sequential + diverging ramps. CI check.
- **Phase 2 — Rules.** `rules.yaml` + schema + generated JSON. Every v1.0 rule migrated, IDs assigned.
- **Phase 3 — Guide prose.** Spanish first; English mirror only where it earns its place. Rule
  callouts generated from `rules.yaml`. New chapters 06, 07, 10, 15 written from scratch.
- **Phase 4 — Skill + snippet.** `skills/umbral-brand/` and `dist/CLAUDE.snippet.md`.
- **Phase 5 — Lint.** `tools/umbral-lint` with checks 1–5, then 6–10.
- **Phase 6 — Packages.** `umbral-viz` (Python) then `umbral-plot` (JS). Publish to PyPI/npm.
- **Phase 7 — Site + release.** Pages deploy, `v1.1.0` tag, packaged `.skill` attached to the release.
- **Phase 8 — Retrofit.** Open a PR against each of the four products fixing the audit findings.

Stop and check in with me at the end of each phase. Do not start Phase 1 before I have seen the
audit — if the contrast numbers are wrong, the whole token plan changes.

## 10. House rules for this build

- Spanish first in `guide/`; English for code, commit messages, and this meta-layer.
- Conventional Commits. One phase per branch, PR per phase.
- Nothing is "done" until it is generated from the normative layer and checked in CI.
- If you find a rule in the v1.0 docs that you believe is wrong, do not silently change it — add it
  to `audit/open-questions.md` with your reasoning and flag it to me.
- Write ADRs in `docs/adr/` for the three decisions that will be hardest to reverse: token
  architecture, site generator, and how downstream repos consume the system.