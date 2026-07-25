"""altair-umbral.py — GENERATED from tokens/src/. Do not edit.
Umbral design system · https://github.com/umbralmx/umbral-style-guide
Code MIT · content CC BY 4.0

Direct series labels are the Umbral default, so legends are disabled in this theme.
If you genuinely need one, re-enable it explicitly at the chart level.
"""
import altair as alt

FONT_DISPLAY = "Space Grotesk"
FONT_BODY = "IBM Plex Sans"
FONT_MONO = "IBM Plex Mono"

_CONFIG = {
    "laboratorio": {
        "background": "#f2f3f1",
        "title": {"font": FONT_DISPLAY, "fontSize": 22, "fontWeight": 500, "anchor": "start", "color": "#16191c"},
        "axis": {
            "labelFont": FONT_MONO, "labelFontSize": 12, "labelColor": "#6c706d",
            "titleFont": FONT_BODY, "titleFontSize": 12, "titleColor": "#565d57",
            "domainColor": "#c4c9c4", "gridColor": "#e6e8e4",
            "tickColor": "#c4c9c4", "grid": False,
        },
        "axisY": {"grid": True, "domain": False, "ticks": False},
        "axisX": {"grid": False},
        "range": {
            "category": ["#128273","#5a63d8","#565d57","#c8503f","#902a00","#6331a0"],
            "heatmap": ["#eaf5f2","#c1d9d4","#98bfb6","#6fa59a","#448b7e","#007264","#00544a"],
            "ramp": ["#eaf5f2","#c1d9d4","#98bfb6","#6fa59a","#448b7e","#007264","#00544a"],
            "diverging": ["#942316","#b05b4d","#ca8c81","#e0bdb6","#f4efee","#b2cdc7","#79a99f","#3c8679","#006155"],
        },
        "legend": {"disable": True},
        "view": {"stroke": None},
    },
    "instrumento": {
        "background": "#101418",
        "title": {"font": FONT_DISPLAY, "fontSize": 22, "fontWeight": 500, "anchor": "start", "color": "#edf1f4"},
        "axis": {
            "labelFont": FONT_MONO, "labelFontSize": 12, "labelColor": "#7a848f",
            "titleFont": FONT_BODY, "titleFontSize": 12, "titleColor": "#8b95a0",
            "domainColor": "#3a434c", "gridColor": "#232a31",
            "tickColor": "#3a434c", "grid": False,
        },
        "axisY": {"grid": True, "domain": False, "ticks": False},
        "axisX": {"grid": False},
        "range": {
            "category": ["#5fd4c4","#8b93f8","#8b95a0","#e26a5a","#ffce2c","#b454b3"],
            "heatmap": ["#152220","#233f3a","#325f57","#428075","#51a395","#62c7b6","#72edd8"],
            "ramp": ["#152220","#233f3a","#325f57","#428075","#51a395","#62c7b6","#72edd8"],
            "diverging": ["#bc4b3a","#984538","#753e34","#543530","#332c2b","#39554f","#477d73","#54a899","#60d5c1"],
        },
        "legend": {"disable": True},
        "view": {"stroke": None},
    },
}


def umbral_theme(mode: str = "laboratorio"):
    """Return an Altair theme config for the given Umbral mode."""
    return {"config": _CONFIG[mode]}


def enable(mode: str = "laboratorio") -> None:
    """Register and activate the Umbral theme."""
    alt.themes.register("umbral", lambda: umbral_theme(mode))
    alt.themes.enable("umbral")
