<!-- Umbral design system v1.5.0 — paste into a downstream repo's CLAUDE.md.
     GENERATED; regenerate from umbralmx/umbral-style-guide rather than editing. -->

## Umbral brand — the minimum

This repo follows the Umbral design system, pinned at **v1.5.0**.
Full guide: https://github.com/umbralmx/umbral-style-guide/tree/v1.5.0/guide

**Load the skill** before producing anything visual: copy
`umbral-style-guide/skills/umbral-brand/` into `.claude/skills/`, or install the packaged
`.skill` from the release.

**Never hand-type a colour, font or spacing value.** Import them:

```
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/tokens/build/tokens.css     # web
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/tokens/build/tokens.json    # anything
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/tokens/build/tokens.py      # Python / Streamlit / notebooks
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/tokens/build/tokens.R       # R / Quarto
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/tokens/build/observable-framework-instrumento.css   # Observable Framework
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/tokens/build/streamlit-config.toml
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.5.0/rules/rules.json            # the 78 rules, machine-readable
```

Pin the tag. Never point at `main` — a token change would land without warning.

**Two modes.** `laboratorio` (light) is the default: site, reports, documents, decks.
`instrumento` (dark) for dashboards, social cards and big-stat slides. Switch with
`data-mode="instrumento"`; never mix them inside one panel.

**The rules broken most often:**

- `signal` (`#128273`) marks **one** element of the data layer per view.
- Use `signal-text` (`#227c6f`) for text and direct series labels — `signal` only
  clears 3:1, and labels are small text needing 4.5:1.
- Chart titles state the finding as a sentence, not the topic.
- Every chart: subtitle (geography · period · unit), source line with licence and snapshot tag,
  `aria-label` with the finding, and a downloadable CSV.
- Space Grotesk **500** for display — never 700. Self-host the fonts; never a CDN.
- Uncertainty is visible: bands at 0.15 opacity, dashed past the
  present, a dashed `hoy` rule.
- Causal verbs only with a named identification strategy. Otherwise «asociado con».
- `lang="es"`. Never encode meaning by colour alone.
- Spanish first. Sensitive terminology is binding — see `guide/15-terminologia.md`.
- One statement per sentence, 25 words maximum. Active voice. One word for one thing.
- Section labels in mono lowercase. Lists are rows with 1px rules, not cards.
- A diagram shows a mechanism, drawn in 1px rules and text. No icons, no fill, no rounded nodes.
- A delta carries an arrow or a word. Colour never carries it alone, and never inside a pill.

**Never:** emoji · gradients · drop shadows · pill buttons · pure black or white · 700-weight
display · a chart without its source · a figure that cannot be rebuilt from raw data.
