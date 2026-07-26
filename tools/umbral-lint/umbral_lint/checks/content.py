"""Content checks: markup accessibility, charts, prose, terminology.

The terminology check is the one that matters most. Umbral publishes on
disappearances, and the difference between «persona desaparecida» and «persona no
localizada» is legal and ethical, not stylistic — so the banned terms are checked
literally, from the glossary, rather than left to review.
"""
from __future__ import annotations

import re

from ..context import (CODE_EXT, MARKUP_EXT, TEXT_EXT, Context, code_lines,
                       is_token_file)

# Charts, in the libraries Umbral actually uses
PLOT_CALL = re.compile(
    r"\b(plt\.(plot|bar|barh|scatter|fill_between|stackplot)|ax\.(plot|bar|barh|scatter)"
    r"|go\.(Figure|Scatter|Bar)|px\.\w+|Plot\.plot|alt\.Chart|ggplot|st\.(line|bar|area)_chart"
    r"|st\.(plotly|altair|pyplot|vega_lite)_chart)\s*\(")
SOURCE_LINE = re.compile(r"Fuente\s*:", re.I)
SNAPSHOT = re.compile(r"consultado\s+\d{4}-\d{2}|\b[a-z][\w-]*-\d{4}-\d{2}\b", re.I)

BANNED_CHARTS = re.compile(
    r"\b(px\.pie|go\.Pie|plt\.pie|ax\.pie|\.pie\s*\(|type\s*=\s*['\"]pie['\"]"
    r"|mark_arc|go\.Surface|go\.Scatter3d|projection\s*=\s*['\"]3d['\"]"
    r"|twinx\s*\(\s*\)|twiny\s*\(\s*\)|secondary_y\s*=\s*True)")

HYPE = re.compile(
    r"\b(revolucionari[oa]s?|disruptiv[oa]s?|game[- ]chang\w*|impresionante|"
    r"alarmante|escandalos[oa]s?|brutal(?:es)?|dispararon|explotaron|"
    r"increíble|espectacular)\b", re.I)

# From guide/15-terminologia.md — the «Nunca» column.
NEVER_TERMS = {
    r"\blevant[óo]n(?:es)?\b": "coloquialismo que normaliza el hecho y presupone móvil criminal",
    r"\bajuste de cuentas\b": "presupone que la víctima participaba en actividad criminal",
    r"\bsicarios?\b": "vocabulario de la narrativa criminal; atribuye pertenencia sin evidencia",
    r"\bejecutad[oa]s?\b": "vocabulario de la narrativa criminal",
    r"\bguerra contra el narco\b": "marco político, no descripción",
    r"\bindigentes?\b": "usar «persona en situación de calle»",
    r"\bminusválid[oa]s?\b": "usar «persona con discapacidad»",
    r"\bdiscapacitad[oa]s?\b": "usar «persona con discapacidad»",
    r"\bilegales?\b(?=[^.]{0,40}\b(migrante|persona|trabajador))":
        "ninguna persona es ilegal; usar «persona migrante»",
}
# Prefer person-first phrasing; flagged only as the bare noun.
PREFER = {
    # Not after «persona(s)», and not inside the RNPDNO's own name.
    r"(?<!persona )(?<!personas )(?<!Personas )\bdesaparecid[oa]s\b":
        "«personas desaparecidas» — persona primero",
    r"\bmenores\b(?!\s+de\s+edad\s+que)": "«niñas, niños y adolescentes» (NNA)",
}

# TODO and FIXME are matched case-SENSITIVELY. Lower-cased, «todo» is the ordinary
# Spanish word for "all" and appears in almost every paragraph of the guide — an
# earlier version of this pattern reported 40 false positives on Spanish prose.
PLACEHOLDER = re.compile(
    r"\bLorem ipsum\b|\blorem ipsum\b|\bTODO\b|\bFIXME\b|\bXXX\b"
    r"|>\s*(foto|imagen|placeholder)\s*<"
    r"|\bplaceholder (text|content|copy|image)\b")


def run(ctx: Context) -> None:
    _markup(ctx)
    _charts(ctx)
    _prose(ctx)


