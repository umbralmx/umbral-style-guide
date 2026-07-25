"""Derive AA-clearing variants of the failing Umbral tokens, in OKLCH.

Method: hold hue and chroma, walk OKLCH lightness toward the far end until the
pair clears 4.5:1 against BOTH `base` and `panel` in that mode. Hue is never
moved, so the corrected token stays recognisably the same colour. Chroma is
only reduced if the target lightness pushes the colour out of sRGB gamut.

Phase 0 proposal only — Phase 1 authors these in tokens/src/ and generates.
"""
from contrast import TOKENS, ratio

# ── sRGB <-> OKLab (Björn Ottosson) ───────────────────────────────────────

def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _unlin(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return c


def hex_to_oklch(h):
    h = h.lstrip("#")
    r, g, b = (_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    import math
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360
    return L, C, H


def oklch_to_hex(L, C, H):
    import math
    a = C * math.cos(math.radians(H))
    bb = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * bb
    m_ = L - 0.1055613458 * a - 0.0638541728 * bb
    s_ = L - 0.0894841775 * a - 1.2914855480 * bb
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    out = []
    clipped = False
    for c in (r, g, b):
        v = _unlin(c)
        if v < -0.001 or v > 1.001:
            clipped = True
        out.append(max(0, min(255, round(v * 255))))
    return "#%02X%02X%02X" % tuple(out), clipped


def solve(name, mode, target=4.5, direction=None):
    """Find the nearest-lightness variant clearing `target` on base AND panel."""
    t = TOKENS[mode]
    L, C, H = hex_to_oklch(t[name])
    if direction is None:
        direction = -1 if mode == "laboratorio" else +1
    step = 0.002
    best = None
    for i in range(0, 501):
        Ln = L + direction * step * i
        if not (0 <= Ln <= 1):
            break
        # reduce chroma only if we leave gamut
        for Cn in (C, C * 0.9, C * 0.8, C * 0.7):
            hx, clipped = oklch_to_hex(Ln, Cn, H)
            if clipped:
                continue
            rb, rp = ratio(hx, t["base"]), ratio(hx, t["panel"])
            if min(rb, rp) >= target:
                best = (hx, Ln, Cn, H, rb, rp)
                break
        if best:
            break
    return L, C, H, best


def show(name, mode, target=4.5, label=None):
    L, C, H, best = solve(name, mode, target)
    t = TOKENS[mode]
    cur_b, cur_p = ratio(t[name], t["base"]), ratio(t[name], t["panel"])
    print(f"\n  {label or name}  ({mode})")
    print(f"    now  {t[name]}  L={L:.3f} C={C:.3f} H={H:.1f}"
          f"   base {cur_b:.2f}  panel {cur_p:.2f}")
    if best:
        hx, Ln, Cn, Hn, rb, rp = best
        dc = "" if abs(Cn - C) < 1e-9 else f" (chroma {C:.3f}->{Cn:.3f})"
        print(f"    ->   {hx}  L={Ln:.3f} C={Cn:.3f} H={Hn:.1f}{dc}"
              f"   base {rb:.2f}  panel {rp:.2f}")
    else:
        print("    -> no in-gamut solution at this hue")


if __name__ == "__main__":
    print("=" * 74)
    print("Proposed AA-clearing variants (>=4.5:1 vs BOTH base and panel)")
    print("=" * 74)

    print("\n── modo laboratorio ──")
    show("caption", "laboratorio")
    show("muted", "laboratorio")
    show("signal", "laboratorio", label="signal-text (new; signal stays as mark)")
    show("model", "laboratorio", label="model-text (new)")
    show("alert", "laboratorio", label="alert-text (new)")

    print("\n── modo instrumento ──")
    show("caption", "instrumento")
    show("muted", "instrumento")
    show("signal", "instrumento", label="signal-text")
    show("model", "instrumento", label="model-text")
    show("alert", "instrumento", label="alert-text")
