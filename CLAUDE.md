# CLAUDE.md — `umbral-style-guide`

> This repo **is** the Umbral design system and editorial style guide. Every other Umbral repo
> consumes it. Read this file before touching anything. Read `KICKOFF-PROMPT.md` for the build plan
> and the list of known v1.0 defects. Where this file and a human disagree, the human decides. Say
> so out loud rather than quietly complying.

---

## 1. What Umbral is

Umbral (`umbral_`) is an independent, open-source data lab. It builds data products, causal analysis
and monitoring tools in the public interest. *Umbral* means threshold: the point where evidence
becomes significant. Spanish-first, bilingual-friendly, reproducible always.

Taglines: «Cruzar el umbral con datos» / "Where evidence crosses over."

Taste references: Isomorphic Labs for air and restraint · Our World in Data for chart discipline ·
AI Futures for uncertainty · opencode.ai/data for dense mono data layout.
Structural references for *this repo*: FT Visual Vocabulary, Urban Institute Data Viz Style Guide,
Economist Style Guide, BBC and FiveThirtyEight chart standards.

Shipped products: `umbral.org.mx` · `desaparecidosmx.streamlit.app` · `pautamx.streamlit.app` ·
`umbralmx.github.io/cabildo-libre`.

## 2. The normative chain — obey this order

```
rules/rules.yaml  +  tokens/src/*.tokens.json      ← the only place a rule or value is authored
        ↓ build
tokens/build/*  ·  rules/rules.json                ← generated, committed, never hand-edited
        ↓ consumed by
guide/*.md  ·  site/  ·  packages/  ·  skills/  ·  tools/umbral-lint
```

Three hard consequences:

1. **Never hand-type a hex, font name, or spacing value** outside `tokens/src/`. Import the value
   from `tokens/build/`. `tools/umbral-lint` fails the build on a literal.
2. **Never state a rule in prose that is not in `rules.yaml`.** Guide chapters cite rule IDs
   (`UMB-COL-004`) and render the rule text from the build, so prose cannot drift.
3. **Never edit a file under `tokens/build/` or `rules/rules.json`.** Change the source and rebuild.

## 3. Brand rules — the short form

The full text lives in `guide/`. This is what you need in working memory. Before you produce
anything visual, read the relevant `guide/` chapter. Do not work from this summary alone.

**Two modes.** Same type, layout, logo and semantics. Only the colour tokens change.
`modo laboratorio` (light) is the **default**: site, reports, decks, documents, press.
`modo instrumento` (dark) is for live dashboards, social cards, monitoring screens, deck section
dividers and big-stat slides. Switch with `data-mode="instrumento"` or `.u-dark`. Never mix modes
inside one panel.

**Colour.** Semantic tokens: `ink · base · panel · border · gridline · baseline · muted · caption ·
signal · signal-text · model · alert`, plus sequential and diverging ramps. `signal` marks the
**single most important element per view**. It is never decorative, and never on the logo and a
button and a series at once. No pure white or black. No gradients. Derive a new categorical colour
in `oklch()`, matching the chroma and lightness of the existing series and varying hue.
*Contrast is a build-time gate, not a review-time opinion.* `tokens/build/contrast.json` is
generated. CI fails on any text pair below 4.5:1 or any graphical pair below 3:1.

**Type.** Space Grotesk **500** for display, headlines, chart titles and big figures. Use 600 only
for small bold labels. **Never 700.** The medium weight is the signature. Tracking is −0.02 to
−0.03em on display sizes. IBM Plex Sans 400–600 for body and UI. IBM Plex Mono 400–500 for axis
ticks, source lines, code and all tabular figures. Never substitute Inter, Roboto, Helvetica or
Arial. Minimums: web 12px mono · slides 24px · documents 11pt.

**Logo.** Wordmark `umbral_` in Space Grotesk 500, lowercase always, underscore in `signal`.
Isotype: a vertical signal bar crossing a horizontal dashed threshold line. The bar ratio is 5:44
and it crosses left of centre. Clear space is one bar-height on all four sides. No distortion, no
outline, no effects, no recolour outside the tokens.

**Charts are the heart of the brand.** Every chart, in every medium, carries three things: a title
that *states the finding* as a sentence (Space Grotesk 500), a subtitle (geography · period · unit),
and a source line in mono (`Fuente: … · umbral.mx · CC BY 4.0`) above a 1px rule.
Horizontal gridlines only, darker baseline, no chart border. Label series directly at line ends. No
legend boxes. Maximum 4–5 series: one in `signal`, the rest in `model` or `muted`. Use `alert` only
for warnings. Axis ticks are mono and abbreviated (`12k`, `3.7M`), with comma thousands separators.
Bars start at zero, use solid fills, and carry value labels in mono.
Never: pie, 3D, dual axes, a truncated y-axis without an annotation, or a chart without its source.

**Uncertainty is a brand signature.** Projection bands at 15% opacity of the series colour. Dashed
stroke past the present. A dashed vertical rule labelled `hoy`. A point estimate without an interval
is incomplete. A rate states its denominator and its `n`.

