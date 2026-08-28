/**
 * Generates every logo variant from one parametric source.
 *
 *   this file + tokens/build/tokens.json
 *        ↓
 *   assets/logo/*.svg
 *
 * Closes OQ-007. The v1.0 files shipped three different bar ratios — 5:44
 * documented, 1:7.13 in the isotype, 1:6.29 in the lockup — and the lockup's bar
 * crossed to the RIGHT of the threshold line's centre, contradicting the one
 * geometric rule the brand states about its own mark. Generating them from a
 * single spec is what stops that recurring.
 *
 * Implements the `logo-geometry` check claimed by UMB-BRD-002.
 *
 * Run with `npm run build:logo` (part of `npm run build`).
 */
import { promises as fs } from 'node:fs';
import { contrast } from './lib/color.mjs';

const OUT = 'assets/logo';
const t = JSON.parse(await fs.readFile('tokens/build/tokens.json', 'utf8'));

// ── the spec ──────────────────────────────────────────────────────────────
const SPEC = {
  barRatio: [5, 44],   // width : height — brand book p.02, canonical per OQ-007
  crossAt: 0.40,       // bar centre, as a fraction along the threshold line
  dashOn: 0.105,       // dash length, as a fraction of the line's length
  dashOff: 0.075,
};

const [BW, BH] = SPEC.barRatio;

/**
 * One mark, parameterised by the height of the bar. Everything else follows,
 * so a variant cannot drift from the ratio.
 */
function mark({ barHeight, cx, cy, lineLength, lineWidth, bar, line, dash: dashOverride }) {
  const w = (barHeight * BW) / BH;
  const x0 = cx - lineLength * SPEC.crossAt;      // line starts left of the bar
  const x1 = x0 + lineLength;
  const dash = dashOverride
    ?? `${(lineLength * SPEC.dashOn).toFixed(2)} ${(lineLength * SPEC.dashOff).toFixed(2)}`;
  return {
    w,
    svg: [
      `<line x1="${round(x0)}" y1="${cy}" x2="${round(x1)}" y2="${cy}"`,
      ` stroke="${line}" stroke-width="${lineWidth}" stroke-dasharray="${dash}" stroke-linecap="butt"/>`,
      `<rect x="${round(cx - w / 2)}" y="${round(cy - barHeight / 2)}"`,
      ` width="${round(w)}" height="${barHeight}" fill="${bar}"/>`,
    ].join(''),
    lineCentre: (x0 + x1) / 2,
    barCentre: cx,
  };
}

const round = (n) => Number(n.toFixed(3));

const HEADER = (name) => `<!-- ${name} — GENERATED from build/logo.mjs. Do not edit.
     Bar ratio ${BW}:${BH}; bar crosses at ${SPEC.crossAt * 100}% of the threshold line.
     Umbral design system · code MIT · content CC BY 4.0 -->`;

await fs.mkdir(OUT, { recursive: true });
const written = [];
const geometry = [];

// ── isotype ───────────────────────────────────────────────────────────────
for (const mode of ['light', 'dark']) {
  const c = t.mode[mode === 'light' ? 'laboratorio' : 'instrumento'];
  const m = mark({
    barHeight: 88, cx: 52, cy: 60, lineLength: 96, lineWidth: 7,
    bar: c.signal, line: c.caption,
  });
  const name = `umbral-isotype-${mode}.svg`;
  await fs.writeFile(`${OUT}/${name}`,
    `${HEADER(name)}\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" `
    + `width="120" height="120" role="img" aria-label="umbral_">\n  ${m.svg}\n</svg>\n`);
  written.push(name);
  geometry.push({ name, ...m, bar: c.signal, line: c.caption, bg: c.base });
}

