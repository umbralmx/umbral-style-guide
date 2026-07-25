# Conformance audit — July 2026

Phase 0 of the `umbral-style-guide` build. Audits the four shipped Umbral products against the
v1.0 brand book, and verifies the contrast defects asserted in `KICKOFF-PROMPT.md` §3.1.

- **Audited:** 2026-07-25
- **Method:** live fetch + computed-style extraction in Chrome (not source inspection), so every
  value below is what a real visitor actually renders. Contrast computed per WCAG 2.1 relative
  luminance, against the *effective* background (walking up the ancestor chain past transparent
  fills), with the large-text exemption applied (≥24px, or ≥18.66px at weight ≥700 → 3:1).
- **Scripts:** `contrast.py`, `derive.py`, `cvd.py` (Phase 0 scratch; superseded in Phase 1 by the
  generated `tokens/build/contrast.json`).

Rule IDs below are **provisional** — they are the IDs I intend to author in Phase 2. They are cited
here so the audit and `rules.yaml` can be reconciled mechanically rather than by memory.

---

## 0. Headline

The v1.0 token set is applied with real discipline across all four products — the failures are
almost never sloppiness, they are **the tokens themselves being wrong**. Three of the four products
faithfully implement a palette that cannot pass WCAG AA.

| Product | Mode | `lang` | Fonts self-hosted | Text elements failing AA | `signal` count |
|---|---|---|---|---|---|
| umbralmx.github.io | mixed L/D | `es` ✓ | ✗ Google CDN | **29 / 66 (44%)** | 1 ✓ |
| cabildo-libre | laboratorio | `es` ✓ | ✓ | **12,092 / 17,394 (70%)** | 4 ✗ |
| desaparecidosmx | instrumento | `en` ✗ | ✓ | caption + pure-white present | **17** ✗ |
| pautamx | instrumento | `en` ✗ | ✓ | caption on every axis label | **10** ✗ |

Three findings dominate everything else:

1. **§3.1 is confirmed and worse than stated.** Jay's four ratios are right, but the failure set is
   larger — `alert` and `model` also fail as text in `modo laboratorio`, and the naive fix collapses
   `caption` into `muted`. See §2.
2. **Most live defects are faithfully-implemented instructions, not sloppiness.** The Google-Fonts
   dependency, the `Source Sans` leak, and the 2.37:1 matplotlib axis labels are each traceable to a
   specific line in `umbral-engineering.md` or the brand book. See §3.5. This is the audit's
   strongest evidence for the normative-layer architecture.
3. **`signal`-on-one-element is unenforceable in Streamlit as currently themed.** Streamlit's
   `primaryColor` is a global accent applied to every widget; both dashboards paint 10–17 elements
   in `signal` without a single deliberate misuse. See §4.1.

---

## 1. v1.0 material

The v1.0 source arrived mid-audit as `assets/` (rather than `_inbox/`): brand book PDF,
`tokens.json`, `tokens.css`, `umbral-engineering.md`, the brand-level `CLAUDE.md`, and five logo
SVGs. Before it arrived the token set had been reconstructed from the live products; that
reconstruction is **byte-identical** to `assets/tokens.css`, so the products and the source agree
exactly on colour.

The v1.0 token set, used as the Phase 1 input baseline:

| | `laboratorio` (light) | `instrumento` (dark) |
|---|---|---|
| `ink` | `#16191C` | `#EDF1F4` |
| `base` | `#F2F3F1` | `#101418` |
| `panel` | `#FAFAF8` | `#171C22` |
| `border` | `#DDE0DC` | `#2A3138` |
| `gridline` | `#E6E8E4` | `#232A31` |
| `baseline` | `#C4C9C4` | `#3A434C` |
| `muted` | `#6E756F` | `#8B95A0` |
| `caption` | `#9AA19B` | `#5C6670` |
| `signal` | `#128273` | `#5FD4C4` |
| `model` | `#5A63D8` | `#8B93F8` |
| `alert` | `#C8503F` | `#E26A5A` |

