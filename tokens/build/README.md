# `tokens/build/`

**Generated from `tokens/src/`. Never edit anything here** (UMB-PRO-001) — change the source and run
`npm run build:tokens`. CI diffs this folder and fails if it's stale.

It's committed rather than built on install so a notebook, a Quarto doc or a downstream repo can
fetch a raw URL without needing Node.

| File | For |
|---|---|
| `tokens.css` | Web. Custom properties, both modes, plus the ramps. |
| `tokens.json` | Anything that can read JSON. |
| `_tokens.scss` | Sass maps. |
| `tokens.py` | Python — notebooks, Streamlit, `umbral-viz`. |
| `tokens.R` | R — ggplot, Quarto. |
| `umbral-{laboratorio,instrumento}.mplstyle` | matplotlib. |
| `plotly-umbral-{mode}.json` | Plotly layout template. |
| `altair-umbral.py` | Altair theme. Legends disabled — Umbral labels series directly. |
| `streamlit-config.toml` | Copy to `.streamlit/config.toml`. Real keys, correct font. |
| `_brand.yml` | Quarto brand file. |
| `contrast.json` | The generated contrast matrix. What the CI gate reads. |

`contrast.json` is the interesting one: it records every token pair, its measured ratio, the role it
declared, and the threshold that role implies. That's what makes contrast a build-time gate instead
of a review-time opinion.