// ── lockup ────────────────────────────────────────────────────────────────
for (const mode of ['light', 'dark']) {
  const c = t.mode[mode === 'light' ? 'laboratorio' : 'instrumento'];
  const m = mark({
    barHeight: 44, cx: 56, cy: 60, lineLength: 60, lineWidth: 4,
    bar: c.signal, line: c.caption,
  });
  const name = `umbral-lockup-${mode}.svg`;
  await fs.writeFile(`${OUT}/${name}`,
    `${HEADER(name)}\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 120" `
    + `width="420" height="120" role="img" aria-label="umbral_">\n`
    + `  <rect width="420" height="120" fill="${c.base}"/>\n`
    + `  ${m.svg}\n`
    + `  <text x="108" y="78" font-family="'${t.font.display}',sans-serif" font-size="52"`
    + ` font-weight="${t.font.displayWeight}" letter-spacing="-1.5" fill="${c.ink}">umbral`
    + `<tspan fill="${c['signal-text']}">_</tspan></text>\n</svg>\n`);
  written.push(name);
  geometry.push({ name, ...m, bar: c.signal, line: c.caption, bg: c.base });
}

// ── favicon ───────────────────────────────────────────────────────────────
{
  const c = t.mode.instrumento;
  const m = mark({
    // Deliberately coarser than the other variants: a favicon renders at 16px,
    // where the standard dash pattern turns into a grey smear.
    barHeight: 44, cx: 27, cy: 32, lineLength: 46, lineWidth: 5,
    dash: '7 5', bar: c.signal, line: c.caption,
  });
  const name = 'umbral-favicon.svg';
  await fs.writeFile(`${OUT}/${name}`,
    `${HEADER(name)}\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" `
    + `width="64" height="64" role="img" aria-label="umbral_">\n`
    + `  <rect width="64" height="64" fill="${c.base}"/>\n  ${m.svg}\n</svg>\n`);
  written.push(name);
  geometry.push({ name, ...m, bar: c.signal, line: c.caption, bg: c.base });
}

// ── the gate: geometry and contrast, checked here rather than by eye ───────
const problems = [];
for (const g of geometry) {
  if (!(g.barCentre < g.lineCentre)) {
    problems.push(`${g.name}: bar centre ${g.barCentre} is not left of line centre ${g.lineCentre}`);
  }
  // the dashed threshold is a meaningful graphical element, so 3:1 applies
  const lineContrast = contrast(g.line, g.bg);
  if (lineContrast < 3) {
    problems.push(`${g.name}: threshold line ${lineContrast.toFixed(2)}:1 against ${g.bg}, needs 3:1`);
  }
  const barContrast = contrast(g.bar, g.bg);
  if (barContrast < 3) {
    problems.push(`${g.name}: bar ${barContrast.toFixed(2)}:1 against ${g.bg}, needs 3:1`);
  }
}

await fs.writeFile(`${OUT}/README.md`, `# \`assets/logo/\`

**Generated by \`build/logo.mjs\`. Do not edit.**

Every variant comes from one parametric spec: bar ratio **${BW}:${BH}**, crossing at
**${SPEC.crossAt * 100}%** along the dashed threshold — always left of centre.

| File | Use |
|---|---|
| \`umbral-isotype-{light,dark}.svg\` | Favicon, avatar, corner of a card |
| \`umbral-lockup-{light,dark}.svg\` | Header, report cover, deck footer |
| \`umbral-favicon.svg\` | Browser tab — coarser dashes so it survives 16px |

The build gate checks two things numerically rather than by eye:

1. The bar crosses left of the threshold line's centre.
2. Both the bar and the dashed line clear 3:1 against their background.

This exists because the v1.0 files shipped **three different bar ratios**: 5:44 documented, 1:7.13
in the isotype, 1:6.29 in the lockup. The lockup's bar also crossed to the *right*. That contradicts
the one geometric rule the brand states about its own mark. See OQ-007.

The clear space is one bar-height on all four sides. That is a layout instruction, not part of the
SVG viewBox.
`);

console.log(`logo: ${written.length} variants generated into ${OUT}/`);
console.log(`  bar ratio ${BW}:${BH} · crossing at ${SPEC.crossAt * 100}% · all bars left of centre`);
for (const g of geometry) {
  console.log(`  ${g.name.padEnd(28)} line ${contrast(g.line, g.bg).toFixed(2)}:1 · `
    + `bar ${contrast(g.bar, g.bg).toFixed(2)}:1`);
}
if (problems.length) {
  console.error('\nlogo gate FAILED');
  for (const p of problems) console.error(`  ${p}`);
  process.exit(1);
}
console.log('logo gate: PASS');