Non-color tokens: `--u-weight-display: 500`, `--u-tracking-display: -0.02em`, `--u-radius: 0px`,
`--u-rule: 1px`, `--u-space: 8px`.

**The brand book documents only 7 of the 11 colour tokens.** Page 03 lists `ink`, `base`, `panel`,
`muted`, `signal`, `model`, `alert` — and omits `caption`, `border`, `gridline`, `baseline`
entirely. `caption` is the worst-failing token in the system and the most-used small-text colour
across all four products, and it is **not documented anywhere in the brand book**. That is very
likely *why* it drifted: nothing to review it against.

The brand book PDF was read by decoding its subset-font ToUnicode CMaps (`pdftext.py`), since
poppler is not installed on this machine. Its full text is preserved at `audit/brandbook-v1.0.txt`
so Phase 3 can migrate the Spanish copy verbatim rather than paraphrase it.

---

## 2. Contrast — §3.1 verified

### 2.1 Jay's four numbers: all confirmed

| Pair | KICKOFF says | Measured | Verdict |
|---|---|---|---|
| `caption` on `base` (light) | ~2.2:1 | **2.37:1** | confirmed fail |
| `caption` on `base` (dark) | ~3.2:1 | **3.16:1** | confirmed fail |
| `muted` on `base` (light) | ~4.25:1 | **4.25:1** | confirmed fail (exact) |
| `signal` on `base` (light) | ~4.2:1 | **4.22:1** | confirmed — fails 4.5 text, passes 3:1 graphical |

### 2.2 Additional failures not listed in §3.1

The full matrix turned up three more, all in `modo laboratorio`:

| Pair | Ratio | Note |
|---|---|---|
| `alert` on `base` | **4.04:1** | fails as text; not mentioned in §3.1 |
| `alert` on `panel` | **4.30:1** | fails as text |
| `model` on `base` | **4.48:1** | fails by 0.02 — the cruellest kind of miss |
| `signal` on `panel` | **4.4991:1** | fails by 0.0009 |

This matters more than it looks. The brand mandates **direct series labels at line ends instead of
legend boxes** — which means series colors *are* text, at small sizes, and must clear 4.5:1, not
3:1. So `model` and `alert` need text-safe variants for exactly the same reason `signal` does.
§3.1's proposed `signal-text` split is right, but it is **not enough**: the same split is needed for
`model` and `alert`.

`modo instrumento` is in much better shape — only `caption` fails. Every other dark token clears AA.

### 2.3 The `caption`/`muted` collapse — a real design problem

Taking §3.1's instruction literally ("darken `caption` until it clears 4.5:1 against both `base` and
`panel`") produces `#6C706D` at OKLCH L=0.542. But `muted`, fixed the same way, lands at `#6A716B`
— **L=0.541. The two tokens become the same colour** (ΔL = 0.000). The light-mode grey hierarchy
`ink > muted > caption` cannot survive a naive minimal fix.

Recommended instead — push `muted` well past the floor so three distinct steps remain:

| Token | v1.0 | Proposed | vs `base` | vs `panel` |
|---|---|---|---|---|
| `ink` | `#16191C` | unchanged | 15.85 | 16.89 |
| `muted` | `#6E756F` | **`#565D57`** (L=0.47) | **6.09** | 6.48 |
| `caption` | `#9AA19B` | **`#6C706D`** (L=0.542) | **4.52** | 4.81 |

### 2.4 Proposed token changes (Phase 1 input)

All derived in OKLCH holding **hue fixed**, reducing chroma only where the target lightness left
sRGB gamut, so each corrected token stays recognisably the same colour.

**`modo laboratorio`**

| Token | v1.0 | Proposed | Ratio vs base / panel | Note |
|---|---|---|---|---|
| `caption` | `#9AA19B` | `#6C706D` | 4.52 / 4.81 | chroma 0.012→0.008 |
| `muted` | `#6E756F` | `#565D57` | 6.09 / 6.48 | darkened past floor, see §2.3 |
| `signal` | `#128273` | **unchanged** | 4.22 / 4.50 | stays the *mark* colour (3:1 applies) |
| `signal-text` | — | **`#227C6F`** | 4.51 / 4.81 | new; chroma 0.095→0.085 |
| `model-text` | — | **`#5962D7`** | 4.54 / 4.84 | new |
| `alert-text` | — | **`#BE4737`** | 4.55 / 4.85 | new |

