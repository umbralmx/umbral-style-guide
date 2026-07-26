/**
 * Packages the agent skill as a .skill file for upload to claude.ai.
 *
 *   skills/umbral-brand/  →  dist/umbral-brand-v<version>.skill
 *
 * A .skill is a zip. This uses the system `zip`, which is present on macOS and on
 * ubuntu-latest, rather than adding an archiver dependency for one command.
 *
 * Run with `npm run package:skill`.
 */
import { promises as fs } from 'node:fs';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const run = promisify(execFile);
const rules = JSON.parse(await fs.readFile('rules/rules.json', 'utf8'));
const out = `dist/umbral-brand-v${rules.version}.skill`;

await fs.mkdir('dist', { recursive: true });
await fs.rm(out, { force: true });

// -x excludes the caches that make a package non-reproducible
await run('zip', ['-r', '-q', '-X', `../../${out}`, '.',
  '-x', '*.pyc', '-x', '*__pycache__*', '-x', '.DS_Store'],
{ cwd: 'skills/umbral-brand' });

const { size } = await fs.stat(out);
const listing = await run('unzip', ['-l', out]);
const files = (listing.stdout.match(/^\s+\d+\s+/gm) ?? []).length;

console.log(`skill package: ${out} (${Math.round(size / 1024)}KB, ${files} files)`);

// the gate: the package must carry the pieces the skill needs to work standalone
const required = ['SKILL.md', 'references/color.md', 'references/charts.md',
  'references/terminology.md', 'assets/tokens.json', 'assets/rules.json',
  'scripts/check_contrast.py'];
const missing = required.filter((f) => !listing.stdout.includes(f));
if (missing.length) {
  console.error('\nskill package FAILED — missing:');
  for (const f of missing) console.error(`  ${f}`);
  process.exit(1);
}
console.log('skill package: PASS — SKILL.md, references, assets and scripts all present');
