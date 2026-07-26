"""Token access. Everything else in this package reads values from here.

No module in `umbral_viz` may write a colour, font or size as a literal. The values
live in `_data/`, vendored byte-identically from `tokens/build/` at build time and
checked by `tools/verify_packages.py`.
"""
from __future__ import annotations

import functools
import json
import pathlib

DATA = pathlib.Path(__file__).parent / "_data"
MODES = ("laboratorio", "instrumento")


class UnknownMode(ValueError):
    """Raised instead of returning None for a mode that does not exist."""


@functools.lru_cache(maxsize=None)
def _load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def all_tokens() -> dict:
    """The whole generated token set."""
    return _load("tokens.json")


def version() -> str:
    """The design-system version these tokens came from."""
    return _load("rules.json")["version"]


def _check_mode(mode: str) -> str:
    if mode not in MODES:
        raise UnknownMode(
            f"unknown Umbral mode {mode!r} — expected one of {', '.join(MODES)}")
    return mode


def tokens(mode: str = "laboratorio") -> dict:
    """Semantic tokens for one mode.

    The doctest asserts a property rather than the value: pinning the hex here would
    make this a second place the value lives, and a token change is a major bump.

    >>> tokens()["signal"].startswith("#")
    True
    """
    return all_tokens()["mode"][_check_mode(mode)]


def color(name: str, mode: str = "laboratorio") -> str:
    """One semantic colour. Raises if the token does not exist."""
    t = tokens(mode)
    if name not in t or not isinstance(t[name], str):
        known = ", ".join(k for k, v in t.items() if isinstance(v, str))
        raise KeyError(f"no Umbral token {name!r} in modo {mode}. Known: {known}")
    return t[name]


def series(mode: str = "laboratorio", n: int | None = None) -> list[str]:
    """The categorical palette, in order.

    The first entry is the highlighted series; the rest step down. Asking for more
    than five raises — UMB-CHT-006 says a chart needing more than five series is
    two charts.
    """
    pal = tokens(mode)["series"]
    if n is None:
        return list(pal)
    if n > 5:
        raise ValueError(
            f"{n} series requested; the maximum is 5 (UMB-CHT-006). "
            "Use two charts, or group the tail into «otros».")
    return list(pal[:n])


def ramp(kind: str = "sequential_signal", mode: str = "laboratorio") -> list[str]:
    """A colour ramp.

    `kind` is one of sequential_signal, sequential_model, diverging.
    """
    ramps = all_tokens()["ramp"][_check_mode(mode)]
    if kind not in ramps:
        raise KeyError(f"no ramp {kind!r}. Known: {', '.join(ramps)}")
    return list(ramps[kind])


def font(role: str = "body") -> str:
    """A font family: display, body or mono."""
    f = all_tokens()["font"]
    key = {"display": "display", "body": "body", "mono": "mono"}.get(role)
    if key is None:
        raise KeyError(f"no font role {role!r} — expected display, body or mono")
    return f[key]


def uncertainty_opacity() -> float:
    """Opacity for a projection or confidence band (UMB-CHT-011)."""
    return all_tokens()["uncertaintyBandOpacity"]


def contrast_report() -> dict:
    """The generated contrast matrix, as shipped."""
    return _load("contrast.json")


def rules() -> dict:
    """The rule set, machine-readable."""
    return _load("rules.json")


def style_path(mode: str = "laboratorio") -> pathlib.Path:
    """Path to the matplotlib style file for a mode."""
    return DATA / f"umbral-{_check_mode(mode)}.mplstyle"


def plotly_template_path(mode: str = "laboratorio") -> pathlib.Path:
    return DATA / f"plotly-umbral-{_check_mode(mode)}.json"


def streamlit_config_path() -> pathlib.Path:
    """The generated .streamlit/config.toml. Copy it; do not retype the keys."""
    return DATA / "streamlit-config.toml"
