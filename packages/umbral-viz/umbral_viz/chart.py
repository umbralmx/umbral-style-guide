"""The chart frame: finding-title, subtitle, source line.

The v1.0 engineering doc asked for this and nobody built it:

    "Every chart component takes required title, subtitle, source props and renders
     the title/subtitle/source frame around the plot. A chart with no source should
     throw in dev."

So `Frame` refuses to construct without a source. That is deliberate — the Phase 0
audit found three of five charts on one dashboard with no source line, and a chart
circulates without its page the moment someone screenshots it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import tokens

_ACCESSED = re.compile(r"\d{4}-\d{2}-\d{2}")
_BUILT = re.compile(r"acumulad|total|tasa|promedio|mediana|cambio|porcentaje|suma|\d{4}", re.I)


class MissingSource(ValueError):
    """A chart without its source does not ship (UMB-CHT-003)."""


@dataclass
class Frame:
    """The text frame every Umbral chart carries.

    >>> f = Frame(
    ...     title="El RNPDNO acumula 351,057 registros con hechos entre 2010-01 y 2026-07",
    ...     subtitle="Suma acumulada de personas desaparecidas por estado, 2021-2026",
    ...     source="Elaboración propia con datos del RNPDNO (CNB/SEGOB)",
    ...     accessed="2026-07-20",
    ... )
    >>> f.source_line()
    'Fuente: Elaboración propia con datos del RNPDNO (CNB/SEGOB). Consulta realizada el 2026-07-20.'
    >>> f.site_line()
    'umbral.org.mx'
    """

    title: str
    subtitle: str
    source: str
    accessed: str = ""
    site: str = "umbral.org.mx"
    strict: bool = True

    def __post_init__(self) -> None:
        if not self.source or not self.source.strip():
            raise MissingSource(
                "a chart needs its source (UMB-CHT-003). Pass source= and accessed= — "
                "the RNPDNO's counts change between queries, so a chart with no access "
                "date cannot be reconciled later. The snapshot tag and the licence "
                "belong on the page (UMB-DAT-002, UMB-DAT-004), not on this line.")
        if not self.title.strip():
            raise ValueError("a chart title states the finding as a sentence (UMB-CHT-001)")
        if self.strict and not self.subtitle.strip():
            raise ValueError(
                "a chart subtitle says how the figure is built — the transformation, "
                "the unit, the scope and the period (UMB-CHT-002). «Suma acumulada de "
                "personas desaparecidas por estado, 2021-2026». Pass strict=False only "
                "for a deliberately bare figure.")

    # ── rendering ─────────────────────────────────────────────────────────
    def source_line(self) -> str:
        """The left half: where the data came from, and when it was read.

        The licence and the snapshot tag are deliberately absent. They live on the
        page (UMB-DAT-004, UMB-DAT-002). A five-field line does not survive a social
        card or a slide, which is what 2.0 fixed.
        """
        # umbral-lint: ignore[snapshot-tag] — assembled here, not quoted
        origin = self.source.strip().rstrip(".")
        line = f"Fuente: {origin}."
        if self.accessed:
            line += f" Consulta realizada el {self.accessed}."
        return line

    def site_line(self) -> str:
        """The right half: the attribution, read at a glance."""
        return self.site.strip()

    def warnings(self) -> list[str]:
        """Non-fatal gaps worth surfacing in review."""
        out = []
        if not _ACCESSED.search(self.accessed):
            out.append('no ISO access date; pass accessed="2026-07-20" (UMB-CHT-003)')
        if not _BUILT.search(self.subtitle or ""):
            out.append("the subtitle names no transformation and no period (UMB-CHT-002)")
        if self.title.rstrip().endswith("."):
            out.append("chart titles carry no full stop")
        if len(self.title.split()) < 4:
            out.append("the title looks like a topic, not a finding (UMB-CHT-001)")
        return out

    def aria_label(self) -> str:
        """The label carries the finding, not the chart type (UMB-A11Y-002)."""
        return self.title.strip()

    # ── matplotlib ────────────────────────────────────────────────────────
    def apply_matplotlib(self, fig, ax, mode: str = "laboratorio"):
        """Draw the frame onto a matplotlib figure."""
        t = tokens.tokens(mode)
        # The title sits above the subtitle, which sits above the axes. Padding the
        # title by the subtitle's height is what stops the two overlapping.
        pad = 26 if self.subtitle else 10
        ax.set_title(self.title, loc="left", pad=pad,
                     fontfamily=tokens.font("display"), fontsize=16, color=t["ink"])
        if self.subtitle:
            ax.text(0, 1.015, self.subtitle, transform=ax.transAxes,
                    fontfamily=tokens.font("body"), fontsize=11, color=t["muted"],
                    va="bottom", ha="left")
        fig.text(0.01, -0.02, self.source_line(),
                 fontfamily=tokens.font("mono"), fontsize=9, color=t["caption"])
        return fig

    # ── plain text / markdown, for Streamlit and Quarto ───────────────────
    def as_markdown(self) -> str:
        return (f"### {self.title}\n\n"
                f"{self.subtitle}\n\n"
                f"`{self.source_line()}`\n")


def frame(title: str, subtitle: str, source: str, **kw) -> Frame:
    """Convenience constructor. Same requirements as `Frame`."""
    return Frame(title=title, subtitle=subtitle, source=source, **kw)
