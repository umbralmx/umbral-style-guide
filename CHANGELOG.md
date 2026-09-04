# Changelog

Semver applies to the **design system**, not just the code (UMB-PRO-004):

- a token value change, or a rule moving to `error` → **major**
- a new rule at `warning`, a new ramp, a new surface chapter → **minor**
- prose and example fixes → **patch**

---

## 1.6.0 — 2026-09-03

The ten components, built. No new rule, no token change. `@umbralmx/umbral-plot` gains one public
export, which is why this is a minor and not a patch.

1.5.0 catalogued 66 shadcn/ui components. This ships the ten a data surface actually needs, and
stops there. The other 56 stay a lookup table.

`packages/umbral-plot/src/components.css` is **authored**, not generated. It is the one stylesheet
in the system a human edits, which makes it the one place a literal could re-enter. It is checked
twice: by `umbral-lint` like any file, and by `verify_packages.py` for a hex, a shadow, or a missing
export. Both guards were confirmed to fire.

| Class | Covers |
|---|---|
| `.u-rule` | `separator` |
| `.u-label` | the UMB-LAY-006 section label |
| `.u-rows` · `.u-row` | `item`, and the list `card` must not make |
| `.u-btn` | `button` |
| `.u-seg` | `tabs`, `toggle`, `toggle-group` |
| `.u-input` · `.u-select` | `input`, `native-select` |
| `.u-table` | `table`, `data-table` |
| `.u-cell` · `.u-empty` | `empty`, and the three empties of UMB-COL-010 |
| `.u-dialog` | `dialog`, `alert-dialog`, `sheet`, `drawer`, `popover` |
| `.u-kpi` | the figure inside a `card` |

Five overlay forms collapse into one. A native `<dialog>` opened with `showModal()` supplies the
whole UMB-A11Y-008 contract: focus enters, focus is trapped, Escape closes, focus returns. That was
verified in a browser, not assumed.

### Added

- `examples/componentes.html` — all ten, both modes, no build step. The first entry in `examples/`,
  which CLAUDE.md's definition of done has required since 1.0 and which did not exist until now.

### Fixed — the mode-switch trap

A section carrying `data-mode="instrumento"` inside a light page rendered dark-on-dark.

Custom properties inherit. A computed `color` does not re-resolve, so children kept the outer mode's
ink while the container painted the inner mode's background. `components.css` now makes any mode
container assert its own `color` and `background`.

This was found by opening the example, not by reading it. It would have hit the first Framework
dashboard with a dark panel.

### Note

The segmented control's active underline was drawn with an inset `box-shadow` in the first pass.
That is a rule faked with a shadow, against UMB-LAY-002, and `umbral-lint` did not catch it because
the check looks for drop shadows. It is a `border-bottom` now. The linter gap is real but small, and
is not worth a check that would flag every legitimate inset.

---

## 1.5.0 — 2026-09-03

The shadcn/ui catalogue mapped against the rules. One new chapter, one new rule, one new skill
reference. No token value changed, so nothing re-renders.

`guide/16-componentes.md` covers all 66 components the shadcn docs list. Each gets a verdict:
37 adopt, 20 adapt, 3 reject, 6 out of scope.

The useful finding is that the corrections are not per-component. Five of them cover almost
everything, and they were read out of the shadcn source rather than remembered.

| | shadcn ships | Rule |
|---|---|---|
| 1 | `rounded-md`, `rounded-xl`, `rounded-full` | UMB-LAY-001 |
| 2 | `shadow-xs`, `shadow-sm` | UMB-LAY-002 |
| 3 | Control heights `h-7` to `h-10` | UMB-A11Y-006 |
| 4 | Tailwind palette and its own variables | UMB-COL-002 |
| 5 | `font-semibold` headings | UMB-TYP-001 |

No default shadcn control height reaches 44px. `badge` and `switch` are `rounded-full`, which is a
pill, and the pill is on the Never list.

The forms are mostly fine. It is the defaults that are not.

### Added — the overlay rule

- **UMB-A11Y-008** (`warning`) — an overlay traps focus, closes on Escape, and returns focus to the
  control that opened it.

Six catalogue components are overlays: `dialog`, `alert-dialog`, `sheet`, `drawer`, `popover` and
`command`. Radix gives them this contract inside React. Nothing gave it to us outside React, and
UMB-A11Y-006 only covered the focus outline, not where the focus goes.

### Added

- `guide/16-componentes.md`, and its mirror in `site/`.
- `skills/umbral-brand/references/components.md`, parsed out of the chapter so the verdicts have one
  source. It is the seventh reference.
- OQ-011 — what a transient message may carry. A `toast` deletes itself, and a finding that deletes
  itself cannot be quoted or verified.
