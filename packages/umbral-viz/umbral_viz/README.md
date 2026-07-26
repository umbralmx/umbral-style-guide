# `umbral_viz/`

| | |
|---|---|
| `tokens.py` | Token access. Every other module reads values from here. |
| `themes.py` | matplotlib / Plotly / Altair activation, plus uncertainty and axis helpers |
| `chart.py` | `Frame` — the title/subtitle/source frame, which refuses to exist without a source |
| `streamlit.py` | Dashboard helpers: config, `lang` shim, KPI tiles, chart + table + CSV |
| `_data/` | **Generated.** Vendored byte-identically from `tokens/build/`. |

## Two rules this package holds itself to

**No module writes a value as a literal.** Not a hex, not a font family, not a size — including in
doctests, where pinning a value would make the docstring a second place it lives.
`tools/verify_packages.py` fails on any literal.

**The themes do not draw the frame.** A theme cannot know your finding, so titles, subtitles, source
lines and CSV buttons stay explicit. `chart.Frame` makes that the short path rather than the
diligent one.
