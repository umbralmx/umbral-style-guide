/**
 * Generates the guide's data-driven partials.
 *
 *   tokens/build/{tokens,contrast}.json + rules/rules.json
 *        ↓  this script
 *   guide/_includes/*.md
 *
 * Chapters include these rather than transcribing values, so the guide cannot
 * state a colour, a ratio or a rule that the normative layer does not.
 *
 * Run with `npm run build:guide` (part of `npm run build`).
 */
import { promises as fs } from 'node:fs';

const OUT = 'guide/_includes';
const tokens = JSON.parse(await fs.readFile('tokens/build/tokens.json', 'utf8'));
const contrast = JSON.parse(await fs.readFile('tokens/build/contrast.json', 'utf8'));
const rules = JSON.parse(await fs.readFile('rules/rules.json', 'utf8'));

const HEAD = '<!-- GENERATED from the normative layer. Do not edit. -->\n';
const MODES = ['laboratorio', 'instrumento'];
const ROLE_ES = {
  text: 'texto', mark: 'marca', furniture: 'mobiliario', surface: 'superficie',
};

// ── the colour token table ────────────────────────────────────────────────
{
  const rows = Object.keys(tokens.mode.laboratorio)
    .filter((k) => k !== 'series')
    .map((name) => {
      const pair = contrast.modes.laboratorio.find((p) => p.token === name);
      const role = pair ? ROLE_ES[pair.role] : 'superficie';
      return `| \`${name}\` | \`${tokens.mode.laboratorio[name]}\` | \`${tokens.mode.instrumento[name]}\` | ${role} |`;
    });
  await fs.writeFile(`${OUT}/token-table.md`, `${HEAD}
| Token | laboratorio | instrumento | Rol de contraste |
|---|---|---|---|
${rows.join('\n')}
`);
}

// ── the generated contrast matrix ─────────────────────────────────────────
{
  const block = (mode) => {
    const pairs = contrast.modes[mode];
    const rows = pairs.map((p) => {
      const need = p.threshold === null ? '—' : `${p.threshold}:1`;
      const verdict = p.pass === null ? 'exento' : (p.pass ? 'pasa' : '**FALLA**');
      return `| \`${p.token}\` | \`${p.on}\` | ${p.ratio.toFixed(2)}:1 | ${ROLE_ES[p.role]} | ${need} | ${verdict} |`;
    });
    return `#### modo ${mode}

| Token | Sobre | Ratio | Rol | Umbral | |
|---|---|---|---|---|---|
${rows.join('\n')}
`;
  };
  await fs.writeFile(`${OUT}/contrast-matrix.md`, `${HEAD}
${MODES.map(block).join('\n')}
Comprobados ${contrast.summary.pairsChecked} pares · ${contrast.summary.failures} fallos ·
${contrast.summary.exempt} tokens de mobiliario exentos por declaración explícita.

Los tokens con rol \`mobiliario\` —retícula, borde, línea base— están **deliberadamente** por debajo
de 3:1. Tienen que quedar por debajo del dato.

La exención se declara token por token en \`tokens/src/semantic.color.tokens.json\`. Nunca se hereda.
`);
}

// ── the series palette, with its dichromacy measurements ──────────────────
{
  const block = (mode) => {
    const names = tokens.mode[mode].series
      .map((hex) => Object.entries(tokens.mode[mode]).find(([, v]) => v === hex)?.[0]);
    const swatches = tokens.mode[mode].series
      .map((hex, i) => `| ${i + 1} | \`${names[i]}\` | \`${hex}\` |`);
    const worst = contrast.cvd[mode]
      .slice().sort((a, b) => a.worst - b.worst).slice(0, 3)
      .map((r) => `| \`${r.a}\` / \`${r.b}\` | ${r.normal} | ${r.protanopia} | ${r.deuteranopia} | ${r.tritanopia} |`);
    return `#### modo ${mode}

| Orden | Token | Valor |
|---|---|---|
${swatches.join('\n')}

Los tres pares peor separados, medidos en distancia OKLab bajo simulación de dicromacía:

| Par | Normal | Protanopía | Deuteranopía | Tritanopía |
|---|---|---|---|---|
${worst.join('\n')}
`;
  };
  await fs.writeFile(`${OUT}/series-palette.md`, `${HEAD}
${MODES.map(block).join('\n')}
Por debajo de ~0.10, dos marcas dejan de distinguirse con fiabilidad.

Por eso la etiqueta directa (UMB-CHT-005) y la prohibición de codificar solo con color
(UMB-A11Y-005) no son estilísticas. Son la mitigación real del punto más débil de la paleta.
`);
}

// ── the full rule index ───────────────────────────────────────────────────
{
  const sev = { error: '■', warning: '▲', info: '·' };
  const byCat = rules.index.byCategory;
  const sections = Object.entries(rules.categories).map(([cat, meta]) => {
    const ids = byCat[cat] ?? [];
    if (!ids.length) return '';
    const rows = ids.map((id) => {
      const r = rules.rules.find((x) => x.id === id);
      const how = r.check.type === 'automated' ? `\`${r.check.id}\`` : r.check.type;
      return `| [\`${r.id}\`](#${r.id.toLowerCase()}) | ${sev[r.severity]} | ${r.title} | ${how} |`;
    });
    return `### ${meta.label}

| ID | | Regla | Comprobación |
|---|---|---|---|
${rows.join('\n')}
`;
  });
  await fs.writeFile(`${OUT}/rule-index.md`, `${HEAD}
${rules.counts.total} reglas · ${rules.counts.bySeverity.error} \`error\` ·
${rules.counts.bySeverity.warning} \`advertencia\` · ${rules.counts.bySeverity.info} \`guía\`.

${sections.filter(Boolean).join('\n')}`);
}

// ── the type scale ────────────────────────────────────────────────────────
{
  await fs.writeFile(`${OUT}/type-scale.md`, `${HEAD}
| Rol | Familia | Peso | Tamaño |
|---|---|---|---|
| h1 | ${tokens.font.display} | ${tokens.font.displayWeight} | 44px |
| h2 | ${tokens.font.display} | ${tokens.font.displayWeight} | 28px |
| Título de gráfica | ${tokens.font.display} | ${tokens.font.displayWeight} | 22px |
| Cuerpo | ${tokens.font.body} | 400 | 17px |
| Etiqueta | ${tokens.font.body} | 400 | 13px |
| Eje y fuente | ${tokens.font.mono} | 400 | 12px |

Tracking de display: \`${tokens.font.displayTracking}\`. Medida máxima: \`${tokens.scale.measure}\`.
Mínimos: 12px mono en web · 24px en slides · 11pt en documentos.
`);
}

console.log(`guide: 5 partials generated into ${OUT}/`);
