# `packages/`

The design system as installable libraries.

| | |
|---|---|
| [`umbral-viz/`](umbral-viz/) | Python — matplotlib, Plotly, Altair, Streamlit |
| [`umbral-plot/`](umbral-plot/) | JS — Observable Plot theme, chart frame, uncertainty helpers |

## Neither package embeds a value

They would otherwise be the fourth and fifth place token values live, after
`tokens/build/`, the skill's `assets/`, and downstream raw-URL fetches.

Instead `build/packages.mjs` vendors the generated files at build time, and
`tools/verify_packages.py` asserts every one is **byte-identical** to what the build produced. It
also fails if any module writes a colour, font or size as a literal.

That check exists because the v1.0 agent skill did the opposite. It froze its own copy of the
tokens and handed out failing contrast for a year. Nothing ever compared the two.

## Both refuse to draw a chart without its source

```python
uv.Frame(title="…", subtitle="…", source="")   # raises MissingSource
```

The v1.0 engineering doc asked for this: "a chart with no `source` should throw in dev". Nobody
built it, and the Phase 0 audit found charts shipping without a source.

Making the conformant call the *shorter* one is the only version of this that works.

```bash
npm run build:packages
python3 tools/verify_packages.py
```
