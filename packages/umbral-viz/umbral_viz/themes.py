"""Theme activation for matplotlib, Plotly and Altair.

Each theme sets colour, type and the chart furniture. None of them draws the frame —
titles, subtitles, source lines and CSV buttons stay the caller's job, because a
theme cannot know your finding. Use `umbral_viz.chart.Frame` for that.

Legends are disabled by default in every theme: Umbral labels series directly at the
line end (UMB-CHT-005). Re-enable one explicitly if you genuinely need it.
"""
from __future__ import annotations

import json

from . import tokens


def use_matplotlib(mode: str = "laboratorio"):
    """Activate the Umbral matplotlib style."""
    import matplotlib.pyplot as plt

    plt.style.use(str(tokens.style_path(mode)))
    return plt


def matplotlib_band(ax, x, low, high, mode: str = "laboratorio",
                    color: str | None = None, **kw):
    """A projection or confidence band at the brand opacity (UMB-CHT-011)."""
    c = color or tokens.color("signal", mode)
    kw.setdefault("linewidth", 0)
    return ax.fill_between(x, low, high, color=c,
                           alpha=tokens.uncertainty_opacity(), **kw)


def matplotlib_today(ax, x, label: str = "hoy", mode: str = "laboratorio"):
    """The dashed vertical rule marking the present."""
    t = tokens.tokens(mode)
    ax.axvline(x, linestyle=(0, (4, 3)), color=t["caption"], linewidth=1)
    ax.annotate(label, xy=(x, 1), xycoords=("data", "axes fraction"),
                xytext=(4, -10), textcoords="offset points",
                fontfamily=tokens.font("mono"), fontsize=9, color=t["caption"])


def matplotlib_label_series(ax, x, y, text: str, color: str, dx: int = 6):
    """A direct series label at the line end, instead of a legend (UMB-CHT-005)."""
    ax.annotate(text, xy=(x, y), xytext=(dx, 0), textcoords="offset points",
                va="center", ha="left", color=color,
                fontfamily=tokens.font("body"), fontsize=11)


def abbreviate(value: float, _pos=None) -> str:
    """12000 -> 12k, 3700000 -> 3.7M (UMB-CHT-007).

    Thousands separators below 10k, because «9,412» reads as a count while «9.4k»
    reads as an approximation.
    """
    a = abs(value)
    if a >= 1_000_000_000:
        return f"{value / 1_000_000_000:.3g}B".replace(".0B", "B")
    if a >= 1_000_000:
        return f"{value / 1_000_000:.3g}M".replace(".0M", "M")
    if a >= 10_000:
        return f"{value / 1_000:.3g}k".replace(".0k", "k")
    if a >= 1_000:
        return f"{value:,.0f}"
    return f"{value:g}"


def abbreviate_axis(ax, axis: str = "y"):
    """Apply the Umbral tick format to an axis."""
    from matplotlib.ticker import FuncFormatter

    fmt = FuncFormatter(abbreviate)
    if axis in ("y", "both"):
        ax.yaxis.set_major_formatter(fmt)
    if axis in ("x", "both"):
        ax.xaxis.set_major_formatter(fmt)
    return ax


def plotly_layout(mode: str = "laboratorio") -> dict:
    """The Umbral Plotly layout, ready for `fig.update_layout(**layout)`."""
    tpl = json.loads(tokens.plotly_template_path(mode).read_text(encoding="utf-8"))
    return {k: v for k, v in tpl["layout"].items() if k != "colorscale"}


def use_plotly(mode: str = "laboratorio"):
    """Register and activate the Umbral Plotly template."""
    import plotly.graph_objects as go
    import plotly.io as pio

    pio.templates["umbral"] = go.layout.Template(layout=plotly_layout(mode))
    pio.templates.default = "umbral"
    return pio


def altair_theme(mode: str = "laboratorio") -> dict:
    """The Umbral Altair theme config."""
    t = tokens.tokens(mode)
    return {"config": {
        "background": t["base"],
        "title": {"font": tokens.font("display"), "fontSize": 22,
                  "fontWeight": tokens.all_tokens()["font"]["displayWeight"],
                  "anchor": "start", "color": t["ink"]},
        "axis": {"labelFont": tokens.font("mono"), "labelFontSize": 12,
                 "labelColor": t["caption"], "titleFont": tokens.font("body"),
                 "titleFontSize": 12, "titleColor": t["muted"],
                 "domainColor": t["baseline"], "gridColor": t["gridline"],
                 "tickColor": t["baseline"], "grid": False},
        "axisY": {"grid": True, "domain": False, "ticks": False},
        "axisX": {"grid": False},
        "range": {"category": t["series"],
                  "heatmap": tokens.ramp("sequential_signal", mode),
                  "ramp": tokens.ramp("sequential_signal", mode),
                  "diverging": tokens.ramp("diverging", mode)},
        "legend": {"disable": True},
        "view": {"stroke": None},
    }}


def use_altair(mode: str = "laboratorio"):
    """Register and activate the Umbral Altair theme."""
    import altair as alt

    alt.themes.register("umbral", lambda: altair_theme(mode))
    alt.themes.enable("umbral")
    return alt
