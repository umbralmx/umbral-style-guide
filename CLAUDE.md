# CLAUDE.md — `umbral-style-guide`

> This repo **is** the Umbral design system and editorial style guide. Every other Umbral repo
> consumes it. Read this file before touching anything; read `KICKOFF-PROMPT.md` for the build plan
> and the list of known v1.0 defects. Where this file and a human disagree, the human decides — but
> say so out loud rather than quietly complying.

---

## 1. What Umbral is

Umbral (`umbral_`) — *umbral* = threshold, the point where evidence becomes significant. An
independent, open-source data lab building data products, causal analysis, and monitoring tools for
the public interest. Spanish-first, bilingual-friendly, reproducible always.

Taglines: «Cruzar el umbral con datos» / "Where evidence crosses over."
Taste references: Isomorphic Labs (air, restraint, medium weights) · Our World in Data (chart
discipline) · AI Futures (uncertainty). Structural references for *this repo*: FT Visual Vocabulary,
Urban Institute Data Viz Style Guide, Economist Style Guide, BBC/FiveThirtyEight chart standards.

Shipped products: `umbralmx.github.io` · `desaparecidosmx.streamlit.app` ·
`pautamx.streamlit.app` · `umbralmx.github.io/cabildo-libre`.

## 2. The normative chain — obey this order

```
rules/rules.yaml  +  tokens/src/*.tokens.json      ← the only place a rule or value is authored
        ↓ build
tokens/build/*  ·  rules/rules.json                ← generated, committed, never hand-edited
        ↓ consumed by
guide/*.md  ·  site/  ·  packages/  ·  skills/  ·  tools/umbral-lint
```

Three hard consequences:

1. **Never hand-type a hex, font name, or spacing value** anywhere outside `tokens/src/`. If you
   need a value, import it from `tokens/build/`. `tools/umbral-lint` fails the build on this.
2. **Never state a rule in prose that isn't in `rules.yaml`.** Guide chapters cite rule IDs
   (`UMB-COL-004`) and render the rule text via the build, so prose cannot drift.
3. **Never edit a file under `tokens/build/` or `rules/rules.json`.** Change the source, rebuild.

## 3. Brand rules — the short form

Full text lives in `guide/`; this is what you need in working memory. When you're about to produce
anything visual, read the relevant `guide/` chapter first — do not work from this summary alone.

**Two modes.** Same type, layout, logo and semantics; only color tokens change.
`modo laboratorio` (light) is the **default**: site, reports, decks, documents, press.
`modo instrumento` (dark) for live dashboards, social cards, monitoring screens, deck section
dividers and big-stat slides. Switch with `data-mode="instrumento"` or `.u-dark`. Never mix modes
inside one panel.

**Color.** Semantic tokens: `ink · base · panel · border · gridline · baseline · muted · caption ·
signal · signal-text · model · alert`, plus sequential/diverging ramps. `signal` is reserved for the
**single most important element per view** — never decorative, never on the logo and a button and a
series at once. No pure white or black, no gradients. New categorical colors are derived in
`oklch()` matching the chroma and lightness of the existing series, varying hue only.
*Contrast is a build-time gate, not a review-time opinion:* `tokens/build/contrast.json` is
generated, and CI fails on any text pair below 4.5:1 or any graphical pair below 3:1.

**Type.** Space Grotesk **500** for display, headlines, chart titles, big figures — 600 only for
small bold labels, **never 700**. Medium weight is the signature. Tracking −0.02 to −0.03em on
display sizes. IBM Plex Sans 400–600 for body and UI. IBM Plex Mono 400–500 for axis ticks, source
lines, code, and all tabular figures. Never substitute Inter, Roboto, Helvetica or Arial. Minimums:
web 12px mono · slides 24px · documents 11pt.

**Logo.** Wordmark `umbral_` in Space Grotesk 500, lowercase always, underscore in `signal`. Isotype:
a vertical signal bar crossing a horizontal dashed threshold line, bar ≈ 5:44, crossing left of
centre. Clear space = one bar-height all round. No distortion, outline, effects, or recolor outside
tokens.

