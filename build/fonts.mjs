/**
 * Generates the self-hosted @font-face CSS.
 *
 *   assets/fonts/*.woff2 + tokens/build/tokens.json
 *        ↓  this script
 *   assets/fonts/fonts.css
 *
 * Satisfies UMB-TYP-005. Until Phase 7 vendored these files, that was a rule this
 * repo itself could not meet — matplotlib reported all three families missing.
 *
 * Why self-host at all: a public-interest data product has to work offline and
 * inside government networks, and a CDN leaks every reader's IP to a third party.
 * The v1.0 engineering doc asked for this in prose and shipped a Google Fonts
 * <link> in the code block of the same section; the main site copied the code.
 *
 * Run with `npm run build:fonts` (part of `npm run build`).
 */
import { promises as fs } from 'node:fs';

const DIR = 'assets/fonts';
const tokens = JSON.parse(await fs.readFile('tokens/build/tokens.json', 'utf8'));

// Exactly the subsets Google Fonts defines. `latin-ext` is the one that carries
// Spanish diacritics beyond the Latin-1 block, so it is not optional here.
const RANGE = {
  latin:
    'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, '
    + 'U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, '
    + 'U+2212, U+2215, U+FEFF, U+FFFD',
  'latin-ext':
    'U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, '
    + 'U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, '
    + 'U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF',
};

/**
 * `variable: [min, max]` declares a weight RANGE against one file — these are
 * variable fonts (they carry an `fvar` axis), so one file legitimately serves
 * every weight in between. IBM Plex Mono is still shipped as static instances,
 * so it gets one file per weight.
 */
const FACES = [
  { family: tokens.font.display, slug: 'space-grotesk', variable: [500, 600] },
  { family: tokens.font.body, slug: 'ibm-plex-sans', variable: [400, 600] },
  { family: tokens.font.mono, slug: 'ibm-plex-mono', weights: [400, 500] },
];

const out = [`/*
fonts.css — GENERATED from build/fonts.mjs. Do not edit.

Self-hosted subsets (UMB-TYP-005). Never replace these with a CDN link: a data
product must work offline and in government networks, and must not leak reader
IPs to a third party.

Space Grotesk and IBM Plex are licensed under the SIL Open Font License —
see OFL-Space-Grotesk.txt and OFL-IBM-Plex.txt in this directory.

Umbral design system · https://github.com/umbralmx/umbral-style-guide
*/
`];

const missing = [];

for (const face of FACES) {
  for (const subset of ['latin', 'latin-ext']) {
    if (face.variable) {
      const file = `${face.slug}-${subset}.woff2`;
      out.push(`@font-face {
  font-family: '${face.family}';
  font-style: normal;
  font-weight: ${face.variable[0]} ${face.variable[1]};
  font-display: swap;
  src: url('${file}') format('woff2');
  unicode-range: ${RANGE[subset]};
}`);
      missing.push(file);
    } else {
      for (const w of face.weights) {
        const file = `${face.slug}-${w}-${subset}.woff2`;
        out.push(`@font-face {
  font-family: '${face.family}';
  font-style: normal;
  font-weight: ${w};
  font-display: swap;
  src: url('${file}') format('woff2');
  unicode-range: ${RANGE[subset]};
}`);
        missing.push(file);
      }
    }
  }
}

await fs.writeFile(`${DIR}/fonts.css`, `${out.join('\n\n')}\n`);

// the gate: every face the CSS declares must actually be on disk
const present = new Set(await fs.readdir(DIR));
const absent = missing.filter((f) => !present.has(f));
const licences = ['OFL-IBM-Plex.txt', 'OFL-Space-Grotesk.txt'].filter((f) => !present.has(f));

let bytes = 0;
for (const f of missing) {
  if (present.has(f)) bytes += (await fs.stat(`${DIR}/${f}`)).size;
}

console.log(`fonts: ${missing.length} faces declared, ${Math.round(bytes / 1024)}KB vendored`);
if (absent.length || licences.length) {
  console.error('\nfonts gate FAILED');
  for (const f of absent) console.error(`  missing font file: ${f}`);
  for (const f of licences) console.error(`  missing licence: ${f} — OFL requires it ships alongside`);
  process.exit(1);
}
console.log('fonts gate: PASS — all faces present, both OFL licences shipped');
