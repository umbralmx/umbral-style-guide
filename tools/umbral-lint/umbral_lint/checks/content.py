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
# 2.0: the access date travels with the chart; the snapshot tag lives on the page
# (UMB-DAT-002), so either form still satisfies the check.
SNAPSHOT = re.compile(
    r"consulta\s+realizada\s+el\s+\d{4}-\d{2}|consultado\s+\d{4}-\d{2}"
    r"|\b[a-z][\w-]*-\d{4}-\d{2}\b", re.I)

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

# ── UMB-VOZ-005: one statement per sentence, 25 words maximum ─────────────
# ASD-STE100 caps an instruction at 20 words and a description at 25. Prose is
# measured against the looser cap, because the tighter one belongs to procedures.
#
# Only prose is measured. A table row, a code fence, a URL and a front-matter
# block are not sentences, and counting them made the check report the type
# scale and the contrast matrix — 60 findings, none of them writing.
SENTENCE_WORDS_MAX = 25
_SENTENCE_SPLIT = re.compile(r'''(?<=[.!?])\s+(?=[«"'(\[]?[A-ZÁÉÍÓÚÑ¿¡])''')
_INLINE_CODE = re.compile(r"`[^`]*`")
_MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_MD_MARKUP = re.compile(r"[*_>#|]+")
_SKIP_LINE = re.compile(
    # tables, fences, divs, includes, comments, bare URLs, checklist items, raw HTML
    r"^\s*(\||```|~~~|:::|\{\{<|<!--|<[a-z/!]|https?://|[-*+]\s*\[[ x]\]|\d+\.\s*\[[ x]\])"
    # A bolded lead-in whose colon sits inside the bold is a field, not a sentence:
    # «- **Origen:** https://…». A bullet that opens with a bolded *statement*
    # («- **El titular se sostiene.** Dice un rango…») keeps its colon outside, so
    # it is still measured — which is right, because it is prose.
    r"|^\s*[-*+]\s*\*\*[^*\n]*:\*\*"
    # a bare YAML-ish key at the start of a line
    r"|^\s*[-*+]?\s*(do|dont|title|title_en|rationale|check|note|evidence)\s*:")


_LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s")


def _prose_paragraphs(text: str):
    """Yield (line_no, paragraph) for prose only.

    Fenced blocks, front matter, tables, headings and directives are dropped
    whole. Everything left is something a person reads as a sentence.

    Each list item starts its own paragraph. Joined into one buffer, three
    one-line bullets read as a single 30-word sentence, which is the wrong
    reading and the wrong finding.
    """
    lines = text.splitlines()
    out, buf, start, fenced, front = [], [], 0, False, False
    if lines and lines[0].strip() == "---":
        front = True
    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if front:
            if i > 1 and stripped == "---":
                front = False
            continue
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        if not stripped or stripped.startswith("#") or _SKIP_LINE.search(raw):
            if buf:
                out.append((start, " ".join(buf)))
                buf = []
            continue
        if _LIST_ITEM.match(raw) and buf:
            out.append((start, " ".join(buf)))
            buf = []
        if not buf:
            start = i
        buf.append(_LIST_ITEM.sub("", stripped, count=1))
    if buf:
        out.append((start, " ".join(buf)))
    return out


def _sentences(paragraph: str):
    """Split a paragraph into sentences, with markup reduced first.

    An inline code span becomes a single capitalised placeholder rather than
    disappearing. It names one referent, so it counts as one word — and blanking
    it instead hides the sentence boundary in «…first time. `theme: none` makes
    Quarto…», which then reads as one 33-word sentence.
    """
    p = _MD_LINK.sub(r"\1", paragraph)
    p = _INLINE_CODE.sub("X", p)
    p = _MD_MARKUP.sub(" ", p)
    return [s.strip() for s in _SENTENCE_SPLIT.split(p) if s.strip()]


# UMB-VOZ-005 states three exceptions, and these are the two a path can decide.
# Third-party licence text is reproduced verbatim as a legal obligation. An accepted
# ADR is frozen by docs/adr/README.md — the rule binds new ADRs, not the record of a
# decision already made. The third exception, a direct quotation, is a judgement and
# is suppressed inline where it occurs.
_FROZEN_FILE = re.compile(
    r"(^|/)(LICEN[CS]E|COPYING|NOTICE|OFL)[\w.-]*$"
    r"|(^|/)docs/adr/\d{4}-", re.I)


def _long_sentences(ctx: Context) -> None:
    for p in ctx.files({".md", ".qmd", ".rmd", ".txt"}):
        if is_token_file(p) or _FROZEN_FILE.search(p.as_posix()):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for line, para in _prose_paragraphs(text):
            for sentence in _sentences(para):
                # «a · b · c» is a list set on one line, not a sentence
                if sentence.count("·") >= 2:
                    continue
                words = sentence.split()
                if len(words) > SENTENCE_WORDS_MAX:
                    ctx.report("long-sentence", p, line,
                               f"{len(words)} words in one sentence: "
                               f"«{' '.join(words[:8])}…»",
                               f"split it; {SENTENCE_WORDS_MAX} words is the ceiling")


def run(ctx: Context) -> None:
    _markup(ctx)
    _charts(ctx)
    _prose(ctx)
    _long_sentences(ctx)


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
                           "Fuente: Elaboración propia con datos de ORIGEN. "
                           "Consulta realizada el AAAA-MM-DD. — and umbral.org.mx on the right")

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
                           "source line names no access date",
                           "add «Consulta realizada el AAAA-MM-DD»; the snapshot tag "
                           "goes on the page, not here (UMB-DAT-002)")


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
