# umbral-viz

The Umbral design system for Python — matplotlib, Plotly, Altair and Streamlit.

```bash
pip install umbral-viz            # or: pip install "umbral-viz[all]"
```

```python
import umbral_viz as uv

uv.use("matplotlib")                       # or "plotly", "altair"
c = uv.tokens.tokens()                     # never retype a hex
```

## The chart frame is required, not optional

```python
frame = uv.Frame(
    title="Los registros crecen 9% anual desde 2015",
    subtitle="México · registros por año · escenario base con IC 80%",
    source="RNPDNO (CNB/SEGOB)", accessed="2026-07-09", snapshot="rnpdno-2026-07",
)
frame.apply_matplotlib(fig, ax)
frame.source_line()   # Fuente: … · consultado … · rnpdno-2026-07 · umbral.org.mx · datos CC BY 4.0
frame.warnings()      # non-fatal gaps worth raising in review
```

Constructing a `Frame` without `source` raises `MissingSource`. Asking `series()` for more than five
raises too. A chart that needs six series is two charts (UMB-CHT-006).

## Uncertainty helpers

```python
uv.themes.matplotlib_band(ax, x, lo, hi)          # 15% opacity band
uv.themes.matplotlib_today(ax, 2026)              # dashed «hoy» rule
uv.themes.matplotlib_label_series(ax, x[-1], y[-1], "Desapariciones", c["signal-text"])
uv.themes.abbreviate_axis(ax)                     # 12k, 3.7M
```

Direct labels use the `-text` variant. A series label is small text and needs 4.5:1. The line
itself only needs 3:1.

## Streamlit

```python
from umbral_viz import streamlit as ust

ust.install_config()          # copies the generated .streamlit/config.toml
ust.set_lang("es")            # Streamlit hardcodes lang="en" (UMB-A11Y-001)
ust.apply_fonts()
ust.kpi("Registros", "351,057", delta="+9%", delta_good=False)
ust.chart(fig, frame, df=df, filename="serie.csv")   # frame + table + CSV in one call
```

`kpi()` requires `delta_good` whenever a delta is shown. Whether a rise is good depends on the
metric, never on the sign. For disappearances it never is.

## Where the values come from

`umbral_viz/_data/` is vendored from `tokens/build/` at build time and verified byte-identical in
CI. Nothing in this package writes a colour, font or size as a literal.
