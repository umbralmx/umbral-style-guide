"""Dichromacy simulation (Vienot et al. 1999 / Brettel) for the Umbral series colours.

Reports pairwise OKLab distance between series after simulation. A pair that
collapses below ~0.10 in OKLab is not reliably separable by that viewer, which
matters because the brand mandates direct series labels rather than legends.
"""
import math
from contrast import TOKENS
from derive import hex_to_oklch, _lin, _unlin

RGB2LMS = [[17.8824, 43.5161, 4.11935],
           [3.45565, 27.1554, 3.86714],
           [0.0299566, 0.184309, 1.46709]]

LMS2RGB = [[0.080944, -0.130504, 0.116721],
           [-0.010248, 0.054019, -0.113614],
           [-0.000365, -0.004120, 0.693513]]

SIM = {
    "protanopia":   [[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]],
    "deuteranopia": [[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]],
    "tritanopia":   [[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]],
}


def _mul(m, v):
    return [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]


def simulate(hexc, kind):
    h = hexc.lstrip("#")
    rgb = [_lin(int(h[i:i + 2], 16)) * 255 for i in (0, 2, 4)]
    lms = _mul(RGB2LMS, rgb)
    lms = _mul(SIM[kind], lms)
    out = _mul(LMS2RGB, lms)
    px = []
    for c in out:
        v = max(0.0, min(1.0, c / 255.0))
        px.append(max(0, min(255, round(_unlin(v) * 255))))
    return "#%02X%02X%02X" % tuple(px)


def oklab(hexc):
    L, C, H = hex_to_oklch(hexc)
    return (L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H)))


def dist(h1, h2):
    a, b = oklab(h1), oklab(h2)
    return math.dist(a, b)


if __name__ == "__main__":
    for mode in ("laboratorio", "instrumento"):
        t = TOKENS[mode]
        series = {k: t[k] for k in ("signal", "model", "alert")}
        print(f"\n{'=' * 70}\nmodo {mode} — series separability under dichromacy\n{'=' * 70}")
        rows = [("normal", series)]
        for kind in SIM:
            rows.append((kind, {k: simulate(v, kind) for k, v in series.items()}))
        for kind, s in rows:
            pairs = [("signal", "model"), ("signal", "alert"), ("model", "alert")]
            out = []
            worst = 9
            for a, b in pairs:
                d = dist(s[a], s[b])
                worst = min(worst, d)
                out.append(f"{a[:3]}/{b[:3]} {d:.3f}")
            flag = "  <<< collapses" if worst < 0.10 else ""
            swatches = " ".join(f"{k}={v}" for k, v in s.items())
            print(f"  {kind:<13} {'  '.join(out)}{flag}")
            print(f"                {swatches}")