- OQ-012 — disabled controls against the 4.5:1 floor. UMB-COL-005 states no exception, WCAG 1.4.3
  does, and the repo currently has no disabled state that satisfies its own rule.

### Refused, and why

- **`switch`** — the form *is* a pill. An interrupted pill stops reading as a switch, so this is not
  a styling detail. The segmented control names both states in words instead.
- **`chart`** — it wraps a second charting library. Twelve UMB-CHT rules and `@umbralmx/umbral-plot`
  already cover this, and a second system means a second place a colour lives.
- **`carousel`** — already excluded by name in the 1.3 Framer survey. It hides content behind motion
  and fights `prefers-reduced-motion`.

### Note on 1.3.0

The 1.3.0 entry lists five component forms as shipping in "both packages" as `.u-heat`, `.u-table`,
`.u-seg`, `.u-toc-lines` and `.u-diagram`. The guide sections that specify them exist. The classes
do not exist in either package. The specification shipped; the implementation did not.

---

## 1.4.0 — 2026-09-03

Observable Framework replaces Streamlit as the dashboard surface. Two new rules. One new generated
target. No token value changed, so nothing re-renders.

The decision and its costs are in [ADR-0004](docs/adr/0004-dashboard-surface.md).

The move is cheaper than it looks. `packages/umbral-plot` already targets Observable Plot, and
Framework renders Observable Plot natively, so the whole chart layer transfers unchanged.

What did not transfer is the page around the chart. Nine Framework defaults collide with the guide.
`guide/14-superficies/framework.md` lists all nine beside their fixes.

Two of the nine could not be fixed in a stylesheet alone, because no rule covered them.

`theme: "dashboard"` resolves to `air` and `near-midnight`, each wrapped in a `prefers-color-scheme`
query. The reader's operating system then picks the mode. Umbral picks the mode by medium, and no
rule had ever needed to say so. **UMB-COL-011** says it.

Framework's themes derive `muted`, `faint`, `fainter` and `faintest` with `color-mix()` from one
foreground. Those values never reach `contrast.json`, so the gate passes them without measuring
them. UMB-COL-002 forbids a hand-written hex, and a formula is not a hex. **UMB-COL-012** closes it.

Both ship at `warning`, following UMB-LAY-006 through UMB-LAY-010.

### Added

- `framework` surface in `rules.schema.json`, carrying all 71 `web` rules. Framework is the `web`
  surface, not a reduced one: UMB-LAY-003, UMB-LAY-009 and UMB-LAY-010 apply again, because
  Framework returns the CSS control Streamlit withheld.
- `tokens/build/observable-framework-{laboratorio,instrumento}.css`. One file per mode, which is
  how UMB-COL-011 is enforced by the artifact's shape rather than by review.
- `guide/14-superficies/framework.md`, and its mirror in `site/`.
- UMB-COL-011 and UMB-COL-012, rendered into `guide/02-color.md`.
- `tools/verify_tokens.py` §8: 33 checks over the two stylesheets (208 to 241). Every `--theme-*`
  must match its token. No `color-mix()`, no built-in theme import, no `prefers-color-scheme` and
  no font CDN. `--font-big` must be mono, not Framework's 700-weight sans.
- OQ-010, on whether a KPI card is a list item or a figure. UMB-LAY-007 and Framework's `.card`
  disagree, and the chapter takes a position in order to ship.

### Changed

- UMB-A11Y-001 now covers an **absent** `lang` attribute. Framework emits `<html>` with none at all,
  which is worse than Streamlit's wrong-but-present `lang="en"`.
- UMB-COL-004's rationale no longer names Streamlit as the sole reason the rule is scoped to the
  data layer. Framework has the same one-accent-for-all-chrome problem via
  `--theme-foreground-focus`, but its accent can be bounded, so the rule reaches further there.
- The Framework stylesheets ship in `@umbralmx/umbral-plot`, not `umbral-viz`. A Framework app
  already depends on the JavaScript package for its charts.

### Not done

`desaparecidosmx` and `pautamx` still run on Streamlit. The `streamlit` surface stays in the rule
set until both migrate. The execution model is the real cost: Streamlit re-runs Python per
interaction, and Framework precomputes at build time and filters on the client.

---

## 1.3.0 — 2026-08-28

Five component forms, taken from a survey of the Framer components marketplace and rebuilt against
the tokens. One new rule. No token value changed, so nothing re-renders.

The survey is worth recording. The marketplace holds 143 components across its five real
categories.

33 are excluded by their name alone: glass, glow, 3D, grain, parallax, carousel, pill, bento, card
stack, pie, donut, radar. Most of the rest go once you look at them. The usual reason is a drop
shadow, or a delta encoded in colour alone.

Five forms survived. In every case the value was the form, not the code. A Framer component
hard-codes its colours and radii, which is UMB-COL-002 and UMB-PRO-003 by construction.

