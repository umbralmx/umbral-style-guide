"""Check registry.

`IMPLEMENTED` is the contract between this tool and `rules/rules.yaml`. A rule that
claims `check: {type: automated, tool: umbral-lint, id: X}` must have X here, and
every X here must be claimed by exactly one rule. `tools/verify_lint.py` enforces
both directions, so the rule set cannot promise a check that does not run.

That reconciliation is the whole reason 14 rules were moved from `automated` to
`review` in v1.1: they named checks nobody had written.
"""
from __future__ import annotations

from ..context import Context
from . import content, repo, style

# check id -> one-line description of what it actually detects
IMPLEMENTED: dict[str, str] = {
    # colour
    "pure-black-white": "pure #fff/#000/white/black as a colour value",
    "hardcoded-token-hex": "a hex that is already a semantic token",
    "hardcoded-value": "any token value written as a literal outside tokens/",
    "no-gradient": "a gradient with more than one colour stop",
    # type
    "banned-font-family": "a non-approved family as a stack entry",
    "display-weight": "font-weight 700 or heavier",
    "minimum-font-size": "font-size below 12px / 11pt",
    "font-hosting": "a font loaded from a CDN",
    "display-tracking": "positive tracking on display type",
    # layout
    "radius-max": "border-radius above 2px",
    "no-drop-shadow": "a box-shadow that is not inset",
    "measure-max": "a measure above 65ch",
    "spacing-scale": "padding/margin/gap off the 8px scale",
    "no-emoji": "emoji",
    # charts
    "chart-source-present": "chart code with no source line",
    "banned-chart-type": "pie, 3D or dual-axis constructs",
    "snapshot-tag": "a source line naming no access date or snapshot",
    # voice, numbers, terminology
    "placeholder-content": "lorem ipsum, TODO, FIXME, placeholder",
    "hype-language": "hype words",
    "long-sentence": "a sentence above 25 words in prose",
    "percent-spacing": "a space before %",
    "date-format": "an ambiguous dd/mm/yyyy date",
    "terminology": "a term the glossary bans or replaces",
    # accessibility
    "lang-attribute": "a missing or wrong lang attribute",
    "chart-aria-label": "a figure with no aria-label carrying the finding",
    "focus-and-target": "outline removed without a focus-visible replacement",
    "reduced-motion": "animation with no prefers-reduced-motion block",
    # data and process
    "source-md-present": "a dataset directory with no SOURCE.md",
    "license-present": "missing LICENSE-CODE / LICENSE-CONTENT",
    "generated-file-edited": "a generated file with uncommitted hand edits",
}


def run_all(ctx: Context) -> None:
    style.run(ctx)
    style.hardcoded_values(ctx)
    content.run(ctx)
    repo.run(ctx)
