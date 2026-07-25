/**
 * Umbral rule build.
 *
 *   rules/rules.yaml        (authored, NORMATIVE)
 *        ↓  this script
 *   rules/rules.json        (generated — machine consumers, umbral-lint, the skill)
 *   guide/CHECKLIST.md      (generated — printable one page)
 *   guide/_includes/rules/  (generated — one callout per rule, included by chapters)
 *
 * Run with `npm run build:rules`.
 *
 * Validation is deliberately stricter than the JSON Schema: the schema checks shape,
 * this checks the invariants that keep the rule set usable — unique IDs, unique check
 * ids, live cross-references, and an ID prefix that matches the rule's category.
 */
// rules.schema.json declares draft 2020-12, which needs Ajv's 2020 entry point;
// the default export only understands draft-07.
import Ajv from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import { parse } from 'yaml';
import { promises as fs } from 'node:fs';
import path from 'node:path';

const SRC = 'rules/rules.yaml';
const SCHEMA = 'rules/rules.schema.json';
const OUT_JSON = 'rules/rules.json';
const OUT_CHECKLIST = 'guide/CHECKLIST.md';
const OUT_INCLUDES = 'guide/_includes/rules';

const PREFIX_FOR = {
  brand: 'BRD',
  color: 'COL',
  type: 'TYP',
  layout: 'LAY',
  chart: 'CHT',
  voice: 'VOZ',
  numbers: 'NUM',
  data: 'DAT',
  a11y: 'A11Y',
  method: 'MET',
  process: 'PRO',
};

const SEVERITY_LABEL = {
  error: { es: 'error', en: 'error', mark: '■' },
  warning: { es: 'advertencia', en: 'warning', mark: '▲' },
  info: { es: 'guía', en: 'info', mark: '·' },
};

const doc = parse(await fs.readFile(SRC, 'utf8'));
const schema = JSON.parse(await fs.readFile(SCHEMA, 'utf8'));

// ── 1. schema ─────────────────────────────────────────────────────────────
const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);
const validate = ajv.compile(schema);
const problems = [];

if (!validate(doc)) {
  for (const e of validate.errors) {
    problems.push(`schema ${e.instancePath || '/'} ${e.message}`);
  }
}

// ── 2. invariants the schema cannot express ───────────────────────────────
const rules = doc.rules ?? [];
const seenId = new Map();
const seenCheck = new Map();

for (const r of rules) {
  if (seenId.has(r.id)) problems.push(`duplicate rule id ${r.id}`);
  seenId.set(r.id, r);

  const want = PREFIX_FOR[r.category];
  if (want && !r.id.startsWith(`UMB-${want}-`)) {
    problems.push(`${r.id} is category "${r.category}" but its ID prefix is not UMB-${want}-`);
  }

  if (r.check?.id) {
    if (seenCheck.has(r.check.id)) {
      problems.push(`check id "${r.check.id}" used by both ${seenCheck.get(r.check.id)} and ${r.id}`);
    }
    seenCheck.set(r.check.id, r.id);
  }

  // an automated check must name a tool that can actually run it
  if (r.check?.type === 'automated' && !r.check.tool) {
    problems.push(`${r.id} is automated but names no tool`);
  }

  // a rule added after 1.0 should say where it came from
  if (r.since !== '1.0' && !r.evidence) {
    problems.push(`${r.id} is new in ${r.since} but records no evidence`);
  }

  if (!doc.categories?.[r.category]) {
    problems.push(`${r.id} uses category "${r.category}", which has no label`);
  }
}

for (const r of rules) {
  for (const ref of r.see_also ?? []) {
    if (!seenId.has(ref)) problems.push(`${r.id} references ${ref}, which does not exist`);
    if (ref === r.id) problems.push(`${r.id} references itself`);
  }
  if (r.supersedes && !seenId.has(r.supersedes)) {
    // superseded rules may legitimately be gone; only flag a live self-reference
    if (r.supersedes === r.id) problems.push(`${r.id} supersedes itself`);
  }
}

if (problems.length) {
  console.error(`rules: ${problems.length} problem(s)\n`);
  for (const p of problems) console.error(`  ${p}`);
  process.exit(1);
}

// ── 3. rules.json ─────────────────────────────────────────────────────────
const byCategory = {};
const bySurface = {};
const bySeverity = { error: 0, warning: 0, info: 0 };
const automated = [];

for (const r of rules) {
  (byCategory[r.category] ??= []).push(r.id);
  for (const s of r.applies_to) (bySurface[s] ??= []).push(r.id);
  bySeverity[r.severity] += 1;
  if (r.check.type === 'automated') {
    automated.push({ rule: r.id, tool: r.check.tool, check: r.check.id, severity: r.severity });
  }
}

const json = {
  $generated: 'rules.json — GENERATED from rules/rules.yaml. Do not edit.',
  version: doc.version,
  counts: {
    total: rules.length,
    bySeverity,
    byCheckType: rules.reduce((a, r) => ({ ...a, [r.check.type]: (a[r.check.type] ?? 0) + 1 }), {}),
  },
  categories: doc.categories,
  index: { byCategory, bySurface },
  automatedChecks: automated,
  rules,
};
await fs.writeFile(OUT_JSON, `${JSON.stringify(json, null, 2)}\n`);

