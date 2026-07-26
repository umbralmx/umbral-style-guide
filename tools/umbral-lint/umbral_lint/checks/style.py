"""Style checks: colour, type, layout. Mostly CSS and markup.

Every check parses declarations rather than matching substrings. Naive matching on
this codebase is close to useless — measured against `cabildo-libre`, the most
conformant product in the portfolio, plain greps produced eleven hits and all
eleven were false:

    "Inter"       ->  cursor: pointer
    "white"       ->  white-space: nowrap
    "gradient"    ->  linear-gradient(var(--u-gridline), var(--u-gridline)) drawing a rule
    "box-shadow"  ->  inset 4px 0 0 var(--u-signal), which is a rule, not a shadow
"""
from __future__ import annotations

import pathlib
import re

from ..context import (CSS_EXT, MARKUP_EXT, Context, code_lines, declarations,
                       is_token_file)

STYLEISH = CSS_EXT | MARKUP_EXT
BANNED_FAMILIES = {
    "inter", "roboto", "arial", "helvetica", "helvetica neue",
    "source sans", "source sans pro", "source sans 3", "open sans", "lato",
}
COLOUR_PROPS = {"color", "background", "background-color", "fill", "stroke",
                "border-color", "outline-color"}
FONT_CDNS = re.compile(
    r"fonts\.(googleapis|gstatic|bunny|cdnfonts)\.com|use\.typekit|fonts\.adobe\.com", re.I)
# Pictographic emoji only. U+2600–U+27BF holds ✓ ✗ → — which are legitimate table
# and prose marks, not decoration; matching them made the check useless on the
# audit's own conformance tables.
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F0FF]"
                   "|[\u2190-\u27BF]\uFE0F")
DISPLAY_SEL = re.compile(r"(^|[\s,{])(h[1-6]|\.display|\.title|\.hero|\[class\*=.title)")


def _px(value: str, unit: str) -> float:
    return float(value) * (16 if unit in ("rem", "em") else 1)


def _gradient_args(value: str) -> str | None:
    """Extract a gradient's arguments with balanced parens.

    `[^)]*` stops at the first `)`, which inside
    `linear-gradient(var(--u-gridline), var(--u-gridline))` is the one closing
    `var(` — leaving a truncated string that looks like two colour stops. That
    misread the single-colour gradient cabildo-libre uses to draw a 1px rule,
    which is precisely the false positive this linter exists to avoid.
    """
    m = re.search(r"(linear|radial|conic)-gradient\(", value)
    if not m:
        return None
    depth, start = 1, m.end()
    for i in range(start, len(value)):
        if value[i] == "(":
            depth += 1
        elif value[i] == ")":
            depth -= 1
            if depth == 0:
                return value[start:i]
    return value[start:]


# words that appear inside a gradient but are not colour stops
_GRADIENT_KEYWORDS = {
    "to", "deg", "turn", "rad", "grad", "at", "top", "bottom", "left", "right",
    "center", "circle", "ellipse", "closest", "farthest", "side", "corner",
    "in", "srgb", "oklch", "oklab", "hsl", "from", "transparent", "currentcolor",
}


def run(ctx: Context) -> None:
    _styles(ctx)
    _font_hosting(ctx)
    _emoji(ctx)


