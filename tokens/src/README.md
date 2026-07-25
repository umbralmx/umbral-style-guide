# `tokens/src/` — the authored layer

**This is the only place in the repository where a colour, font, or spacing value is authored.**
Everything in `tokens/build/` is generated from these files by `npm run build:tokens`. Never edit a
generated file; change the source and rebuild. See [ADR-0001](../../docs/adr/0001-token-architecture.md).

| File | Holds |
|---|---|
| `primitive.color.tokens.json` | Raw palette. Each value records the OKLCH coordinates it was derived at. |
| `semantic.color.tokens.json` | The two modes. References primitives, never literals. Declares `contrastRole`. |
| `type.tokens.json` | Families, weights, tracking, the size scale, and the hard minimums. |
| `space.tokens.json` | Spacing scale, rules, radius ceiling, measure, touch target. |
| `ramp.tokens.json` | Sequential and diverging ramps, authored as **derivation specs**. |

## The rules the build enforces

1. **A hex may be authored once.** `verify_tokens.py` fails if the same value appears in two source
   files. Semantic tokens must reference primitives. This is the mechanical fix for the v1.0 failure
   where the mplstyle and the brand book disagreed about the third series colour.
2. **Every token declares a `contrastRole`**, and the CI gate reads it:
   `text` → 4.5:1 · `mark` → 3:1 · `furniture` → exempt with a written rationale · `surface` → a
   background. The exemption is never inherited; a new token has to claim it explicitly.
3. **Ramps are specs, not lists.** You author lightness/chroma endpoints and a hue; the build
   expands the steps in OKLCH. A ramp can therefore be re-derived if a background changes.

## How the corrected tokens were derived

Every correction holds **hue fixed** and moves lightness, reducing chroma only where the target left
sRGB gamut — so a corrected token stays recognisably the same colour. The derivation is in
`audit/scripts/derive.py`; the measurements that motivated it are in
[`audit/2026-07-conformance.md`](../../audit/2026-07-conformance.md).

| Token | v1.0 | Now | Why |
|---|---|---|---|
| `caption` (light) | `#9AA19B` 2.37:1 | `#6C706D` 4.52:1 | Worst failure in the system. |
| `muted` (light) | `#6E756F` 4.25:1 | `#565D57` 6.09:1 | Darkened *past* the floor — at the floor it would have collapsed onto `caption`. |
| `caption` (dark) | `#5C6670` 2.93:1 | `#7A848F` 4.51:1 | |
| `signal-text` | — | `#227C6F` 4.51:1 | `signal` clears 3:1 as a mark but not 4.5:1 as text. |
| `model-text` | — | `#5962D7` 4.54:1 | `model` was 4.48:1 — short by 0.02. |
| `alert-text` | — | `#BE4737` 4.55:1 | `alert` was 4.04:1, a failure the kickoff had not identified. |

The `*-text` split exists because the brand mandates **direct series labels at line ends instead of
legend boxes**, which makes series colours into small text subject to the 4.5:1 threshold.

## A note on the 4th and 5th categorical colours

`CLAUDE.md` §3 says new categorical colours are derived "matching the chroma and lightness of the
existing series, varying hue only." Measured against dichromacy simulation, that rule cannot produce
five separable series — see **OQ-009**. `series-4` and `series-5` therefore vary lightness as well
as hue. The existing `signal`/`model` pair remains the palette's weak point (0.014 OKLab separation
under tritanopia); the mitigation is the brand's own rule that meaning is never carried by colour
alone.

## Changing a token

```bash
# 1. edit a file here
# 2. rebuild — this also runs the contrast gate and fails if a token misses its role's threshold
npm run build:tokens
# 3. verify independently
python3 tools/verify_tokens.py
# 4. commit tokens/src/ AND tokens/build/ together
```

A token value change is a **major** version bump for the design system, not a patch — see
`CLAUDE.md` §4.
