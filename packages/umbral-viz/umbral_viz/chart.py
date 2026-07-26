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

_SNAPSHOT = re.compile(r"consultado\s+\d{4}-\d{2}|\b[a-z][\w-]*-\d{4}-\d{2}\b", re.I)
_LICENCE = re.compile(r"CC BY|MIT|dominio p[úu]blico", re.I)


class MissingSource(ValueError):
    """A chart without its source does not ship (UMB-CHT-003)."""


@dataclass
class Frame:
    """The text frame every Umbral chart carries.

    >>> f = Frame(
    ...     title="El RNPDNO acumula 351,057 registros con hechos entre 2010-01 y 2026-07",
    ...     subtitle="México · registros por mes de la fecha de hechos",
    ...     source="RNPDNO (CNB/SEGOB)",
    ...     accessed="2026-07-09",
    ...     snapshot="rnpdno-2026-07",
    ... )
    >>> f.source_line()
    'Fuente: RNPDNO (CNB/SEGOB) · consultado 2026-07-09 · rnpdno-2026-07 · umbral.mx · datos CC BY 4.0'
    """

    title: str
    subtitle: str
    source: str
    accessed: str = ""
    snapshot: str = ""
    licence: str = "CC BY 4.0"
    site: str = "umbral.mx"
    strict: bool = True

    def __post_init__(self) -> None:
        if not self.source or not self.source.strip():
            raise MissingSource(
                "a chart needs its source (UMB-CHT-003). Pass source=, and ideally "
                "accessed= and snapshot= — the RNPDNO's counts change between queries, "
                "so a chart without a snapshot tag cannot be reconciled later.")
        if not self.title.strip():
            raise ValueError("a chart title states the finding as a sentence (UMB-CHT-001)")
        if self.strict and not self.subtitle.strip():
            raise ValueError(
                "a chart needs a subtitle with geography, period and unit (UMB-CHT-002). "
                "Pass strict=False only for a deliberately bare figure.")

    # ── rendering ─────────────────────────────────────────────────────────
    # umbral-lint: ignore[snapshot-tag] — the line below is assembled, not quoted
    def source_line(self) -> str:
        parts = [f"Fuente: {self.source.strip()}"]
        if self.accessed:
            parts.append(f"consultado {self.accessed}")
        if self.snapshot:
            parts.append(self.snapshot)
        parts += [self.site, f"datos {self.licence}"]
        return " · ".join(parts)

    def warnings(self) -> list[str]:
        """Non-fatal gaps worth surfacing in review."""
        out = []
        line = self.source_line()
        if not _SNAPSHOT.search(line):
            out.append("source line names no access date or snapshot tag (UMB-DAT-002)")
        if not _LICENCE.search(line):
            out.append("source line names no licence (UMB-DAT-004)")
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