def _markup(ctx: Context) -> None:
    for p in ctx.files(MARKUP_EXT):
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue

        if p.suffix in (".html", ".htm"):
            m = re.search(r"<html[^>]*\blang\s*=\s*[\"']([^\"']+)", text, re.I)
            spanish = re.search(r"[áéíóúñ¿¡]|\b(el|la|los|las|de|para|con)\b", text, re.I)
            if not m:
                ctx.report("lang-attribute", p, 1, "no lang attribute on <html>",
                           'lang="es"')
            elif m.group(1).lower().startswith("en") and spanish:
                ctx.report("lang-attribute", p, 1,
                           f'lang="{m.group(1)}" on Spanish content', 'lang="es"')

        # figures and charts need a label carrying the finding
        for m in re.finditer(r"<(svg|canvas|figure)\b([^>]*)>", text, re.I):
            attrs = m.group(2)
            line = text[:m.start()].count("\n") + 1
            if re.search(r'aria-hidden\s*=\s*["\']true', attrs, re.I):
                continue
            if not re.search(r'aria-label\s*=\s*["\'][^"\']{12,}', attrs, re.I) \
                    and not re.search(r"aria-labelledby", attrs, re.I):
                ctx.report("chart-aria-label", p, line,
                           f"<{m.group(1)}> with no aria-label carrying the finding",
                           'aria-label with the same claim as the title')


def _charts(ctx: Context) -> None:
    for p in ctx.files(CODE_EXT | {".qmd", ".rmd", ".md"}):
        if is_token_file(p):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue

        first = PLOT_CALL.search(text)
        if first:
            line = text[:first.start()].count("\n") + 1
            if not SOURCE_LINE.search(text):
                ctx.report("chart-source-present", p, line,
                           "chart code with no «Fuente:» line anywhere in the file",
                           "Fuente: ORIGEN · consultado FECHA · SNAPSHOT · umbral.mx · CC BY 4.0")

        for n, line in code_lines(text):
            m = BANNED_CHARTS.search(line)
            if m:
                ctx.report("banned-chart-type", p, n,
                           f"banned chart construct: {m.group().strip()}",
                           "bars for composition, two panels for two units")

        # a source line that names no snapshot
        for n, line in enumerate(text.splitlines(), 1):
            if SOURCE_LINE.search(line) and not SNAPSHOT.search(line):
                ctx.report("snapshot-tag", p, n,
                           "source line names no access date or snapshot tag",
                           "add «consultado AAAA-MM-DD» and the snapshot tag")


def _prose(ctx: Context) -> None:
    for p in ctx.files(TEXT_EXT | MARKUP_EXT | CODE_EXT):
        if is_token_file(p):
            continue
        rel = p.as_posix()
        # the guide and the audit quote banned terms in order to ban them
        documents_terms = ("guide/15-terminologia" in rel or "/audit/" in rel
                           or "umbral-lint" in rel or "rules/rules" in rel
                           or "skills/umbral-brand/references/terminology" in rel)
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue

        for n, line in enumerate(text.splitlines(), 1):
            if PLACEHOLDER.search(line):
                ctx.report("placeholder-content", p, n,
                           f"placeholder content: {PLACEHOLDER.search(line).group().strip()}",
                           "publish the section when its copy exists")

            m = HYPE.search(line)
            if m and not documents_terms:
                ctx.report("hype-language", p, n, f"hype word {m.group()!r}",
                           "quantify instead")

            # numbers and dates
            if re.search(r"\b\d+([.,]\d+)?\s+%", line):
                ctx.report("percent-spacing", p, n, "space before %", "9.2%, tight")
            dm = re.search(r"\b(\d{2})/(\d{2})/(\d{4})\b", line)
            if dm:
                ctx.report("date-format", p, n,
                           f"ambiguous date {dm.group()}",
                           "ISO in data (2026-07-09), prose in text (9 de julio de 2026)")

            if documents_terms:
                continue
            for pat, why in NEVER_TERMS.items():
                tm = re.search(pat, line, re.I)
                if tm:
                    ctx.report("terminology", p, n,
                               f"«{tm.group().strip()}» — {why}",
                               "see guide/15-terminologia.md")
            for pat, why in PREFER.items():
                tm = re.search(pat, line, re.I)
                if tm:
                    ctx.report("terminology", p, n,
                               f"«{tm.group().strip()}» — prefer {why}",
                               "see guide/15-terminologia.md")


def register() -> dict:
    return {"content": run}