**`modo instrumento`**

| Token | v1.0 | Proposed | Ratio vs base / panel |
|---|---|---|---|
| `caption` | `#5C6670` | **`#7A848F`** | 4.87 / 4.51 |
| everything else | — | **unchanged** | all ≥ 5.26 |

`*-text` tokens in dark mode can alias the base series colours (`signal` 10.31, `model` 6.72,
`alert` 5.68 — all pass), but should still exist as distinct token *names* so downstream code can
reference one semantic role across both modes.

### 2.5 A threshold-policy question the gate must answer first

`baseline`, `border` and `gridline` fail 3:1 against their backgrounds in **both** modes
(1.11–1.84:1). This is almost certainly **correct design**, not a defect: FT/Urban/OWID all use
gridlines far below 3:1 deliberately, and WCAG 1.4.11 only governs graphics *required to understand
the content*. Chart furniture is not.

So the CI gate must classify tokens by role, not check every pair:

- **text roles** (`ink`, `muted`, `caption`, `*-text`) → 4.5:1
- **data marks** (`signal`, `model`, `alert` as fills/strokes) → 3:1
- **furniture** (`gridline`, `border`, `baseline`) → **exempt**, deliberately low-contrast

A naive "fail on any pair below threshold" gate as written in §3.1 would fail on gridlines forever
and get switched off. Logged in `open-questions.md`.

### 2.6 Colour-vision deficiency — the series trio

Dichromacy simulation (Viénot/Brettel), reporting OKLab distance between series:

| | signal/model | signal/alert | model/alert |
|---|---|---|---|
| normal (light) | 0.208 | 0.247 | 0.283 |
| protanopia | 0.189 | **0.089** | 0.239 |
| deuteranopia | 0.171 | 0.119 | 0.280 |
| tritanopia | **0.014** | 0.361 | 0.354 |

`signal` and `model` are **indistinguishable under tritanopia** (0.014 — effectively identical), and
`signal`/`alert` are marginal under protanopia. Dark mode behaves similarly (signal/model 0.076
under tritanopia).

This is not a blocker — the brand already forbids encoding meaning by colour alone and mandates
direct labels, which is the correct mitigation. But it is a hard constraint on §3.3's ramps: the
sequential ramps anchored on `signal` and on `model` will collapse into each other for these
viewers, so **the two sequential ramps must never be used to distinguish two variables in the same
figure.**

---

## 3. Product-by-product

### 3.1 umbralmx.github.io — main site

Light default with two `data-mode="instrumento"` sections (`#proyectos`, `#metodologia`).

| Check | Result |
|---|---|
| `lang` | `es` ✓ |
| Fonts loading | Space Grotesk 500, IBM Plex Sans 400, IBM Plex Mono 400 ✓ (no 700 anywhere) |
| Font hosting | **`fonts.googleapis.com`** ✗ — confirms KICKOFF §3.6 |
| Hard-coded hex outside tokens | none ✓ |
| `border-radius` | `var(--u-radius)` only ✓ |
| `box-shadow` | none ✓ |
| Banned families | none ✓ |
| Contrast | **29/66 text elements fail** |
| `signal` count | 1 (wordmark underscore) ✓ |
| Charts | none on the page |

Failures by token: `muted` ×12, `caption` ×7 (light) + `caption` ×9 (dark sections), `signal` ×1.

That last one is notable: **the wordmark underscore itself fails.** `#128273` on `#F2F3F1` at 22px
weight 500 = 4.22:1, and at 22px/500 it does not qualify for the large-text exemption. The logo is
non-conformant against its own contrast rule — the single cleanest argument for the `signal-text`
split.

