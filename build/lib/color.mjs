/**
 * OKLab/OKLCH colour maths and WCAG contrast for the Umbral token build.
 *
 * This is the single implementation used to expand ramps and to generate
 * `tokens/build/contrast.json`. `audit/scripts/contrast.py` and `cvd.py` re-derive
 * the same numbers independently in Python and CI compares them, so a mistake here
 * cannot silently propagate into the published system.
 *
 * OKLab conversion: Björn Ottosson, https://bottosson.github.io/posts/oklab/
 */

// ── sRGB transfer ─────────────────────────────────────────────────────────
const toLinear = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const toGamma = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);

export function hexToRgb(hex) {
  const h = hex.replace('#', '');
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
}

export function rgbToHex([r, g, b]) {
  const c = (v) => Math.max(0, Math.min(255, Math.round(v * 255)))
    .toString(16).padStart(2, '0').toUpperCase();
  return `#${c(r)}${c(g)}${c(b)}`;
}

// ── OKLab ─────────────────────────────────────────────────────────────────
export function hexToOklch(hex) {
  const [r, g, b] = hexToRgb(hex).map(toLinear);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
  const C = Math.hypot(A, B);
  const H = ((Math.atan2(B, A) * 180) / Math.PI + 360) % 360;
  return { L, C, H };
}

/** Returns { hex, inGamut } — inGamut false means the requested L/C/H was clipped. */
export function oklchToHex(L, C, H) {
  const a = C * Math.cos((H * Math.PI) / 180);
  const b = C * Math.sin((H * Math.PI) / 180);
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3;
  const lin = [
    +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
  ];
  let inGamut = true;
  const rgb = lin.map((v) => {
    const g = toGamma(v);
    if (g < -0.0005 || g > 1.0005) inGamut = false;
    return Math.max(0, Math.min(1, g));
  });
  return { hex: rgbToHex(rgb), inGamut };
}

/**
 * Bring an OKLCH colour into sRGB gamut by reducing chroma only — hue and
 * lightness are preserved, because hue is what makes a token recognisable and
 * lightness is what makes it pass contrast.
 */
export function gamutFit(L, C, H) {
  let lo = 0;
  let hi = C;
  if (oklchToHex(L, C, H).inGamut) return oklchToHex(L, C, H).hex;
  for (let i = 0; i < 28; i += 1) {
    const mid = (lo + hi) / 2;
    if (oklchToHex(L, mid, H).inGamut) lo = mid;
    else hi = mid;
  }
  return oklchToHex(L, lo, H).hex;
}

// ── WCAG 2.1 contrast ─────────────────────────────────────────────────────
export function luminance(hex) {
  const [r, g, b] = hexToRgb(hex).map(toLinear);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export function contrast(a, b) {
  const l1 = luminance(a);
  const l2 = luminance(b);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

/** Round the way a contrast gate must: never round *up* into a pass. */
export const floorRatio = (r) => Math.floor(r * 100) / 100;

// ── dichromacy simulation (Viénot 1999 / Brettel) ─────────────────────────
const RGB2LMS = [
  [17.8824, 43.5161, 4.11935],
  [3.45565, 27.1554, 3.86714],
  [0.0299566, 0.184309, 1.46709],
];
const LMS2RGB = [
  [0.080944, -0.130504, 0.116721],
  [-0.010248, 0.054019, -0.113614],
  [-0.000365, -0.004120, 0.693513],
];
const SIM = {
  protanopia: [[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]],
  deuteranopia: [[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]],
  tritanopia: [[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]],
};

const mul = (M, v) => M.map((row) => row.reduce((acc, x, i) => acc + x * v[i], 0));

export function simulateCvd(hex, kind) {
  const rgb = hexToRgb(hex).map((c) => toLinear(c) * 255);
  const out = mul(LMS2RGB, mul(SIM[kind], mul(RGB2LMS, rgb)));
  return rgbToHex(out.map((c) => toGamma(Math.max(0, Math.min(1, c / 255)))));
}

/** Perceptual distance in OKLab — below ~0.10 two marks are not reliably separable. */
export function oklabDistance(h1, h2) {
  const p = (h) => {
    const { L, C, H } = hexToOklch(h);
    return [L, C * Math.cos((H * Math.PI) / 180), C * Math.sin((H * Math.PI) / 180)];
  };
  const [a, b] = [p(h1), p(h2)];
  return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
}

export const CVD_KINDS = Object.keys(SIM);
