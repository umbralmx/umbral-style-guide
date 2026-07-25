# `build/lib/`

Shared maths for the build. One file.

**`color.mjs`** — sRGB ↔ OKLab/OKLCH conversion, gamut fitting by chroma reduction, WCAG 2.1
contrast, and dichromacy simulation (Viénot/Brettel) with OKLab distance.

Two things worth knowing about it:

- **`gamutFit` reduces chroma only.** Hue and lightness are preserved, because hue is what makes a
  token recognisably the same colour and lightness is what makes it pass contrast.
- **`floorRatio` rounds down.** A contrast gate must never round *up* into a pass — 4.4991:1 is a
  failure, and v1.0 had a token that missed by exactly that kind of margin.

`audit/scripts/contrast.py` and `cvd.py` implement the same maths in Python. They're not duplicates
by accident — CI runs both and compares.
