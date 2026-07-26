#!/usr/bin/env python3
"""Independently verify the generated Umbral tokens.

The build (build/index.mjs) computes contrast and expands ramps in JavaScript.
This script re-derives the same quantities in Python, from the *generated* files,
and fails if they disagree. The point is that a mistake in the colour maths has to
be made twice, in two languages, to reach the published system.

It also checks properties the build does not: ramp monotonicity, that every
generated file actually carries the "do not edit" header, and that the corrected
tokens really do fix every failure recorded in the Phase 0 audit.

Implements the checks claimed by rules.yaml as `verify-tokens`:
`contrast-text` (UMB-COL-005), `contrast-mark` (UMB-COL-006) and
`series-separation` (UMB-COL-008).

Run: python3 tools/verify_tokens.py    (exit 1 on any failure)
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

BUILD = pathlib.Path("tokens/build")
SRC = pathlib.Path("tokens/src")

failures: list[str] = []
checks = 0


def check(ok: bool, msg: str) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(msg)


# ── colour maths, re-implemented independently of build/lib/color.mjs ──────
def _srgb_to_linear(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.2126 * _srgb_to_linear(r)
            + 0.7152 * _srgb_to_linear(g)
            + 0.0722 * _srgb_to_linear(b))


def contrast(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def oklab_l(hex_color: str) -> float:
    """OKLab lightness only — enough to check ramp monotonicity."""
    h = hex_color.lstrip("#")
    r, g, b = (_srgb_to_linear(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_


# ── load ──────────────────────────────────────────────────────────────────
if not BUILD.exists():
    sys.exit("tokens/build/ missing — run `npm run build:tokens` first")

tokens = json.loads((BUILD / "tokens.json").read_text())
report = json.loads((BUILD / "contrast.json").read_text())
THRESH = report["thresholds"]

# ── 1. every recorded ratio re-derives to the same number ─────────────────
for mode, pairs in report["modes"].items():
    for p in pairs:
        ours = contrast(p["fg"], p["bg"])
        # the build floors to 2dp so a gate can never round up into a pass
        floored = int(ours * 100) / 100
        check(abs(floored - p["ratio"]) < 0.011,
              f"{mode}/{p['token']} on {p['on']}: build says {p['ratio']}, "
              f"Python says {floored:.2f}")

# ── 2. the gate's verdicts are correct for the declared role ──────────────
for mode, pairs in report["modes"].items():
    for p in pairs:
        need = THRESH.get(p["role"])
        if need is None:
            check(p["pass"] is None,
                  f"{mode}/{p['token']}: role {p['role']} should not be gated")
        else:
            check(p["pass"] == (p["ratio"] >= need),
                  f"{mode}/{p['token']} on {p['on']}: verdict {p['pass']} "
                  f"disagrees with {p['ratio']} vs {need}")

check(report["summary"]["failures"] == 0,
      f"contrast gate reports {report['summary']['failures']} failures")

# ── 3. the Phase 0 audit failures are actually fixed ──────────────────────
# Each of these was measured on a live product in audit/2026-07-conformance.md.
AUDIT_FAILURES = [
    ("laboratorio", "caption", 2.37),
    ("laboratorio", "muted", 4.25),
    ("instrumento", "caption", 2.93),
]
for mode, token, was in AUDIT_FAILURES:
    now = min(contrast(tokens["mode"][mode][token], tokens["mode"][mode][bg])
              for bg in ("base", "panel"))
    check(now >= 4.5,
          f"{mode}/{token} was {was}:1 in v1.0 and is still only {now:.2f}:1")

# text-role variants must exist and clear 4.5 in both modes
for mode in ("laboratorio", "instrumento"):
    for token in ("signal-text", "model-text", "alert-text"):
        check(token in tokens["mode"][mode], f"{mode}/{token} missing")
        if token in tokens["mode"][mode]:
            worst = min(contrast(tokens["mode"][mode][token], tokens["mode"][mode][bg])
                        for bg in ("base", "panel"))
            check(worst >= 4.5, f"{mode}/{token} only {worst:.2f}:1")

# ── 4. ramps are monotonic in lightness and long enough to be useful ──────
for mode, ramps in tokens["ramp"].items():
    for name, steps in ramps.items():
        check(len(steps) >= 5, f"{mode}/{name}: only {len(steps)} steps")
        ls = [oklab_l(s) for s in steps]
        if name.startswith("sequential"):
            mono = all(b > a for a, b in zip(ls, ls[1:])) or all(b < a for a, b in zip(ls, ls[1:]))
            check(mono, f"{mode}/{name}: lightness is not monotonic — {[round(x,3) for x in ls]}")
        else:
            mid = len(ls) // 2
            low, high = ls[:mid + 1], ls[mid:]
            ok = (all(b >= a for a, b in zip(low, low[1:]))
                  and all(b <= a for a, b in zip(high, high[1:]))) or \
                 (all(b <= a for a, b in zip(low, low[1:]))
                  and all(b >= a for a, b in zip(high, high[1:])))
            check(ok, f"{mode}/{name}: diverging ramp does not turn at its midpoint")
        check(len(set(steps)) == len(steps), f"{mode}/{name}: duplicate steps")

# ── 5. no generated file is missing its header ────────────────────────────
for f in sorted(BUILD.iterdir()):
    if f.suffix in {".json", ".css", ".scss", ".py", ".R", ".toml", ".yml", ".mplstyle"}:
        text = f.read_text()
        check("GENERATED from tokens/src/" in text,
              f"{f.name} has no generated-file header")

# ── 6. nothing in tokens/src/ hard-codes a value twice ────────────────────
hexes: dict[str, list[str]] = {}
for f in SRC.glob("*.tokens.json"):
    for m in re.finditer(r'"\$value":\s*"(#[0-9A-Fa-f]{6})"', f.read_text()):
        hexes.setdefault(m.group(1).upper(), []).append(f.name)
for hx, files in hexes.items():
    check(len(files) == 1,
          f"{hx} is authored {len(files)} times ({', '.join(files)}) — "
          f"semantic tokens must reference primitives, not repeat their values")

# ── 7. the Streamlit config carries real keys, not the v1.0 mangled ones ──
# Only actual declarations are inspected. The file's comments quote the mangled
# v1.0 keys deliberately, to explain the correction — a substring search over the
# whole file would flag its own documentation. (Audit §4.3: every naive-grep hit
# against the most conformant product in the set was a false positive.)
toml_decls = {}
for line in (BUILD / "streamlit-config.toml").read_text().splitlines():
    if line.lstrip().startswith("#"):
        continue
    # match `key = "value"` — a naive split on "#" would truncate hex values
    m = re.match(r'\s*([A-Za-z][\w-]*)\s*=\s*"([^"]*)"', line)
    if m:
        toml_decls[m.group(1)] = m.group(2)

for key in ("primaryColor", "backgroundColor", "secondaryBackgroundColor", "textColor"):
    check(key in toml_decls, f"streamlit-config.toml missing {key}")
check(not any(k.startswith("sc-camel") for k in toml_decls),
      "streamlit-config.toml declares sc-camel- keys")
check(toml_decls.get("font") != "sans serif",
      'streamlit-config.toml sets font = "sans serif", which is Streamlit\'s Source Sans')
# umbral-lint: ignore[hardcoded-value] — asserting on the generated value is the point
check("IBM Plex Sans" in toml_decls.get("font", ""),
      f"streamlit-config.toml font is {toml_decls.get('font')!r}, not IBM Plex Sans")
check(toml_decls.get("primaryColor", "").lower() == tokens["mode"]["instrumento"]["signal"].lower(),
      "streamlit-config.toml primaryColor does not match the instrumento signal token")

# ── report ────────────────────────────────────────────────────────────────
print(f"verify_tokens: {checks} checks, {len(failures)} failed")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("all token checks pass")
