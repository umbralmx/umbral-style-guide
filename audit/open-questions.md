# Open questions

Per `CLAUDE.md` §4 (Disagreement protocol) and `KICKOFF-PROMPT.md` §10: where a v1.0 rule looks
wrong or underspecified, it is recorded here with evidence rather than quietly changed.

Status: `open` · `decided` · `superseded`

**OQ-001 – OQ-008 were all decided on 2026-07-25**, adopting the proposal recorded under each.
The decision text below is normative for Phase 1 onward; where a decision and the v1.0 docs
disagree, the decision wins and the v1.0 line is cited as superseded.

---

## OQ-001 — The contrast gate needs role classification, or it will be switched off

**Status:** **decided** · **Blocks:** Phase 1 (`tokens/build/contrast.json`, CI gate) · **Raised:** 2026-07-25 · **Decided:** 2026-07-25

**Decision — adopt the three-role split.** Every token in `tokens/src/` carries an explicit
`$extensions.umbral.contrastRole` of `text` (gate 4.5:1), `mark` (gate 3:1) or `furniture`
(exempt, asserted). The exemption must be written per-token, never inherited by default, so a new
token cannot acquire it silently. `tokens/build/contrast.json` records the role, the measured ratio
and the applicable threshold for every pair; CI fails only where the role's gate is missed.

KICKOFF §3.1 specifies "CI fails on any pair below threshold" and `CLAUDE.md` §3 states "CI fails on
any text pair below 4.5:1 or any graphical pair below 3:1."

Taken literally this fails immediately and permanently: `gridline`, `border` and `baseline` sit at
**1.11–1.84:1** against their backgrounds in both modes. That is deliberate and correct — FT, Urban
Institute and OWID all render gridlines far below 3:1, and WCAG 1.4.11 governs only graphics
*required to understand the content*, which chart furniture is not.

A gate that fails on correct design gets disabled within a week, taking the real checks with it.

**Proposal — classify tokens by role in `tokens/src/`, and gate per role:**

| Role | Tokens | Threshold |
|---|---|---|
| text | `ink`, `muted`, `caption`, `signal-text`, `model-text`, `alert-text` | 4.5:1 |
| data mark | `signal`, `model`, `alert` (as fill/stroke) | 3:1 |
| furniture | `gridline`, `border`, `baseline` | exempt, asserted low-contrast |

The furniture exemption should be *explicit* in the token source (e.g. `"contrast": "exempt"`) so it
reads as a decision, not an oversight — and so a future token can't quietly inherit the exemption.

**Needs from Jay:** approve the three-role split, or specify a different gate.

---

## OQ-002 — `signal` on exactly one element per view cannot hold in Streamlit

**Status:** **decided** · **Blocks:** Phase 2 (`rules.yaml`), Phase 6 (`umbral-viz`) · **Raised:** 2026-07-25 · **Decided:** 2026-07-25

**Decision — option 1 as the rule, option 3 as the tooling.** UMB-COL-004 is scoped to the data
layer: "at most one `signal` element in the data layer per view", with widget chrome exempt.
`umbral-viz` additionally ships a CSS neutraliser so Streamlit's accents can be damped where a
project wants the stricter look. The `signal-count` lint check (KICKOFF §7 check 7) therefore runs
against rendered chart output only, not whole-page HTML — a deliberate narrowing recorded here so
it does not read as an oversight later.

Measured: desaparecidosmx renders **17** elements in `signal`, pautamx **10**. Neither app is
misusing the token. Streamlit maps `primaryColor` simultaneously onto slider tracks and handles,
multiselect chips, tab underlines, links and focus rings. **No Streamlit configuration produces
exactly one `signal` element.**

So UMB-COL-004 as drafted is unsatisfiable for half the product portfolio. Three ways out:

1. **Scope the rule to the data layer.** "At most one `signal` element in the data layer per view";
   widget chrome exempt. Keeps the rule meaningful where it earns its keep — charts.
2. **Set `primaryColor` to `muted`/`border`**, apply `signal` only via explicit chart colours plus
   one deliberate override. Purest, but every widget reads as disabled and it fights the framework.
