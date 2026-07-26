# Changelog

Semver applies to the **design system**, not just the code (UMB-PRO-004):

- a token value change, or a rule moving to `error` → **major**
- a new rule at `warning`, a new ramp, a new surface chapter → **minor**
- prose and example fixes → **patch**

---

## 1.1.0 — 2026-07-26

The first release built from a normative layer. Everything below was motivated by the
[July 2026 conformance audit](audit/2026-07-conformance.md), which measured the four shipped
products in a browser and found **44% of visible text on the main site failing WCAG AA** — almost
none of it sloppiness, and most of it traceable to a specific line in a v1.0 document.

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
  legend boxes, which makes series colours into *small text* — 4.5:1, not the 3:1 a mark needs.
  `signal` alone could never satisfy both.
- **Sequential and diverging ramps**, a `missing` fill and a suppressed-value hatch. v1.0 defined
  three categorical colours and nothing else, while every real project needs choropleths.
- **`series-4` and `series-5`**, derived over lightness *and* hue — hue alone cannot produce five
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

- **The Streamlit config.** v1.0's brand book showed `sc-camel-primary-color` (a PDF-export
  artifact) *and* set `font = "sans serif"` — a valid Streamlit value meaning Streamlit's own Source
  Sans, which is why `pautamx` renders the wrong typeface. Both corrected in a generated file.
- **The logo.** v1.0 shipped three different bar ratios and a lockup whose bar crossed on the wrong
  side of the threshold line. All variants now generate from the 5:44 spec and are gated.
- **The third series colour.** The brand book said `muted`, the engineering doc's mplstyle and Plot
  theme said `caption` — at 2.37:1, below what a data mark needs. `muted` wins everywhere.
- **The false AA claim** in `umbral-engineering.md` §4, replaced by a generated contrast matrix that
  fails the build.

### Changed

- **UMB-COL-004 is scoped to the data layer.** Streamlit applies `primaryColor` to every widget at
  once, so "one `signal` element per view" was unsatisfiable for half the portfolio (OQ-002).
- **Contrast is gated by role**, not universally. Gridlines are deliberately below 3:1; a gate that
  failed on them would have been switched off within a week (OQ-001).
- **14 rules moved from `automated` to `review`**, each with a written reason. They named checks
  nobody had written, and a rule promising a check that does not run is worse than one honestly
  marked for review.

### Known gaps

- **OQ-009 is open.** `series-4`/`series-5` vary lightness, contradicting v1.0's "vary hue only".
  The evidence is logged; the decision is reversible.
- **`signal` and `model` are indistinguishable under tritanopia** (0.014 OKLab). Inherited from
  v1.0 and unfixable without changing a brand-defining colour. Mitigated by the mandatory direct
  labels and the ban on colour-only encoding.
- **matplotlib cannot read `.woff2`**, so notebooks fall back to a default face unless the families
  are installed system-wide. Vendoring TTFs would roughly double the asset weight.

---

## 1.0 — 2026-07

The original brand book, tokens and logo files. Preserved in `_inbox/`. Superseded by 1.1.0; see
the audit for what it got right and where it drifted.