| ID | Finding | Sev | Fix |
|---|---|---|---|
| UMB-TYP-005 | Fonts served from Google CDN, not self-hosted | **error** | Vendor per §3.6; cabildo-libre already does this — copy its `assets/fonts.css` |
| UMB-COL-005 | 29/66 text elements below 4.5:1 | **error** | Adopt §2.4 tokens; no markup change needed |
| UMB-COL-005 | Wordmark `_` at 4.22:1 | **error** | Use `signal-text` for the wordmark |
| UMB-CNT-001 | Both bios are `Lorem ipsum` placeholder | **warning** | Write real copy before the guide ships as an exemplar |
| UMB-CNT-002 | Missing photo rendered as text placeholder "foto" | info | Ship the asset or drop the slot |

### 3.2 cabildo-libre

| Check | Result |
|---|---|
| `lang` | `es` ✓ |
| Fonts | **self-hosted, subset, with `unicode-range`** ✓ — the reference implementation |
| Contrast | 12,092 / 17,394 elements fail (`caption` ×7,354, `muted` ×4,736) |
| `signal` count | **4** ✗ — `_`, "Cabildo de Colima", `01`, `02` |
| Source line | ✓ present, with licence and independence disclaimer |
| CSV / JSON | ✓ both downloadable |
| Snapshot stated | ✓ "actualización de los datos: 23 de julio de 2026" |
| `border-radius` | max 2px ✓ (at the limit) |
| Method honesty | ✓ exemplary — declares AI-generated summaries over OCR, and lists known gaps ("27 sesiones… no imputados") |

The raw failure count is inflated by the timeline repeating one row pattern thousands of times; the
*distinct* failing styles number about a dozen. Same root cause as everywhere else — two tokens.

| ID | Finding | Sev | Fix |
|---|---|---|---|
| UMB-COL-005 | `caption` at 12px = 2.37:1 across the whole timeline and all stat labels | **error** | §2.4 tokens |
| UMB-COL-004 | 4 elements in `signal` in one view | **error** | Keep the hero accent; move `01`/`02` section numbers to `muted`, wordmark to `signal-text` |

The prose here is the strongest editorial writing across the four products, and §3.5's terminology
chapter should mine it.

### 3.3 desaparecidosmx

| Check | Result |
|---|---|
| Mode | `instrumento` ✓ correct for a dashboard |
| Tokens applied | `base #101418`, `ink #EDF1F4` ✓ exact |
| Fonts | Space Grotesk 500, Plex Sans 400/500/600, Plex Mono 400 ✓ self-hosted |
| `lang` | **`en`** ✗ on a Spanish app |
| Chart titles | ✓ finding-as-sentence: "El RNPDNO acumula 351,057 registros con hechos entre 2010-01 y 2026-07" |
| Subtitle | ✓ geography · unit · caveat |
| Source line | ✓ **with snapshot tag** — "Fuente: RNPDNO (CNB/SEGOB) · consultado 2026-07-09 · `rnpdno-2026-07` · umbral.mx · datos CC BY 4.0". Best-in-class; 2 charts, 2 source lines |
| CSV | ✓ per-chart download buttons |
| Uncertainty | ✓ dashed vertical rule + "provisional →" |
| Axis ticks | ✓ mono, abbreviated (`3.5k`) |
| `aria-label` on charts | **none** ✗ |
| Data table / `<details>` | 2 `<details>` present ✓ |

| ID | Finding | Sev | Fix |
|---|---|---|---|
| UMB-COL-004 | **17 elements** in `signal` — slider handles/labels, 6 multiselect chips, series | **error** | See §4.1; needs a Streamlit theming decision, not a per-app fix |
| UMB-A11Y-001 | `lang="en"` | **error** | Streamlit hardcodes this; needs a documented override recipe |
| UMB-TYP-003 | **11px** Plex Mono on 34 elements — below the 12px web minimum | **error** | Raise to 12px |
| UMB-COL-001 | `#FFFFFF` pure white on 6 elements | **error** | Streamlit widget default leaking; override to `ink` |
| UMB-COL-005 | `caption #5C6670` at 16px = 2.93:1 | **error** | §2.4 tokens |
| UMB-A11Y-002 | No `aria-label` on either chart | **error** | Add finding-summary label |
| UMB-TYP-004 | KPI figures in **Plex Sans 500 36px** | **warning** | See §4.2 — the guide contradicts itself here |

