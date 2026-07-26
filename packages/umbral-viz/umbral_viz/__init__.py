"""umbral-viz — the Umbral design system for Python charts and dashboards.

    import umbral_viz as uv

    uv.use("matplotlib")                     # activate the theme
    c = uv.tokens.color("signal")            # never retype a hex
    frame = uv.Frame(title=..., subtitle=..., source=...)   # required, or it raises

Token values are vendored from `tokens/build/` at build time and verified
byte-identical in CI. Nothing here writes a colour, font or size as a literal.
"""
from . import chart, themes, tokens
from .chart import Frame, MissingSource, frame
from .tokens import color, font, ramp, series, version

__version__ = version()
__all__ = [
    "chart", "themes", "tokens",
    "Frame", "MissingSource", "frame",
    "color", "font", "ramp", "series", "version",
    "use",
]

_USE = {
    "matplotlib": lambda mode: themes.use_matplotlib(mode),
    "plotly": lambda mode: themes.use_plotly(mode),
    "altair": lambda mode: themes.use_altair(mode),
}


def use(library: str, mode: str = "laboratorio"):
    """Activate the Umbral theme for a plotting library.

    `mode` is `laboratorio` (light, the default) or `instrumento` (dark, for live
    dashboards and social cards).
    """
    if library not in _USE:
        raise ValueError(
            f"unknown library {library!r} — expected one of {', '.join(_USE)}")
    tokens._check_mode(mode)
    return _USE[library](mode)