**Layout.** Generous margins. Measure ≈ 65ch. An 8px spacing scale. More whitespace than feels
necessary. Flat: 1px rules do the structural work. No shadows, no pills, no radius above 2px, no
decorative illustration.

**The minimal idiom** — new in 1.2, and what `umbral.org.mx` already does:
- Section labels are mono, lowercase, in `caption`. They name structure, not content (UMB-LAY-006).
- A list of items is rows separated by 1px rules that reach the container edge. Not cards
  (UMB-LAY-007).
- A secondary control is a 1px rectangle in mono with no fill. Hover and focus move it to `signal`
  (UMB-LAY-008).
- The dot field lives in the outer margin only, behind the content sheet. It never sits under text
  (UMB-LAY-009).
- A landing page has no nav bar. The mark sits at the start of the content
  (`guide/14-superficies/landing.md`).

**Voice.** Precise, sober, civic-scientific. The numbers carry the argument. State findings as full
sentences. Always name the source and its licence. Spanish first, English added for international
artifacts. No hype words, no exclamation marks, no emoji, no rhetorical-question headlines, and no
adjective where a number works.

**Write one statement per sentence, 25 words maximum** (UMB-VOZ-005). Use active voice. Use one word
for one thing throughout a document. Do not join two ideas with a semicolon. Do not use a metaphor
where a number fits. This is ASD-STE100 discipline applied to Spanish and to English. It binds what
you write here as well as what you review. `umbral-lint` checks it.

**Method honesty.** Use "asociado con" and "correlaciona" for descriptive work. Use "efecto",
"reduce" and "causa" only with an identification strategy named next to the estimate: RCT, DiD, RD
or IV. Disclose missing or under-reported data. Never drop or impute it silently. Handle sensitive
topics — desapariciones, violence — with dignity: count people, never make spectacle of them, and
never map to identifiable individuals. Terminology comes from `guide/15-terminologia.md`, which is
binding.

**Never list.** Emoji · gradients · stock icons · drop shadows · pill buttons · pure black or white ·
decorative SVG illustration · hype copy · 700-weight display type · `signal` on more than one element
per view · a chart without its source · a published figure that cannot be rebuilt from raw.

## 4. Working on this repo

- **Language.** `guide/` is Spanish first. An English mirror only where it earns its place. Code,
  commit messages, ADRs and this meta layer are English. Set `lang` correctly on every rendered
  subtree.
- **Branches and commits.** One phase or feature per branch. One PR per branch. Conventional Commits
  (`feat(tokens):`, `fix(a11y):`, `docs(guide):`, `chore(build):`).
- **Semver applies to the design system, not just the code.** A token value change, or a rule
  becoming `error`, is **major**. A new rule at `warning`, a new ramp, or a new surface chapter is
  **minor**. Prose and example fixes are **patch**. Every release updates `CHANGELOG.md` and
  attaches the packaged `.skill`.
- **Definition of done for any change.** It builds from source with one command. Tokens regenerate
  clean. `umbral-lint` passes on the repo and on `examples/`. The contrast gate is green. The guide
  page and the rule entry are updated together. An example exists in `examples/`.
- **Disagreement protocol.** If a rule looks wrong, do not silently change it. Add it to
  `audit/open-questions.md` with the evidence and raise it. If a rule is right but inconvenient, the
  rule wins.
- **Accessibility is not negotiable** for a public-interest lab. Never encode meaning by colour
  alone: a series needs a direct text label, a delta needs an arrow or a word. A chart needs an
  `aria-label` summarising the finding and an adjacent data table or `<details>`. Ship the CSV next
  to every chart. Respect `prefers-reduced-motion`. Draw focus-visible outlines in `signal`. Give
  touch targets 44px or more.
- **Provenance.** Every dataset gets a `SOURCE.md`: origin URL, accessor, download date, licence,
  caveats. Tag snapshots (`rnpdno-2026-07`) and state which snapshot a chart uses. Code is MIT. Data
  and content are CC BY 4.0. *If you cannot reproduce the figure, it does not ship.*

## 5. Pre-ship checklist

- [ ] Correct mode for the medium — light by default, dark only where `guide/14-superficies/` says
- [ ] Every colour, font and spacing value pulled from `tokens/build/`, none hand-typed
- [ ] Display is Space Grotesk 500, not bold. Body is Plex Sans. Every number is Plex Mono.
- [ ] Every chart: finding-title, subtitle, source line, licence, downloadable CSV
- [ ] Uncertainty shown wherever a projection or estimate appears
- [ ] Exactly one `signal`-coloured element per view
- [ ] AA contrast verified from the generated matrix. Meaning never carried by colour alone.
- [ ] Section labels in mono lowercase. Lists as rows, not cards. Dot field in the margin only.
- [ ] Spanish first. Terminology conforms to `guide/15-terminologia.md`.
- [ ] One statement per sentence, 25 words maximum
- [ ] Causal language matches the identification strategy actually used
- [ ] `umbral-lint` clean. Nothing from the Never list.