### 3.4 pautamx

| Check | Result |
|---|---|
| Mode | `instrumento` ✓ |
| Tokens | ✓ exact |
| `lang` | **`en`** ✗ |
| Chart titles | ✓ "El gasto observable acumula ≥ 107.6 M MXN" — states the finding *and* signals censoring with `≥` |
| Subtitle | ✓ names the interval explicitly: "la banda es el intervalo [cota inferior, cota superior] que publica Meta" |
| Source line | ✓ 2 visible charts, 2 source lines (3 further charts sit in inactive tabs) |
| Uncertainty | ✓ band rendered from Meta's published bounds — exemplary |
| Axis ticks | mono 12px, but coloured `#5C6670` = **2.93:1** ✗ |
| **CSV** | **none — zero download affordances** ✗ |
| `aria-label` | none ✗ |
| Fonts | **`Source Sans` loading and rendering** on ~10 elements ✗ |

| ID | Finding | Sev | Fix |
|---|---|---|---|
| UMB-A11Y-004 | No CSV anywhere; desaparecidosmx has it, this doesn't | **error** | Add `st.download_button` per chart |
| UMB-TYP-002 | Streamlit's `Source Sans` rendering on tab labels and captions | **error** | Set `font` in `config.toml`; ship as generated file (§3.2) |
| UMB-COL-005 | Every axis label at 2.93:1 | **error** | §2.4 tokens |
| UMB-COL-004 | 10 elements in `signal` | **error** | See §4.1 |
| UMB-A11Y-001 | `lang="en"` | **error** | as above |
| UMB-A11Y-002 | No `aria-label` on charts | **error** | Add |

---

### 3.5 The v1.0 source documents themselves

Several live defects are not product mistakes — they are faithfully implemented instructions. This
is the strongest argument in the audit for the normative-layer architecture: prose that isn't
generated from tokens drifts, and then products inherit the drift.

#### The AA claim

`umbral-engineering.md` §4:

> "Contrast: body text on `base`/`panel` meets WCAG AA (both modes are designed to). If you
> introduce a new color, verify ≥ 4.5:1 for text, ≥ 3:1 for UI/graph strokes."

The claim is false for `caption` (2.37:1 light, 3.16:1 dark) and `muted` (4.25:1 light) — and the
verification instruction applies only to *new* colours, so nobody was ever told to check the
existing ones. Phase 1 should cite this line when documenting the correction.

#### Self-hosting contradicts itself, in the same section

`umbral-engineering.md` §1 ships a Google Fonts `<link>` in its copy-paste HTML block, then eight
lines later says "Self-host the three fonts for production (don't ship a Google Fonts dependency on
a data product that must work offline / in government networks)." The brand book's Streamlit page
(10) likewise injects `@import url('https://fonts.googleapis.com/...')`.

Engineers copy code blocks, not prose. `umbralmx.github.io` uses the CDN; cabildo-libre — the one
product with no such snippet to copy — self-hosts correctly. **Defect 3.6 is a documentation bug
before it is an implementation bug.**

#### `caption` prescribed as a data-series colour

Both source docs put a token that fails 3:1 into a series palette:

| Source | Palette | Problem |
|---|---|---|
| `umbral-engineering.md` §2 mplstyle | `prop_cycle: ['128273','5A63D8','9AA19B','C8503F']` | 3rd series = `caption`, **2.37:1** on base |
| `umbral-engineering.md` §2 Plot theme | `range: [signal, model, caption, alert]` | same |
| Brand book p.10 Plotly | `colorway=[SIGNAL, MODEL, MUTED]` | uses `muted` — **inconsistent with the other two** |
| `CLAUDE.md` (brand) §6.4 | "others in model / muted gray" | says `muted` |

