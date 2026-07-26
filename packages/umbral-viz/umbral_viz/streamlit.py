# umbral-lint: ignore-file[chart-source-present] — every chart here renders a
# caller-supplied Frame, which cannot be constructed without a source (UMB-CHT-003).
"""Streamlit helpers.

Two of Umbral's four products are Streamlit apps, and the Phase 0 audit found the
same three defects in both: `lang="en"`, KPI figures in the wrong family, and — on
one of them — no CSV download anywhere. These helpers make the correct version the
short one.

Import is lazy: `import umbral_viz` must work in a notebook with no Streamlit
installed.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from . import tokens
from .chart import Frame


def _st():
    try:
        import streamlit as st
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "umbral_viz.streamlit needs Streamlit: pip install streamlit") from exc
    return st


def install_config(target: str | Path = ".streamlit/config.toml") -> Path:
    """Copy the generated theme config into the app.

    Do not retype the keys. The v1.0 brand book rendered them as
    `sc-camel-primary-color` (a PDF-export artifact) and set `font = "sans serif"`,
    which is a valid Streamlit value meaning Streamlit's own Source Sans — and is
    why pautamx renders Source Sans today.
    """
    dest = Path(target)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(tokens.streamlit_config_path(), dest)
    return dest


def set_lang(lang: str = "es") -> None:
    """Fix the document language (UMB-A11Y-001).

    Streamlit hardcodes `lang="en"` and does not expose it, so a Spanish dashboard
    is read aloud with English phonetics until this runs. One call, at the top.
    """
    st = _st()
    import streamlit.components.v1 as components

    components.html(
        f"<script>window.parent.document.documentElement.lang='{lang}';</script>",
        height=0)
    del st


def apply_fonts(mode: str = "instrumento") -> None:
    """Inject the display/mono rules Streamlit's theme cannot express."""
    st = _st()
    t = tokens.tokens(mode)
    st.markdown(
        f"""<style>
h1, h2, h3 {{
  font-family: '{tokens.font("display")}', system-ui, sans-serif;
  font-weight: {tokens.all_tokens()["font"]["displayWeight"]};
  letter-spacing: {tokens.all_tokens()["font"]["displayTracking"]};
}}
[data-testid="stMetricValue"] {{
  font-family: '{tokens.font("mono")}', ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
}}
[data-testid="stMetricLabel"] {{
  font-family: '{tokens.font("mono")}', ui-monospace, monospace;
  text-transform: uppercase; letter-spacing: .04em;
  color: {t["caption"]};
}}
</style>""",
        unsafe_allow_html=True)


def kpi(label: str, value, delta: str | None = None,
        delta_good: bool | None = None, mode: str = "instrumento") -> None:
    """A KPI tile.

    The figure renders in Plex Mono, because a KPI row is compared digit-by-digit
    across tiles (UMB-TYP-004). `delta_good` is required when a delta is shown:
    whether a rise is good depends on the metric, never on the sign.
    """
    st = _st()
    if delta is not None and delta_good is None:
        raise ValueError(
            "pass delta_good=True/False — colouring a delta by its sign assumes "
            "that up is good, which is false for disappearances and for crime")
    st.metric(label, value, delta,
              delta_color="normal" if delta_good else "inverse")
    del mode


def csv_button(df, filename: str, label: str = "Descargar CSV") -> None:
    """The download every chart ships (UMB-A11Y-004)."""
    st = _st()
    st.download_button(label, df.to_csv(index=False).encode("utf-8"),
                       filename, "text/csv")


def chart(fig, frame: Frame, df=None, filename: str | None = None,
          show_table: bool = True) -> None:
    """Render a chart with its full frame, table and CSV.

    Everything UMB-CHT-001/002/003 and UMB-A11Y-002/003/004 require, in one call,
    so the conformant version is less work than the non-conformant one.
    """
    st = _st()
    st.markdown(f"#### {frame.title}")
    if frame.subtitle:
        st.caption(frame.subtitle)

    try:
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": False})
    except Exception:                                    # noqa: BLE001
        st.pyplot(fig)

    st.caption(frame.source_line())

    if df is not None:
        if show_table:
            with st.expander("Ver los datos"):
                st.dataframe(df, use_container_width=True)
        csv_button(df, filename or "datos.csv")


def panel(title: str | None = None):
    """A bordered panel — `panel` fill, 1px border, no shadow."""
    st = _st()
    box = st.container(border=True)
    if title:
        box.markdown(f"**{title}**")
    return box