def _styles(ctx: Context) -> None:
    for p in ctx.files(STYLEISH):
        token_src = is_token_file(p)
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        lines = code_lines(text)

        for n, line in lines:
            low = line.lower()

            for prop, value in declarations(line):
                v = value.lower()

                # ── colour ────────────────────────────────────────────────
                if not token_src:
                    if prop in COLOUR_PROPS or prop.startswith("--"):
                        if re.search(r"(^|[\s,(])(#fff|#ffffff|#000|#000000)\b", v):
                            ctx.report("pure-black-white", p, n,
                                       f"{prop}: {value} — pure black or white",
                                       "var(--u-base) / var(--u-ink)")
                        if re.fullmatch(r"(white|black)", v.strip()):
                            ctx.report("pure-black-white", p, n,
                                       f"{prop}: {value} — pure black or white",
                                       "var(--u-base) / var(--u-ink)")
                    for hx in re.findall(r"#[0-9a-f]{6}\b", v):
                        if hx in ctx.token_hex:
                            ctx.report("hardcoded-token-hex", p, n,
                                       f"{hx} is the {ctx.token_hex[hx]} token, written by hand",
                                       f"var(--u-{ctx.token_hex[hx].split()[0]})")

                # ── gradients: a single-colour one draws a rule ───────────
                args = _gradient_args(v)
                if args is not None:
                    stops = set(re.findall(
                        r"var\(--[\w-]+\)|#[0-9a-f]{3,8}|rgba?\([^)]*\)|\b[a-z]{3,}\b", args))
                    stops -= _GRADIENT_KEYWORDS
                    if len(stops) > 1:
                        ctx.report("no-gradient", p, n,
                                   f"{prop}: gradient with {len(stops)} stops",
                                   "solid fills; a sequential ramp to encode intensity")

                # ── type ──────────────────────────────────────────────────
                if prop == "font-family":
                    for fam in v.split(","):
                        fam = fam.strip().strip("'\"")
                        if fam in BANNED_FAMILIES:
                            ctx.report("banned-font-family", p, n,
                                       f"font-family includes {fam!r}",
                                       "Space Grotesk / IBM Plex Sans / IBM Plex Mono")

                if prop == "font-weight":
                    m = re.match(r"(\d{3})|bold", v)
                    if m and (v.startswith("bold") or int(m.group(1) or 0) >= 700):
                        ctx.report("display-weight", p, n,
                                   f"font-weight: {value}",
                                   "display type is Space Grotesk 500; 600 for small labels")

                if prop == "font-size" and not token_src:
                    m = re.match(r"([\d.]+)(px|rem|em|pt)", v)
                    if m and m.group(2) != "pt" and _px(m.group(1), m.group(2)) < 12:
                        ctx.report("minimum-font-size", p, n,
                                   f"font-size: {value} — below the 12px web minimum",
                                   "12px is the floor; raise it or use a larger role")
                    if m and m.group(2) == "pt" and float(m.group(1)) < 11:
                        ctx.report("minimum-font-size", p, n,
                                   f"font-size: {value} — below the 11pt document minimum", "")

                if prop == "letter-spacing":
                    m = re.match(r"([\d.]+)(em|px)", v)
                    if m and float(m.group(1)) > 0 and DISPLAY_SEL.search(low):
                        ctx.report("display-tracking", p, n,
                                   f"positive tracking on display type: {value}",
                                   "var(--u-tracking-display), between -0.02 and -0.03em")

                # ── layout ────────────────────────────────────────────────
                if prop == "border-radius":
                    for num, unit in re.findall(r"([\d.]+)(px|rem|em|%)", v):
                        if unit == "%" or _px(num, unit) > 2:
                            ctx.report("radius-max", p, n,
                                       f"border-radius: {value}", "2px is the ceiling")
                            break

                if prop == "box-shadow" and "inset" not in v and v != "none":
                    ctx.report("no-drop-shadow", p, n, f"box-shadow: {value}",
                               "1px rules do the structural work; inset shadows are rules")

                if prop in ("max-width", "width") and not token_src:
                    m = re.match(r"([\d.]+)ch", v)
                    if m and float(m.group(1)) > 65:
                        ctx.report("measure-max", p, n,
                                   f"{prop}: {value} — measure above 65ch",
                                   "var(--u-measure)")

                if prop in ("padding", "margin", "gap", "row-gap", "column-gap") \
                        and not token_src:
                    for num, unit in re.findall(r"\b([\d.]+)(px)\b", v):
                        n_ = float(num)
                        # 1px and 2px are rules and radii, not spacing
                        if n_ > 2 and n_ % 8 != 0:
                            ctx.report("spacing-scale", p, n,
                                       f"{prop}: {value} — {num}px is not a multiple of 8",
                                       "var(--u-space-1) … var(--u-space-10)")
                            break

            # ── accessibility, whole-line ─────────────────────────────────
            if re.search(r"outline\s*:\s*(none|0)\b", low) and ":focus" not in low:
                ctx.report("focus-and-target", p, n, "outline removed",
                           ":focus-visible outline in signal")

        # ── file-level CSS checks ─────────────────────────────────────────
        if p.suffix in CSS_EXT:
            if re.search(r"\b(transition|animation)\s*:", text) \
                    and "prefers-reduced-motion" not in text:
                ctx.report("reduced-motion", p, 1,
                           "animation or transition with no prefers-reduced-motion block",
                           "@media (prefers-reduced-motion: reduce) { transition: none }")


def _font_hosting(ctx: Context) -> None:
    for p in ctx.files():
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for n, line in code_lines(text):
            if FONT_CDNS.search(line):
                ctx.report("font-hosting", p, n, "font served from a CDN",
                           "self-host to assets/fonts/ — a data product must work "
                           "offline and must not leak reader IPs")


def _emoji(ctx: Context) -> None:
    for p in ctx.files():
        if is_token_file(p):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            m = EMOJI.search(line)
            if m:
                ctx.report("no-emoji", p, n, f"emoji {m.group()!r}",
                           "the numbers carry the argument")
                break  # one per file is enough to make the point


def hardcoded_values(ctx: Context) -> None:
    """UMB-PRO-003 — any value that exists as a token, outside the token files."""
    fams = ctx.font_families
    for p in ctx.files(CSS_EXT | MARKUP_EXT | {".py", ".r", ".js", ".mjs", ".ts"}):
        if is_token_file(p):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for n, line in code_lines(text):
            low = line.lower()
            # a token font family written as a literal, outside a font-family stack
            for fam in fams:
                if fam and fam in low and "font-family" not in low and "@font-face" not in low:
                    if re.search(rf"['\"]{re.escape(fam)}['\"]", low):
                        ctx.report("hardcoded-value", p, n,
                                   f"font family {fam!r} written as a literal",
                                   "import it from tokens/build/")
                        break
            for hx in re.findall(r"#[0-9a-f]{6}\b", low):
                if hx in ctx.token_hex:
                    ctx.report("hardcoded-value", p, n,
                               f"{hx} is the {ctx.token_hex[hx]} token, written by hand",
                               "import it from tokens/build/")
                    break


def register() -> dict:
    return {"style": run, "hardcoded": hardcoded_values}


__all__ = ["run", "hardcoded_values", "register", "pathlib"]