// ── 4. guide/CHECKLIST.md — one printable page ────────────────────────────
// Deliberately NOT every `error` rule. CI already enforces the automated ones and
// will block the release on its own; reprinting them makes a two-page list that
// nobody reads. This page carries what only a human can decide.
const errors = rules.filter((r) => r.severity === 'error');
const human = errors.filter((r) => r.check.type !== 'automated');
const auto = errors.filter((r) => r.check.type === 'automated');
const catOrder = Object.keys(doc.categories);

const checklist = [
  '<!-- GENERATED from rules/rules.yaml. Do not edit. -->',
  '',
  '# Checklist de entrega',
  '',
  `Umbral v${doc.version}`,
  '',
  `Esta hoja **no** repite las ${auto.length} reglas que CI ya comprueba sola — si alguna falla, el`,
  'release se bloquea sin que nadie tenga que acordarse. Aquí están las que exigen',
  'criterio humano, que son las que se pierden.',
  '',
  `Antes de publicar, verificar estas **${human.length}**:`,
  '',
];
for (const cat of catOrder) {
  const inCat = human.filter((r) => r.category === cat);
  if (!inCat.length) continue;
  checklist.push(`### ${doc.categories[cat].label}`, '');
  for (const r of inCat) {
    checklist.push(`- [ ] **${r.id}** — ${r.title}`);
  }
  checklist.push('');
}
checklist.push(
  '---',
  '',
  '## Lo que comprueba la máquina',
  '',
  '```',
  'npm run build      # tokens + reglas; falla si un token no alcanza su umbral',
  'npm run verify     # re-deriva contraste y reglas de forma independiente',
  'umbral-lint .      # las comprobaciones automáticas sobre este repo',
  '```',
  '',
  `${auto.length} reglas \`error\` automáticas · ${rules.filter((r) => r.severity === 'warning').length} advertencias · `
  + `${rules.filter((r) => r.severity === 'info').length} de guía. Todas en \`rules/rules.yaml\`.`,
  '',
  '`■ error` bloquea el release · `▲ advertencia` se reporta y se justifica · `· guía` orienta.',
  '',
);
await fs.mkdir('guide', { recursive: true });
await fs.writeFile(OUT_CHECKLIST, checklist.join('\n'));

// ── 5. one callout include per rule ───────────────────────────────────────
// Chapters include these rather than restating a rule, which is what makes
// UMB-PRO-002 ("prose never states a rule rules.yaml does not") mechanical.
await fs.rm(OUT_INCLUDES, { recursive: true, force: true });
await fs.mkdir(OUT_INCLUDES, { recursive: true });

for (const r of rules) {
  const sev = SEVERITY_LABEL[r.severity];
  const lines = [
    '<!-- GENERATED from rules/rules.yaml. Do not edit. -->',
    `<div class="u-rule" id="${r.id}" data-severity="${r.severity}">`,
    '',
    `**${sev.mark} ${r.id}** · ${doc.categories[r.category].label} · ${sev.es}`,
    '',
    `### ${r.title}`,
    '',
    r.rationale.trim(),
    '',
    `| | |`,
    `|---|---|`,
    `| **Sí** | ${r.do} |`,
    `| **No** | ${r.dont} |`,
    '',
  ];
  if (r.exceptions?.length) {
    lines.push('**Excepciones**', '');
    for (const e of r.exceptions) lines.push(`- ${e.trim()}`);
    lines.push('');
  }
  const how = r.check.type === 'automated'
    ? `Automática — \`${r.check.tool}\`, comprobación \`${r.check.id}\`.`
    : r.check.type === 'manual'
      ? `Manual. ${r.check.note ?? ''}`.trim()
      : 'En revisión.';
  lines.push(`*Comprobación:* ${how}`);
  if (r.check.note && r.check.type === 'automated') lines.push('', `*Nota:* ${r.check.note.trim()}`);
  if (r.evidence) lines.push('', `*Origen:* ${r.evidence.trim()}`);
  if (r.see_also?.length) lines.push('', `*Ver también:* ${r.see_also.join(' · ')}`);
  lines.push('', `<small>Desde v${r.since}. Regla normativa: <code>rules/rules.yaml</code>.</small>`, '', '</div>', '');
  await fs.writeFile(path.join(OUT_INCLUDES, `${r.id}.md`), lines.join('\n'));
}

// ── report ────────────────────────────────────────────────────────────────
console.log(`rules: ${rules.length} rules validated`);
console.log(`  severity   ${bySeverity.error} error · ${bySeverity.warning} warning · ${bySeverity.info} info`);
console.log(`  checks     ${automated.length} automated · `
  + `${rules.filter((r) => r.check.type === 'manual').length} manual · `
  + `${rules.filter((r) => r.check.type === 'review').length} review`);
console.log(`  categories ${catOrder.map((c) => `${c}:${(byCategory[c] ?? []).length}`).join(' ')}`);
console.log(`\n✔︎ ${OUT_JSON}\n✔︎ ${OUT_CHECKLIST}\n✔︎ ${OUT_INCLUDES}/ (${rules.length} callouts)`);