3. **Ship a CSS neutraliser** in `umbral-viz` that strips widget accents.

**Recommendation: (1) as the rule, (3) as the tooling.** Option 2 trades a real usability cost for a
literal reading of a rule whose actual purpose — one focal point in the *data* — option 1 preserves.

Knock-on: the `signal-count` automated check (KICKOFF §7 check 7) can then only run against the
rendered data layer, not whole-page HTML. That is a meaningful narrowing of that check's scope.

**Needs from Jay:** pick 1, 2 or 3.

---

## OQ-003 — Big figures: Space Grotesk or IBM Plex Mono?

**Status:** **decided** · **Blocks:** Phase 3 (`guide/06-numeros.md`), Phase 8 retrofit · **Raised:** 2026-07-25 · **Decided:** 2026-07-25

**Decision — decide on alignment, not size.** IBM Plex Mono for any figure that aligns in a
column, is compared digit-by-digit, or sits in a KPI row where digits should line up across tiles
(tabular numerals are the point). Space Grotesk 500 for a single standalone hero figure read as
language rather than compared. Consequence: pautamx is already correct; desaparecidosmx's KPI row
moves from Plex Sans 500 to Plex Mono 500 in Phase 8.

`CLAUDE.md` §3 assigns Space Grotesk 500 to "display, headlines, chart titles, **big figures**" and
IBM Plex Mono to "axis ticks, source lines, code, and **all tabular figures**". A KPI number is
simultaneously a big figure and a tabular figure. The rule is genuinely ambiguous, and the products
have already resolved it three different ways:

| Product | KPI rendering |
|---|---|
| desaparecidosmx | Plex **Sans** 500 36px — matches neither reading |
| pautamx | Plex **Mono** 500 25.6px |
| umbralmx.github.io | no KPIs |

**Proposal:** the deciding property is *alignment*, not size.

- **Plex Mono** — any figure that aligns in a column, is compared digit-by-digit, or sits in a KPI
  row where digits should line up across tiles. Tabular numerals are the point.
- **Space Grotesk 500** — a single standalone hero figure inside a sentence or headline, where it is
  read as language rather than compared.

Under this reading pautamx is correct and desaparecidosmx needs a change.

**Needs from Jay:** confirm the alignment heuristic, or state a simpler rule.

---

## OQ-004 — `lang="en"` on the Streamlit apps

**Status:** **decided** · **Blocks:** Phase 3 (`guide/14-superficies/streamlit.md`) · **Raised:** 2026-07-25 · **Decided:** 2026-07-25

**Decision — `error`, with a documented shim.** Screen-reader users are exactly the constituency
a public-interest lab should not defer on. `guide/14-superficies/streamlit.md` carries a supported
`components.html` snippet setting `document.documentElement.lang`, and `umbral-viz` exposes it as a
helper so each app is one call away from compliance.

Both dashboards serve `<html lang="en">` while being entirely in Spanish. Streamlit hardcodes this;
it is not an app-level mistake. It affects screen-reader pronunciation and is a real a11y defect for
a Spanish-first lab.

Known workarounds are all somewhat unpleasant: a `components.html` JS shim setting
`document.documentElement.lang`, or patching Streamlit's `index.html` at deploy time.

**Needs from Jay:** decide whether the rule is `error` (with a documented shim in the Streamlit
surface chapter) or `warning` (acknowledged framework limitation). I lean `error` + shim — screen
reader users are exactly the constituency a public-interest lab should not defer on.

---

## OQ-005 — Sequential ramps anchored on `signal` and `model` collapse under tritanopia

**Status:** **decided** · **Blocks:** Phase 1 (§3.3 ramps) · **Raised:** 2026-07-25 · **Decided:** 2026-07-25

**Decision — derive both ramps, and make the constraint binding.** Both sequential ramps ship,
plus a rule (category `a11y`) that the `signal`-anchored and `model`-anchored ramps must never encode
two different variables in the same figure, because they are indistinguishable under tritanopia
(OKLab separation 0.014). Where two sequential scales genuinely must coexist, they must differ in
lightness range as well as hue, and `cvd.py` runs in CI to verify separation.