So the two documents disagree about the third series colour, and the version that won in Python
tooling is the one that fails contrast. The mplstyle also sets `xtick.color`/`ytick.color` to
`9AA19B` — so **any chart exported through the documented `umbral.mplstyle` has 2.37:1 axis
labels.** (No matplotlib output appears on the four live products, so this is a latent defect in the
tooling rather than a measured one — but `observatorio-delictivo-mx` is named as a consumer of it.)

#### Streamlit config — §3.2 confirmed exactly

Brand book p.10 renders:

```toml
[theme]
base                                = "dark"
sc-camel-primary-color              = "#5FD4C4"   # signal
sc-camel-background-color           = "#101418"   # base
sc-camel-secondary-background-color = "#171C22"
sc-camel-text-color                 = "#EDF1F4"   # ink
font                                = "sans serif"
```

The `sc-camel-` prefix is a PDF-export artifact wrapping the kebab-cased real key. Correct file:

```toml
[theme]
base                      = "dark"
primaryColor              = "#5FD4C4"
backgroundColor           = "#101418"
secondaryBackgroundColor  = "#171C22"
textColor                 = "#EDF1F4"
font                      = "IBM Plex Sans, sans-serif"
```

**There is a second, semantic bug on the same line that §3.2 doesn't mention.** `font = "sans serif"`
is a valid Streamlit value meaning *Streamlit's own default sans* — Source Sans. It is not a
mangling; it is simply wrong. This is the direct cause of the `Source Sans` rendering measured on
pautamx (§3.4). Fixing only the key names would leave that defect in place.

#### Logo files disagree with the spec and with each other

Brand book p.02 and `CLAUDE.md` both specify: bar ratio **≈ 5:44**, bar "cruza a la izquierda del
centro", clear space = one bar height.

| File | Bar w×h | Ratio | Bar centre vs line centre |
|---|---|---|---|
| spec | — | 1 : 8.8 | left |
| `umbral-isotype-light/dark.svg` | 12.8 × 91.2 | **1 : 7.13** | 54.4 vs 58.8 — left ✓ |
| `umbral-lockup-light/dark.svg` | 7 × 44 | **1 : 6.29** | 63.5 vs 58.0 — **right ✗** |

Three different bar ratios across spec, isotype and lockup; and the lockup's bar crosses to the
**right** of the threshold line's centre, contradicting the one geometric rule the brand book states
about the mark. Additionally the dashed threshold line is drawn in `caption` `#9AA19B` = **2.37:1**
on `base`, below the 3:1 needed for a meaningful graphical element.

| ID | Finding | Sev | Fix |
|---|---|---|---|
| UMB-BRD-001 | Lockup bar crosses right of centre | **error** | Rebuild lockup from the isotype geometry |
| UMB-BRD-002 | Three inconsistent bar ratios (5:44, 7.13, 6.29) | **error** | Pick one, generate both SVGs from it in Phase 1 |
| UMB-BRD-003 | Threshold line at 2.37:1 | **warning** | Darken with corrected `caption` (§2.4) → 4.52:1 |
| UMB-DOC-001 | `caption`/`border`/`gridline`/`baseline` undocumented | **error** | All tokens documented in `guide/02-color.md`, generated |
| UMB-DOC-002 | False AA claim in `umbral-engineering.md` §4 | **error** | Replace with the generated contrast matrix |
| UMB-DOC-003 | Google Fonts in code blocks vs self-host in prose | **error** | Generated `@font-face` CSS is the only snippet |
| UMB-DOC-004 | `caption` as 3rd series in mplstyle + Plot theme | **error** | Generated palettes; `muted`, per brand book |
| UMB-DOC-005 | `font = "sans serif"` in Streamlit config | **error** | Generated `streamlit-config.toml` |

---

## 4. Cross-cutting findings

### 4.1 `signal`-per-view is structurally unenforceable in Streamlit