**Charts — the heart of the brand.** Every chart, in every medium, carries: a title that *states the
finding* as a sentence (Space Grotesk 500), a subtitle (geography · period · unit), and a source line
in mono (`Fuente: … · umbral.mx · CC BY 4.0`) above a 1px rule. Horizontal gridlines only, darker
baseline, no chart border. Direct series labels at line ends — no legend boxes. Max 4–5 series; one
in `signal`, the rest in `model`/`muted`; `alert` only for warnings. Mono axis ticks, abbreviated
(`12k`, `3.7M`), comma thousands separator. Bars from zero, solid fills, value labels in mono.
Never: pie, 3D, dual axes, truncated y-axis without an annotation, or a chart without its source.

**Uncertainty is a brand signature.** Projection bands at 15% opacity of the series color; dashed
stroke past the present; a dashed vertical rule labelled `hoy`. Point estimates without intervals are
incomplete. Rates state their denominator and `n`.

**Layout.** Generous margins, measure ≈ 65ch, 8px spacing scale, more whitespace than feels
necessary. Flat: 1px rules do the structural work. No shadows, no pills, no radius > 2px, no
decorative illustration.

**Voice.** Precise, sober, civic-scientific; the numbers carry the argument. Findings as full
sentences. Always name the source and its license. Spanish first, English added for international
artifacts. No hype words, exclamation marks, emoji, rhetorical-question headlines, or an adjective
where a number works.

**Method honesty.** "Asociado con"/"correlaciona" for descriptive work; "efecto", "reduce", "causa"
only with an identification strategy (RCT, DiD, RD, IV) named next to the estimate. Missing or
underreported data is disclosed, never silently dropped or imputed. Sensitive topics — desapariciones,
violence — are handled with dignity: people are counted, never made spectacle; no mapping to
identifiable individuals. Terminology comes from `guide/15-terminologia.md`, which is binding.

**Never list.** Emoji · gradients · stock icons · drop shadows · pill buttons · pure black/white ·
decorative SVG illustration · hype copy · 700-weight display type · `signal` on more than one element
per view · a chart without its source · a published figure that can't be rebuilt from raw.

## 4. Working on this repo

- **Language.** `guide/` is Spanish first; an English mirror only where it earns its place. Code,
  commit messages, ADRs, and this meta-layer are English. Set `lang` correctly on every rendered
  subtree.
- **Branches and commits.** One phase or feature per branch, PR per branch, Conventional Commits
  (`feat(tokens):`, `fix(a11y):`, `docs(guide):`, `chore(build):`).
- **Semver applies to the design system, not just the code.** A token value change or a rule
  becoming `error` is a **major**. A new rule at `warning`, a new ramp, or a new surface chapter is a
  **minor**. Prose and example fixes are **patch**. Every release updates `CHANGELOG.md` and attaches
  the packaged `.skill`.
- **Definition of done for any change:** builds from source with one command · tokens regenerate
  clean · `umbral-lint` passes on the repo and on `examples/` · contrast gate green · the guide page
  and the rule entry updated together · an example exists in `examples/`.
- **Disagreement protocol.** If a v1.0 rule looks wrong, do not silently change it. Add it to
  `audit/open-questions.md` with the evidence and raise it. If a rule is right but inconvenient, the
  rule wins.
- **Accessibility is not negotiable** for a public-interest lab. Never encode meaning by color alone
  — series need direct text labels, deltas need an arrow or a word. Charts need an `aria-label`
  summarizing the finding and an adjacent data table or `<details>`. Ship the CSV next to every
  chart. Respect `prefers-reduced-motion`; focus-visible outlines in `signal`; touch targets ≥ 44px.
- **Provenance.** Every dataset gets a `SOURCE.md` (origin URL, accessor, download date, license,
  caveats). Snapshots are tagged (`rnpdno-2026-07`) and charts state which snapshot they use. Code
  MIT, data and content CC BY 4.0. *If you can't reproduce the figure, it doesn't ship.*

## 5. Pre-ship checklist

- [ ] Correct mode for the medium — light by default, dark only where `guide/14-superficies/` says
- [ ] Every color, font and spacing value pulled from `tokens/build/`, none hand-typed
- [ ] Display is Space Grotesk 500 (not bold); body is Plex Sans; every number is Plex Mono
- [ ] Every chart: finding-title + subtitle + source line + license + downloadable CSV
- [ ] Uncertainty shown wherever a projection or estimate appears
- [ ] Exactly one `signal`-colored element per view
- [ ] AA contrast verified from the generated matrix; meaning never carried by color alone
- [ ] Spanish first; terminology conforms to `guide/15-terminologia.md`
- [ ] Causal language matches the identification strategy actually used
- [ ] `umbral-lint` clean; nothing from the Never list