Measured OKLab separation between `signal` and `model` under simulated tritanopia: **0.014** in
light mode, 0.076 in dark — effectively identical colours. Under protanopia `signal`/`alert` falls
to 0.089.

The categorical trio is fine in practice because the brand already forbids colour-only encoding and
mandates direct labels. But KICKOFF §3.3 asks for *two* sequential ramps, one anchored on `signal`
and one on `model`. For a tritanope those two ramps are the same ramp.

**Proposal:** derive both ramps, but state as a binding rule that they must never encode two
different variables in the same figure (e.g. two choropleths side by side). Where two sequential
scales genuinely must coexist, vary lightness range as well as hue, and verify separation with the
CVD script in CI.

**Needs from Jay:** accept the constraint, or drop the second ramp in favour of one sequential +
one diverging.

---

## OQ-006 — v1.0 source material

**Status:** decided (resolved 2026-07-25) · **Raised:** 2026-07-25

The repo initially had no commits and no `_inbox/`. The v1.0 material arrived mid-audit as
`assets/` — brand book PDF, `tokens.json`, `tokens.css`, `umbral-engineering.md`, brand `CLAUDE.md`,
and five logo SVGs. Everything KICKOFF §1 lists is present.

The token set reconstructed from the live products before it arrived is byte-identical to
`assets/tokens.css`, so both routes agree. The brand book was read by decoding its ToUnicode CMaps
(poppler is not installed here); full text preserved at `audit/brandbook-v1.0.txt`.

No further input needed. Note the directory is `assets/`, not `_inbox/` — Phase 1 should decide
whether to move it to `_inbox/` for clarity, since `assets/` is also the name of a *target* directory
in the KICKOFF §4 structure and the collision will get confusing.

---

## OQ-007 — Which logo bar ratio is canonical?

**Status:** **decided and implemented** · **Raised:** 2026-07-25 · **Decided:** 2026-07-25 · **Implemented:** 2026-07-26

> Implemented in Phase 4, not Phase 1 as the decision said — the generator was written when the skill needed logo assets. `build/logo.mjs` now produces all five variants from the 5:44 spec, and gates them: the bar must cross left of the threshold line's centre, and both the bar and the dashed line must clear 3:1. The dashed line moved to the corrected `caption`, so it is now 4.52:1 rather than 2.37:1.

**Decision — 5:44 is canonical.** Both v1.0 documents state it, so the drawn files are the drift.
All logo variants (isotype, lockup, favicon, and the PNG/OG derivatives) are generated in Phase 1
from a single parametric source so they cannot diverge again; the crossing point is fixed to the
left of centre; and the dashed threshold line moves to the corrected `caption` (4.52:1) so it clears
the 3:1 a meaningful graphical element needs.

Three different values ship today, and they cannot all be right:

| Source | Bar w×h | Ratio |
|---|---|---|
| Brand book p.02 + `CLAUDE.md` §5 | — | **5:44** = 1 : 8.8 |
| `umbral-isotype-{light,dark}.svg` | 12.8 × 91.2 | 1 : 7.13 |
| `umbral-lockup-{light,dark}.svg` | 7 × 44 | 1 : 6.29 |

The lockup's `44` matches the spec's `44`, which suggests the intended bar width was `5` and it was
drawn at `7` — but the isotype matches neither.

Worse, the **lockup violates the one geometric rule the brand book states about the mark**: "La
barra cruza a la izquierda del centro." Its bar centre sits at x=63.5 against a threshold line
centred at x=58.0 — it crosses to the *right*. The isotype is correct (54.4 vs 58.8).

**Proposal:** treat **5:44** as canonical since both documents state it, fix the crossing point, and
generate all logo variants from a single parametric source in Phase 1 so isotype, lockup and favicon
can never diverge again. Also darken the dashed threshold line from `caption` (2.37:1, below the 3:1
a meaningful graphical element needs) to the corrected `caption` in OQ-001's §2.4 table.

**Needs from Jay:** confirm 5:44, or state the ratio the mark should actually have — this is a
visual-identity call, and the drawn files may well look better than the documented number.