### Added — the diagram rule

- **UMB-LAY-010** (`warning`) — a diagram shows a mechanism, drawn with 1px rules and text. No
  icons, no colour fill, no rounded nodes.

UMB-LAY-005 bans decorative illustration. Without this rule a diagram would be an unwritten
exception to it, which is the same gap UMB-LAY-009 closed for the dot field.

The other four forms needed no new rule. They needed specification and implementation, not a norm.

The heatmap is already bound by UMB-COL-009 and UMB-COL-010. The table is bound by UMB-A11Y-003 and
UMB-A11Y-005. The segmented control is bound by UMB-LAY-008, and the line-menu index by
UMB-LAY-006.

### Added — the five components

| Form | Where it is specified | Where it ships |
|---|---|---|
| Calendar heatmap | `07-vocabulario-visual` § Densidad en el tiempo | both packages, `.u-heat` |
| Data table with deltas | `04-layout` § Tablas de datos | both packages, `.u-table` |
| Segmented control | `04-layout` § Controles (UMB-LAY-008) | `.u-seg` |
| Line-menu index | `04-layout` § Etiquetas de sección (UMB-LAY-006) | `.u-toc-lines` |
| Process diagram | `04-layout` § Diagramas (UMB-LAY-010) | `.u-diagram` |

The calendar heatmap is the one that filled a real gap. The chart chooser had no entry for daily
density over years, and the lab publishes on live daily registers.

It is also the chart that breaks UMB-COL-010 most easily. A day with no entry, a suppressed day and
a measured zero all look like an empty cell unless three fills are drawn. A live register makes it
worse: the recent tail is always empty, and empty reads as zero.

### Refused, and why

- **Count-up counters** — the most tempting category on the marketplace. The animation carries no
  information. On a disappearances count an odometer dramatises the figure, which UMB-MET-004
  forbids.
- **Pie, donut and radar charts** — UMB-CHT-010. Radar encodes in angle, with the same problem.
- **Smooth-scroll hijacking** — it overrides native scrolling and fights `prefers-reduced-motion`.
- **Arc maps** — an arc encodes nothing. An Umbral map is a rate choropleth.

---

## 1.2.0 — 2026-08-28

A minimal rewrite. It adds five rules at `warning`, one linter check and one surface chapter.

Every line of prose in the repo is rewritten to one statement per sentence.

No token value changed, so nothing re-renders. That is why this is a minor release.

### Added — the writing rule

- **UMB-VOZ-005** (`warning`) — a sentence states one thing and does not exceed 25 words. It is
  ASD-STE100 discipline applied to Spanish. Active voice, no semicolon joining two ideas, one word
  for one thing, and no metaphor where a number fits.
- **`long-sentence`** in `umbral-lint` — the check that makes it mechanical. It measures prose only:
  tables, code fences, front matter, bolded metadata fields and raw HTML are not sentences.
- **Three written exceptions.** A direct quotation, an accepted ADR, and third-party licence text
  are reproduced as they are.