Both dashboards paint 10–17 elements in `signal`, and **neither does anything wrong**. Streamlit
maps `primaryColor` onto slider tracks and handles, multiselect chips, tab underlines, focus rings
and links simultaneously. There is no Streamlit configuration in which `primaryColor` applies to
exactly one element.

UMB-COL-004 as written in KICKOFF §5 is therefore un-shippable for two of four products. Options:

1. **Scope the rule to data marks + one UI emphasis.** Widget chrome is exempt; the rule becomes
   "at most one `signal` element *in the data layer* per view".
2. **Set `primaryColor` to `muted`/`border`** and apply `signal` only through explicit chart colours
   and one deliberate CSS override.
3. Ship a `umbral-viz` CSS injection that neutralises widget accents.

My recommendation is **(1) as the rule + (3) as the tooling**, because (2) makes every Streamlit
widget look dead and fights the framework. Logged in `open-questions.md` — this is a rule-semantics
decision, not mine to make silently.

### 4.2 The guide contradicts itself on big figures

`CLAUDE.md` §3 says Space Grotesk 500 for "display, headlines, chart titles, **big figures**" and
also IBM Plex Mono for "**all tabular figures**". A KPI number is both. The products have already
diverged on this reading:

- desaparecidosmx → **Plex Sans 500 36px** (neither!)
- pautamx → **Plex Mono 500 25.6px**

`guide/06-numeros.md` must resolve it explicitly. My recommendation: **Mono for anything that aligns
in a column or is compared digit-by-digit; Grotesk for a standalone hero figure.** Both products
then need a change. Logged in `open-questions.md`.

### 4.3 Linter design: naive string matching is ~100% false positives

Worth recording now, because it directly shapes `tools/umbral-lint` (§7). Running the KICKOFF §7
checks as plain substring greps over `cabildo-libre/styles.css` produced **11 hits, all false**:

| Check | Hits | Reality |
|---|---|---|
| banned font `Inter` | 6 | `cursor: pointer` |
| pure `white` | 4 | `white-space: nowrap` / `pre-wrap` |
| `gradient` | 1 | `linear-gradient(var(--u-gridline), var(--u-gridline))` — a solid 1px rule, entirely on-brand |
| `box-shadow` | 2 | `inset 0 -2px 0 var(--u-signal)` — an inset rule, not a drop shadow |

So: `umbral-lint` must parse CSS declarations (property + value), match font families as
comma-separated stack tokens, treat `inset` shadows as rules rather than shadows, and allow
single-colour gradients. Naive greps would have flagged the *most* conformant product in the set.

### 4.4 What v1.0 got right

Worth stating, because the guide should codify these rather than reinvent them:

- Token discipline is genuinely excellent — **zero** hard-coded hexes outside `tokens.css` in either
  static product, across ~28KB of CSS.
- Source lines carry origin · access date · **snapshot tag** · licence. `rnpdno-2026-07` is exactly
  the provenance model §12 should specify.
- Uncertainty is already handled well and idiomatically in both dashboards.
- cabildo-libre's methodology section — declaring AI-generated OCR summaries, and listing gaps as
  "declarados y no imputados" — is a model for `guide/13-interpretabilidad.md`.
- No weight-700 display type, no shadows, no radius > 2px anywhere. The restraint rules stuck.

---

## 5. Recommendation before Phase 1

Phase 1 can start on the §2.4 numbers — they are verified and the derivation is reproducible. Four
decisions in `open-questions.md` should be settled first, because each changes what gets generated:

1. **OQ-001** — the contrast gate's role classification (§2.5); otherwise CI fails on gridlines forever.
2. **OQ-002** — UMB-COL-004's scope in Streamlit (§4.1); changes `rules.yaml` and the Streamlit theme.
3. **OQ-003** — big-figure typeface (§4.2); changes `tokens/build/` type roles and both dashboards.
4. **OQ-007** — the canonical logo bar ratio (§3.5); the three existing values can't all be right,
   and Phase 1 should generate the SVGs from whichever is chosen.

The v1.0 source in `assets/` is complete enough to proceed — no further input needed.