---

## OQ-008 — Third series colour: `muted` or `caption`?

**Status:** **decided** · **Blocks:** Phase 1 (generated palettes) · **Raised:** 2026-07-25 · **Decided:** 2026-07-25

**Decision — `muted` is the third series.** It already has a 2:1 majority across the v1.0 docs and
it is the only one of the two that clears 3:1 as a data mark. All four chart palettes (mplstyle,
Observable Plot, Plotly, Altair) are generated from one token list. A legible 4th and 5th
categorical colour are derived in OKLCH during the Phase 1 ramp work, so the documented 4–5 series
maximum is actually reachable.

The v1.0 documents disagree:

| Source | 3rd series |
|---|---|
| Brand book p.10 (Plotly `colorway`) | `muted` |
| `CLAUDE.md` (brand) §6.4 | `muted` |
| `umbral-engineering.md` §2 (mplstyle `prop_cycle`) | **`caption`** |
| `umbral-engineering.md` §2 (Observable Plot `range`) | **`caption`** |

`caption` at `#9AA19B` is **2.37:1** on `base` — below the 3:1 a data mark requires. So the Python
and JS chart themes have shipped an effectively invisible third series, while the prose specifies a
legible one.

**Proposal:** `muted` is correct and already has a 2:1 majority; adopt it everywhere and generate all
four palettes from one token list so they cannot diverge again. Note this still leaves only three
usable categorical colours against a documented max of 4–5 series — Phase 1's ramp work (§3.3)
should derive a legible 4th and 5th in OKLCH at that point.

**Needs from Jay:** confirm `muted`, and confirm whether 4th/5th categorical colours are wanted now
or deferred.

---

## OQ-009 — "vary hue only" cannot produce five separable categorical colours

**Status:** open · **Blocks:** nothing — a decision was needed to ship Phase 1, and the reasoning is
recorded below so it can be reversed cheaply · **Raised:** 2026-07-26

`CLAUDE.md` §3 and the brand book p.03 both state that new categorical colours are derived
"matching the chroma and lightness of the existing series, **varying hue only**" (brand book:
«igualando croma y luminosidad de señal/model/alert, variando solo el tono»).

Measured against dichromacy simulation, that rule does not work. Holding lightness and chroma fixed
and scanning all 360 hues for the best-separated 4th and 5th series:

| Constraint | best series-4 | best series-5 |
|---|---|---|
| hue only (the v1.0 rule) | 0.076 | **0.042** |
| lightness and hue both free | 0.169 | **0.131** |

(Worst-case OKLab separation against all previously chosen series, across normal vision plus
simulated protanopia, deuteranopia and tritanopia. Below ~0.10 two marks are not reliably
separable.)

The reason is structural: for a dichromat, hue collapses to roughly one axis, so hue-only variation
has almost nothing left to vary. This is why Okabe–Ito and every other CVD-safe categorical palette
varies lightness substantially.

**Decision taken to ship Phase 1:** `series-4` and `series-5` vary lightness as well as hue
(`#902A00` and `#6331A0` in light mode). Accessibility is stated as non-negotiable in `CLAUDE.md`
§4, and the alternative was shipping two colours a colour-blind reader cannot separate.

**Proposal for the rule text:** replace "varying hue only" with something like *"varying hue and, if
necessary, lightness; verify with `audit/scripts/cvd.py` that worst-case separation against every
existing series stays above 0.10."* Hue-only remains the right advice for a **sequential ramp**,
where lightness is already doing the encoding — the v1.0 rule is not wrong, it is misapplied to the
categorical case.

**Worth knowing regardless of the decision:** the weakest pair in the palette is not one of the new
colours. It is `signal`/`model`, at **0.014** under tritanopia — they are effectively the same
colour to such a reader. That is inherited from v1.0 and cannot be fixed without changing a
brand-defining colour. The mitigation is the brand's own rule that meaning is never carried by
colour alone, which is why direct series labels are mandatory rather than stylistic.

**Needs from Jay:** confirm the rule change for `guide/02-color.md`, or tell me to revert
`series-4`/`series-5` to hue-only and accept the 0.042.