Every chapter, README, changelog entry and rule rationale in the repo was rewritten against it. The
[Simplified English](https://github.com/AminBlg/SimpleEnglish) skill supplied the rule taxonomy.

### Added — the minimal layout idiom

Four rules make normative what `umbral.org.mx` already does, so the guide and the site it describes
stop disagreeing:

| Rule | |
|---|---|
| **UMB-LAY-006** | Section labels are mono, lowercase, in `caption` |
| **UMB-LAY-007** | A list of items is rows separated by 1px rules, not cards |
| **UMB-LAY-008** | Secondary controls are mono with a 1px border, moving to `signal` on focus |
| **UMB-LAY-009** | The dot field occupies only the outer margin of the sheet |

UMB-LAY-009 exists to resolve a contradiction rather than to add decoration. UMB-LAY-005 bans
decorative illustration. Without a written rule, the dot field would be an unwritten exception to
it. Written, it is bounded: a furniture token, outside the content sheet, gone on mobile.

- **`guide/14-superficies/landing.md`** — the portada surface. One sentence, no nav bar, rows
  instead of cards, and one optional entrance animation that degrades to static text.

### Changed — the site

- The site is rebuilt in that idiom. A dot field in the outer margin, a content sheet over it,
  mono lowercase labels, and 1px rules doing the separating.
- **It has navigation for the first time.** `theme: none` makes Quarto emit no navbar and no
  sidebar, so the `_quarto.yml` chrome had never rendered. `build/site.mjs` now writes a mono top
  bar and a footer into every page.
- Quarto's coloured callouts are replaced by `.u-note`, a labelled block behind a 1px rule. The
  callouts carried icons and a radius the system does not permit.
- The index page is the landing surface applied to this repo.
- Rule callouts are rows rather than filled panels.

### Known gaps

- **The prose rule is measured, not judged.** `long-sentence` counts words. It cannot see a short
  sentence that says nothing, and UMB-VOZ-003 is still the rule that catches that.
- **The Spanish/English split is unchanged.** UMB-VOZ-001 still holds: `guide/` is Spanish, the meta
  layer is English. STE-100 is applied to both.

---

## 1.1.0 — 2026-07-26

The first release built from a normative layer.

The [July 2026 conformance audit](audit/2026-07-conformance.md) measured the four shipped products
in a browser. It found **44% of visible text on the main site failing WCAG AA**. Almost none of it
was sloppiness. Most of it traced to a specific line in a v1.0 document.

### Breaking — token values changed

Every product re-renders. This is why the release is 1.1.0 and not 1.0.1.

| Token | v1.0 | 1.1.0 | |
|---|---|---|---|
| `caption` (light) | `#9AA19B` 2.37:1 | `#6C706D` 4.51:1 | the worst failure in the system |
| `muted` (light) | `#6E756F` 4.25:1 | `#565D57` 6.08:1 | darkened *past* the floor, or it collapsed onto `caption` |
| `caption` (dark) | `#5C6670` 2.93:1 | `#7A848F` 4.51:1 | |

Corrections hold hue exactly and move lightness, so each token stays recognisably the same colour.

### Added

- **`signal-text`, `model-text`, `alert-text`.** The brand mandates direct series labels instead of
  legend boxes. That makes a series colour into *small text*, which needs 4.5:1 rather than the 3:1
  a mark needs. `signal` alone could never satisfy both.
- **Sequential and diverging ramps**, a `missing` fill and a suppressed-value hatch. v1.0 defined
  three categorical colours and nothing else. Every real project needs choropleths.
- **`series-4` and `series-5`**, derived over lightness *and* hue. Hue alone cannot produce five
  colours a dichromat can separate (OQ-009).
- **`rules/rules.yaml`** — 69 rules with stable IDs, a written rationale each, and a JSON Schema.
- **Four new guide chapters**: `06-numeros`, `07-vocabulario-visual`, `10-mapas`, and
  `15-terminologia` (a binding bilingual controlled vocabulary).
- **`umbral-lint`** — 29 implemented checks, severities read from the rule set.
- **`umbral-viz`** and **`@umbralmx/umbral-plot`**. Both refuse to draw a chart without its source.
- **The agent skill** `skills/umbral-brand/`, with generated references and pinned assets.
- **Self-hosted fonts**, subset to `latin` + `latin-ext`, with their OFL licences.
- **The published site** — every swatch, ratio and specimen generated from the tokens.

### Fixed

- **The Streamlit config.** v1.0's brand book showed `sc-camel-primary-color`, a PDF-export
  artifact. It also set `font = "sans serif"`, a valid Streamlit value meaning Streamlit's own
  Source Sans. That is why `pautamx` renders the wrong typeface. Both are corrected in a generated
  file.
- **The logo.** v1.0 shipped three different bar ratios and a lockup whose bar crossed on the wrong
  side of the threshold line. All variants now generate from the 5:44 spec and are gated.
- **The third series colour.** The brand book said `muted`. The engineering doc's mplstyle and Plot
  theme said `caption`, at 2.37:1, below what a data mark needs. `muted` wins everywhere.
- **The false AA claim** in `umbral-engineering.md` §4, replaced by a generated contrast matrix that
  fails the build.

### Changed

- **UMB-COL-004 is scoped to the data layer.** Streamlit applies `primaryColor` to every widget at
  once. "One `signal` element per view" was unsatisfiable for half the portfolio (OQ-002).
- **Contrast is gated by role**, not universally. Gridlines are deliberately below 3:1. A gate that
  failed on them would have been switched off within a week (OQ-001).
- **14 rules moved from `automated` to `review`**, each with a written reason. They named checks
  nobody had written. A rule that promises a check that does not run is worse than one honestly
  marked for review.

### Known gaps

- **OQ-009 is open.** `series-4` and `series-5` vary lightness, which contradicts v1.0's "vary hue
  only". The evidence is logged. The decision is reversible.
- **`signal` and `model` are indistinguishable under tritanopia** (0.014 OKLab). It is inherited
  from v1.0 and unfixable without changing a brand-defining colour. The mitigation is the mandatory
  direct labels plus the ban on colour-only encoding.
- **matplotlib cannot read `.woff2`.** Notebooks fall back to a default face unless the families
  are installed system-wide. Vendoring TTFs would roughly double the asset weight.

---

## 1.0 — 2026-07

The original brand book, tokens and logo files. Preserved in `_inbox/`. Superseded by 1.1.0. See
the audit for what it got right and where it drifted.
