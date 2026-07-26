# `site/`

The published guide — https://umbralmx.github.io/umbral-style-guide

**Mostly generated. Do not edit `guide/`, `demo/`, `_includes/`, `styles.css` or `_quarto.yml`
here** — change `guide/` or `tokens/src/` and run the build.

```bash
npm run build:site     # regenerate site/ from guide/ + tokens + rules
quarto render site     # build site/_site/
npm run site           # both
```

| | |
|---|---|
| `index.qmd` `reglas.qmd` `checklist.qmd` | Generated |
| `guide/` | Generated from `guide/*.md` — `.md` links become `.qmd`, illustrative code fences are made non-executing |
| `demo/` | Generated: swatches, type specimen, chart chooser, correct-vs-incorrect gallery, and one real chart |
| `_includes/` `styles.css` `fonts/` `assets/` | Generated / copied |
| `data/raw/` | **Authored input.** A real dataset with its `SOURCE.md`. |
| `data/sesiones-por-anio.csv` | Rebuilt from `data/raw/` on every build (UMB-DAT-003) |

## The site demonstrates the system rather than describing it

Every swatch, ramp, contrast ratio and type specimen is generated from `tokens/build/`. There is no
hand-written colour anywhere in `site/`. If a token changes, the demonstration pages change with it.

`demo/grafica.qmd` rebuilds a chart from 7,019 real agenda points of the Colima cabildo, with a live
mode toggle. It is also the honest version: the two partial years are drawn dashed, because letting
them read as a collapse is the easiest way to misread a live register.

See [ADR-0002](../docs/adr/0002-site-generator.md) for why Quarto.
