/**
 * Generates the agent skill's references and pinned assets, plus the downstream
 * CLAUDE.md snippet.
 *
 *   tokens/build/* + rules/rules.json + guide/*
 *        ↓  this script
 *   skills/umbral-brand/references/*   (generated)
 *   skills/umbral-brand/assets/*       (pinned copies)
 *   dist/CLAUDE.snippet.md             (generated, version-pinned)
 *
 * SKILL.md itself is authored — it is instructions, not data. Everything it cites
 * lives in the generated references, so the skill cannot drift from the norm.
 * That matters: the v1.0 skill shipped the old token values and kept handing out
 * colours that failed contrast long after they were known to be wrong.
 *
 * Run with `npm run build:skill` (part of `npm run build`).
 */
import { promises as fs } from 'node:fs';
import path from 'node:path';

const SKILL = 'skills/umbral-brand';
const REF = `${SKILL}/references`;
const AST = `${SKILL}/assets`;

const tokens = JSON.parse(await fs.readFile('tokens/build/tokens.json', 'utf8'));
const contrast = JSON.parse(await fs.readFile('tokens/build/contrast.json', 'utf8'));
const rules = JSON.parse(await fs.readFile('rules/rules.json', 'utf8'));

const VERSION = rules.version;
const TAG = `v${VERSION}`;
const RAW = `https://raw.githubusercontent.com/umbralmx/umbral-style-guide/${TAG}`;

const HEAD = (what) => `<!-- ${what} — GENERATED from the normative layer of
     umbralmx/umbral-style-guide ${TAG}. Do not edit; regenerate. -->\n`;

await fs.mkdir(REF, { recursive: true });
await fs.mkdir(AST, { recursive: true });
await fs.mkdir('dist', { recursive: true });

const inCategory = (c) => rules.rules.filter((r) => r.category === c);

/** Render rules as a compact list an agent can act on. */
function ruleList(rs) {
  return rs.map((r) => {
    const sev = r.severity === 'error' ? '**must**' : r.severity === 'warning' ? 'should' : 'may';
    return `- **${r.id}** (${sev}) — ${r.title_en}\n`
      + `  - do: ${r.do}\n  - don't: ${r.dont}`;
  }).join('\n');
}

// ── references/color.md ───────────────────────────────────────────────────
{
  const rows = Object.keys(tokens.mode.laboratorio)
    .filter((k) => k !== 'series')
    .map((n) => {
      const p = contrast.modes.laboratorio.find((x) => x.token === n);
      return `| \`${n}\` | \`${tokens.mode.laboratorio[n]}\` | \`${tokens.mode.instrumento[n]}\` | ${p ? p.role : 'surface'} |`;
    });
  const worst = ['laboratorio', 'instrumento'].map((m) => {
    const w = contrast.cvd[m].slice().sort((a, b) => a.worst - b.worst)[0];
    return `- **${m}**: worst-separated pair is \`${w.a}\`/\`${w.b}\` at ${w.worst} (OKLab, worst case across normal vision and simulated dichromacy)`;
  }).join('\n');

  await fs.writeFile(`${REF}/color.md`, `${HEAD('references/color.md')}
# Color

Read \`assets/tokens.json\` for machine-readable values. Never retype a hex.

| Token | laboratorio (light) | instrumento (dark) | Contrast role |
|---|---|---|---|
${rows.join('\n')}

## Roles decide the threshold

| Role | Threshold | Meaning |
|---|---|---|
| \`text\` | 4.5:1 | anything read |
| \`mark\` | 3:1 | data marks — series, bars, points |
| \`furniture\` | exempt | gridlines, borders, baselines. Deliberately low-contrast; do not "fix" |
| \`surface\` | — | backgrounds; measured against |

Verified in CI: ${contrast.summary.pairsChecked} pairs, ${contrast.summary.failures} failing,
${contrast.summary.exempt} furniture tokens exempt by explicit declaration.

## The text variants

\`signal\` clears 3:1 as a mark but not 4.5:1 as text. Because the brand mandates **direct series
labels instead of legend boxes**, series colours end up as small text — so:

- use \`signal\` / \`model\` / \`alert\` for the mark;
- use \`signal-text\` / \`model-text\` / \`alert-text\` for any text, link, or direct series label.

## Series order

\`${tokens.mode.laboratorio.series.join('` · `')}\` (laboratorio)

Semantic order: signal, model, muted, alert, series-4, series-5. Maximum 5 in one chart.

The third series is **\`muted\`**, not \`caption\`. v1.0's matplotlib and Observable Plot themes used
\`caption\`, which sits below the 3:1 a data mark needs.

## Colour-vision deficiency

${worst}

Below ~0.10 two marks are not reliably separable. The mitigation is not cosmetic — it is the
mandatory direct label (UMB-CHT-005) and the ban on colour-only encoding (UMB-A11Y-005).

## Ramps

| Ramp | Steps | Use |
|---|---|---|
| sequential \`signal\` | ${tokens.ramp.laboratorio.sequentialSignal.length} | intensity of one variable; the default choropleth |
| sequential \`model\` | ${tokens.ramp.laboratorio.sequentialModel.length} | a second variable — **never in the same figure** as the above |
| diverging | ${tokens.ramp.laboratorio.diverging.length} | change, surplus/deficit, above/below expectation |

Plus \`missing\` for absent data and a 45° hatch for suppressed values. Missing, suppressed and zero
must look different from one another.

## Rules

${ruleList(inCategory('color'))}
`);
}

// ── references/charts.md ──────────────────────────────────────────────────
{
  await fs.writeFile(`${REF}/charts.md`, `${HEAD('references/charts.md')}
# Charts

**Read this before writing any chart code.**

## The frame every chart carries

\`\`\`
Title that states the finding, as a sentence      Space Grotesk 500, 22px, left-aligned
Geography · period · unit                         Plex Sans, muted
[ plot area ]                                     horizontal gridlines only,
                                                  darker baseline, no border, no fill
──────────────────────────────────────            1px rule
Fuente: … Consulta realizada el …      umbral.org.mx   Plex Mono 12px, caption
\`\`\`

Plus, always:

- \`aria-label\` carrying the same claim as the title — not "line chart";
- an adjacent data table or \`<details>\`;
- a downloadable CSV.

## Source line format

\`\`\`
Fuente: Elaboración propia con datos de ORIGEN (INSTITUCIÓN). Consulta realizada el AAAA-MM-DD.
…and umbral.org.mx on the right of the same rule. The licence and the snapshot tag go on the
page, not in this line (UMB-DAT-004, UMB-DAT-002).
\`\`\`

The snapshot tag matters for live registers: the RNPDNO's counts for past months change between
queries, so two correct charts made weeks apart appear to contradict each other without it.

## Uncertainty

- Band at **${tokens.uncertaintyBandOpacity}** opacity of the series colour, no border.
- Dashed stroke (\`7 5\`) past the last observed datum.
- Dashed vertical rule labelled \`hoy\`.
- The subtitle must say **what the band is**: \`IC 95%\`, \`intervalo de predicción 80%\`, or the
  source's own published bounds.

Live registers under-report recent periods. Mark the incomplete tail as provisional, or the final
drop reads as an improvement.

## Never

Pie · donut · 3D · dual axes · truncated y-axis without an annotation · legend boxes · more than 5
series · a chart without its source.

## Picking a chart

| Intent | Chart |
|---|---|
| Change over time | Line; area only if the total means something |
| Ranking | Horizontal bars, sorted by value |
| Composition | Stacked bar to 100% — never a pie |
| Distribution | Histogram; box or ridge to compare; dots when n < 30 |
| Relationship | Scatter; no trend line unless the model is declared |
| Geography | Choropleth of **rates**, never counts — and ask if sorted bars read better |
| Daily density over years | Calendar heatmap — one square cell per day, one sequential ramp |

## The calendar heatmap

One square cell per day, columns are weeks, rows are weekdays. Use it for cadence, not for trend.

It breaks UMB-COL-010 more easily than any other chart. A day with no entry, a suppressed day and a
measured zero all look like an empty cell. Draw three distinct fills and put all three in the
legend.

A live register makes this worse. Its recent tail is always empty, and empty reads as zero. Hatch
the provisional range and say so in the subtitle.

\`umbral_viz.heatmap.calendar()\` and \`@umbralmx/umbral-plot\`'s \`calendar()\` both do this.

## The adjacent table

Every chart ships one (UMB-A11Y-003). Top rule 2px \`ink\`, row rules 1px \`border\`, header in Plex
Sans 600.

Text columns align left. Figure columns align right, in Plex Mono with tabular numerals, because
comparing columns is what the table is for.

A delta carries an arrow or a word: \`+9.2% ▲\`. Colour never carries direction alone
(UMB-A11Y-005), and never inside a filled pill (UMB-LAY-001).

A missing cell reads \`sin dato\`. Never \`0\`, never empty (UMB-NUM-006).

The table repeats the chart's exact figures at the same precision. Rounding differently in the two
places publishes two numbers for one fact.

## Rules

${ruleList(inCategory('chart'))}
`);
}

// ── references/voice-and-numbers.md ───────────────────────────────────────
{
  await fs.writeFile(`${REF}/voice-and-numbers.md`, `${HEAD('references/voice-and-numbers.md')}
# Voice, numbers and method

## Voice

Precise, sober, civic-scientific. The numbers carry the argument. **Spanish first**; English only
where the audience earns it. Code, commits and metadata are English.

Chart titles and headlines state the **finding**, as a full sentence — a claim that can be checked
against the figure, and therefore argued with.

Never: hype words, exclamation marks, emoji, rhetorical-question headlines, an adjective where a
number works, or placeholder text in production.

Hedge precisely, next to the claim — not in a footnote:

> Los registros con fecha de hechos en 2025 son 12% más que en 2024; el registro se actualiza
> retroactivamente, así que la cifra de 2025 subirá.

## Numbers (es-MX and en)

| | |
|---|---|
| Thousands / decimals | \`351,057\` · \`3.7\` — Mexico uses the anglophone convention, unlike Spain |
| Axis abbreviation | \`12k\` · \`3.7M\`; write figures in full in prose |
| Percent | \`9.2%\`, tight. Distinguish **per cent** from **percentage points** |
| Precision | 2–3 significant figures unless the data supports more |
| Money | Always name the currency: \`107.6 M MXN\`. In long series use real pesos with a stated base year |
| Dates | ISO in data and axes (\`2026-07\`); prose in text (\`julio de 2026\`). Never \`07/06/2026\` |
| Ranges | \`2010–2026\` with an en dash |
| Censored values | \`≥ 107.6 M\` — a lower bound is not an estimate |

**Zero, null and suppressed are three different things** and must be written differently:
\`0\` · \`sin dato\` · \`suprimido (< umbral)\`. Filling a null with zero is a silent imputation, and
in disappearance data it changes the claim.

## Rates

Any comparison across places of different size uses a **rate per 100,000**, with the denominator
and its year named, plus *n*. Small denominators make rates jump on a single case — publish the
count alongside, or suppress and say so.

## Method

Descriptive verbs («asociado con», «correlaciona») unless there is a named identification strategy
(RCT, diff-in-diff, RD, IV), in which case name it and its key assumption **next to the estimate**.

Disclose gaps; never silently drop or impute. Sensitive topics are handled with dignity: people are
counted, never made spectacle, and never mapped to identifiable individuals.

## Rules

${ruleList([...inCategory('voice'), ...inCategory('numbers'), ...inCategory('method')])}
`);
}

// ── references/surfaces.md ────────────────────────────────────────────────
{
  const bySurface = Object.entries(rules.index.bySurface)
    .sort((a, b) => b[1].length - a[1].length)
    .map(([s, ids]) => `| \`${s}\` | ${ids.length} |`).join('\n');

  await fs.writeFile(`${REF}/surfaces.md`, `${HEAD('references/surfaces.md')}
# Surfaces

| Surface | Mode | The thing that bites |
|---|---|---|
| Web | laboratorio | Self-host fonts; never a CDN |
| Observable Framework | instrumento | \`style\`, never \`theme\`; \`<html>\` ships with no \`lang\` at all |
| Streamlit | instrumento | \`primaryColor\` hits every widget; \`lang="en"\` is hardcoded (superseded) |
| Quarto | laboratorio | Use the generated \`_brand.yml\`; \`fig-alt\` carries the finding |
| Notebook | laboratorio | Use the generated \`.mplstyle\`; the v1.0 one failed contrast |
| Social | instrumento | The card travels without its page — the source line is mandatory |
| Slides | laboratorio | Nothing below 24px, ever |
| GitHub | — | No emoji, no decorative badges, both licence files |
| Email | laboratorio | No CSS variables; inline values copied from the build |

## Observable Framework — the dashboard surface

Framework replaced Streamlit as the dashboard surface in 1.4 (ADR-0004). It is the \`web\` surface,
not a reduced one: UMB-LAY-003, UMB-LAY-009 and UMB-LAY-010 all apply again.

\`\`\`js
// observablehq.config.js
export default {
  style: "observable-framework-instrumento.css",   // copied from assets/
  globalStylesheets: [],                            // its default is Google Fonts
  head: '<script>document.documentElement.lang="es"</script>',
};
\`\`\`

\`\`\`bash
cp assets/observable-framework-instrumento.css src/
\`\`\`

**Ship \`style\`, never \`theme\`.** Framework's own themes derive muted, faint, fainter and faintest
with \`color-mix()\` from one foreground. A derived colour never reaches \`contrast.json\`, so the
gate cannot measure it (UMB-COL-012). The generated stylesheet declares all nine \`--theme-*\`
properties from the tokens instead.

**One file per mode.** \`theme: "dashboard"\` resolves to \`air\` and \`near-midnight\` under
\`prefers-color-scheme\`, which hands the mode to the reader's operating system. The medium sets the
mode (UMB-COL-011). Two stylesheets ship; import exactly one.

**\`<html>\` has no \`lang\` attribute at all.** Not a wrong value — an absent one, which is the worse
case of UMB-A11Y-001. Framework does not expose the tag, so the shim goes in \`head\`.

**Charts need no new work.** Framework renders Observable Plot natively, so \`@umbralmx/umbral-plot\`
applies unchanged: \`theme()\`, \`Frame\`, \`band()\`, \`label()\`.

**Cards.** Framework's dashboard vocabulary is \`.card\` inside \`.grid\`. The generated stylesheet
fixes the 12px radius. It does not make a card the right container for a *list* — that stays rows
separated by 1px rules (UMB-LAY-007).

## Streamlit — the two traps

Streamlit is superseded but still live in \`desaparecidosmx\` and \`pautamx\` until both migrate.

**1. The config keys.** v1.0's brand book rendered them as \`sc-camel-primary-color\`, a PDF-export
artifact. It also set \`font = "sans serif"\`, which is a *valid* Streamlit value meaning Streamlit's
own Source Sans. Copy the generated file instead:

\`\`\`bash
cp assets/streamlit-config.toml .streamlit/config.toml
\`\`\`

**2. \`lang="en"\`.** Streamlit hardcodes it. One call, at the top of the app:

\`\`\`python
import streamlit.components.v1 as components
components.html("<script>window.parent.document.documentElement.lang='es';</script>", height=0)
\`\`\`

**On \`signal\` in Streamlit:** \`primaryColor\` is applied to sliders, chips, tabs, links and focus
rings simultaneously. No configuration restricts it to one element. So UMB-COL-004 is scoped to the
data layer — in a dashboard it means *one series in signal per chart*. Widget chrome is exempt.

## Rule counts by surface

| Surface | Rules |
|---|---|
${bySurface}
`);
}

// ── references/components.md ──────────────────────────────────────────────
// Parsed out of guide/16-componentes.md so the verdicts have one source. The
// chapter is normative; this is its English index for an agent.
{
  const chapter = await fs.readFile('guide/16-componentes.md', 'utf8');
  const rows = [...chapter.matchAll(/^\| `([a-z-]+)` \| (adopta|adapta|rechaza) \| (.+?) \|$/gm)]
    .map((m) => ({ name: m[1], verdict: m[2], note: m[3] }));
  const OUT_OF_SCOPE = ['attachment', 'bubble', 'message', 'message-scroller',
    'questionnaire', 'marker'];
  const EN = { adopta: 'adopt', adapta: 'adapt', rechaza: 'reject' };
  const count = (v) => rows.filter((r) => r.verdict === v).length;
  const table = (v) => rows.filter((r) => r.verdict === v)
    .map((r) => `| \`${r.name}\` | ${r.note} |`).join('\n');

  await fs.writeFile(`${REF}/components.md`, `${HEAD('references/components.md')}
# Components

The shadcn/ui catalogue mapped against the rules. The normative text is
\`guide/16-componentes.md\`; this is its index.

shadcn/ui is copied code, not a dependency. Take the **form** and the accessibility contract. Never
take the values — a shadcn component writes its colours and radii into Tailwind classes, which is
UMB-COL-002 and UMB-PRO-003 by construction.

## The five systematic corrections

They apply to every component. Apply them before reading any entry below.

| | shadcn ships | Umbral applies | Rule |
|---|---|---|---|
| 1 | \`rounded-md\`, \`rounded-xl\`, \`rounded-full\` | 2px radius ceiling; a pill is banned outright | UMB-LAY-001 |
| 2 | \`shadow-xs\`, \`shadow-sm\` | No shadows; 1px rules carry the structure | UMB-LAY-002 |
| 3 | Control heights \`h-7\` to \`h-10\` | 44px touch target minimum | UMB-A11Y-006 |
| 4 | Tailwind palette and its own variables | Every colour from the tokens | UMB-COL-002 |
| 5 | \`font-semibold\` headings | Space Grotesk 500; 600 is for small labels only | UMB-TYP-001 |

No default shadcn control height reaches 44px. The touch target may exceed the visible border, so
the fix does not force a fatter control.

## Overlays

\`dialog\`, \`alert-dialog\`, \`sheet\`, \`drawer\`, \`popover\` and \`command\` share one contract
(UMB-A11Y-008): focus enters on open, is trapped while open, Escape closes, and focus returns to
the control that opened it. Radix supplies this in React. It has to be written by hand elsewhere.

## Reject (${count('rechaza')})

| Component | Instead |
|---|---|
${table('rechaza')}

## Adapt (${count('adapta')})

| Component | The specific change |
|---|---|
${table('adapta')}

## Adopt (${count('adopta')})

Form is fine. Apply the five corrections and nothing else.

| Component | Note |
|---|---|
${table('adopta')}

## Out of scope (${OUT_OF_SCOPE.length})

${OUT_OF_SCOPE.map((n) => `\`${n}\``).join(' · ')}

The catalogue's chat pieces. Umbral does not publish a conversational product.

## Open

OQ-011 asks what a transient message may carry. OQ-012 asks how a disabled control meets the 4.5:1
floor, which UMB-COL-005 states without an exception.
`);
  console.log(`  components: ${rows.length} verdicts (${count('adopta')} adopt, `
    + `${count('adapta')} adapt, ${count('rechaza')} reject)`);
}

// ── references/terminology.md ─────────────────────────────────────────────
{
  const src = await fs.readFile('guide/15-terminologia.md', 'utf8');
  const body = src
    .replace(/^---[\s\S]*?---\n/, '')
    .replace(/\{\{<\s*include[^>]*>\}\}\n?/g, '')
    .replace(/^:::.*$/gm, '');
  await fs.writeFile(`${REF}/terminology.md`, `${HEAD('references/terminology.md')}
> Binding controlled vocabulary. Mirrored from \`guide/15-terminologia.md\`.
> The distinctions here are legal and ethical, not stylistic — see UMB-MET-005.
${body}`);
}

// ── references/checklist.md ───────────────────────────────────────────────
{
  const human = rules.rules.filter((r) => r.severity === 'error' && r.check.type !== 'automated');
  const auto = rules.rules.filter((r) => r.severity === 'error' && r.check.type === 'automated');
  await fs.writeFile(`${REF}/checklist.md`, `${HEAD('references/checklist.md')}
# Pre-ship checklist

${auto.length} \`error\` rules are checked by \`umbral-lint\` and the token build. These
${human.length} need human judgement:

${human.map((r) => `- [ ] **${r.id}** — ${r.title_en}`).join('\n')}

## Always

- [ ] Correct mode for the surface — light by default
- [ ] Every colour, font and spacing value from the tokens; none hand-typed
- [ ] Display is Space Grotesk 500, never 700
- [ ] Every chart: finding-title + subtitle + source + licence + CSV + \`aria-label\`
- [ ] Uncertainty visible wherever there is a projection or estimate
- [ ] One \`signal\` element in the data layer per view
- [ ] \`lang\` correct
- [ ] Spanish first; terminology per \`references/terminology.md\`
- [ ] Causal language matches the identification strategy actually used
- [ ] Nothing from the never list
`);
}

// ── pinned assets ─────────────────────────────────────────────────────────
const ASSET_COPIES = [
  ['tokens/build/tokens.json', 'tokens.json'],
  ['tokens/build/tokens.css', 'tokens.css'],
  ['tokens/build/tokens.py', 'tokens.py'],
  ['tokens/build/contrast.json', 'contrast.json'],
  ['tokens/build/umbral-laboratorio.mplstyle', 'umbral-laboratorio.mplstyle'],
  ['tokens/build/umbral-instrumento.mplstyle', 'umbral-instrumento.mplstyle'],
  ['tokens/build/plotly-umbral-laboratorio.json', 'plotly-umbral-laboratorio.json'],
  ['tokens/build/plotly-umbral-instrumento.json', 'plotly-umbral-instrumento.json'],
  ['tokens/build/streamlit-config.toml', 'streamlit-config.toml'],
  ['tokens/build/observable-framework-laboratorio.css', 'observable-framework-laboratorio.css'],
  ['tokens/build/observable-framework-instrumento.css', 'observable-framework-instrumento.css'],
  ['tokens/build/_brand.yml', '_brand.yml'],
  ['rules/rules.json', 'rules.json'],
];
for (const [from, to] of ASSET_COPIES) {
  await fs.copyFile(from, path.join(AST, to));
}
for (const f of await fs.readdir('assets/logo')) {
  await fs.copyFile(path.join('assets/logo', f), path.join(AST, f));
}

// ── dist/CLAUDE.snippet.md ────────────────────────────────────────────────
{
  const t = tokens.mode.laboratorio;
  await fs.writeFile('dist/CLAUDE.snippet.md', `<!-- Umbral design system ${TAG} — paste into a downstream repo's CLAUDE.md.
     GENERATED; regenerate from umbralmx/umbral-style-guide rather than editing. -->

## Umbral brand — the minimum

This repo follows the Umbral design system, pinned at **${TAG}**.
Full guide: https://github.com/umbralmx/umbral-style-guide/tree/${TAG}/guide

**Load the skill** before producing anything visual: copy
\`umbral-style-guide/skills/umbral-brand/\` into \`.claude/skills/\`, or install the packaged
\`.skill\` from the release.

**Never hand-type a colour, font or spacing value.** Import them:

\`\`\`
${RAW}/tokens/build/tokens.css     # web
${RAW}/tokens/build/tokens.json    # anything
${RAW}/tokens/build/tokens.py      # Python / Streamlit / notebooks
${RAW}/tokens/build/tokens.R       # R / Quarto
${RAW}/tokens/build/observable-framework-instrumento.css   # Observable Framework
${RAW}/tokens/build/streamlit-config.toml
${RAW}/rules/rules.json            # the ${rules.counts.total} rules, machine-readable
\`\`\`

Pin the tag. Never point at \`main\` — a token change would land without warning.

**Two modes.** \`laboratorio\` (light) is the default: site, reports, documents, decks.
\`instrumento\` (dark) for dashboards, social cards and big-stat slides. Switch with
\`data-mode="instrumento"\`; never mix them inside one panel.

**The rules broken most often:**

- \`signal\` (\`${t.signal}\`) marks **one** element of the data layer per view.
- Use \`signal-text\` (\`${t['signal-text']}\`) for text and direct series labels — \`signal\` only
  clears 3:1, and labels are small text needing 4.5:1.
- Chart titles state the finding as a sentence, not the topic.
- Every chart: subtitle (geography · period · unit), source line with licence and snapshot tag,
  \`aria-label\` with the finding, and a downloadable CSV.
- Space Grotesk **500** for display — never 700. Self-host the fonts; never a CDN.
- Uncertainty is visible: bands at ${tokens.uncertaintyBandOpacity} opacity, dashed past the
  present, a dashed \`hoy\` rule.
- Causal verbs only with a named identification strategy. Otherwise «asociado con».
- \`lang="es"\`. Never encode meaning by colour alone.
- Spanish first. Sensitive terminology is binding — see \`guide/15-terminologia.md\`.
- One statement per sentence, 25 words maximum. Active voice. One word for one thing.
- Section labels in mono lowercase. Lists are rows with 1px rules, not cards.
- A diagram shows a mechanism, drawn in 1px rules and text. No icons, no fill, no rounded nodes.
- A delta carries an arrow or a word. Colour never carries it alone, and never inside a pill.

**Never:** emoji · gradients · drop shadows · pill buttons · pure black or white · 700-weight
display · a chart without its source · a figure that cannot be rebuilt from raw data.
`);
}

// ── READMEs for the generated folders ─────────────────────────────────────
await fs.writeFile(`${REF}/README.md`, `# \`references/\`

**Generated by \`build/skill.mjs\`. Do not edit.**

Loaded on demand — the agent reads \`SKILL.md\` first and pulls one of these in when the task calls
for it.

| | Read it when |
|---|---|
| \`color.md\` | Choosing any colour |
| \`charts.md\` | **Before writing any chart code** |
| \`voice-and-numbers.md\` | Writing prose, numbers, dates or rates |
| \`surfaces.md\` | Targeting web, Observable Framework, Quarto, notebooks, social, slides, GitHub or email |
| \`components.md\` | Building any UI component — the shadcn/ui catalogue, mapped |
| \`terminology.md\` | Anything touching disappearances, crime or victims — binding |
| \`checklist.md\` | Finishing up |

All seven are generated from \`tokens/build/\`, \`rules/rules.json\` and \`guide/\`, so the skill cannot
state a value or a rule the normative layer does not. The v1.0 skill restated token values in prose
and kept handing out colours that failed contrast long after they were known to be wrong.
`);

await fs.writeFile(`${AST}/README.md`, `# \`assets/\`

**Generated by \`build/skill.mjs\`. Do not edit.** Pinned copies of the normative outputs at
${TAG}, so the skill works offline and cannot disagree with the repo it came from.

| | |
|---|---|
| \`tokens.json\` \`tokens.css\` \`tokens.py\` | The values. Read these; never retype a hex. |
| \`contrast.json\` | The generated contrast matrix — what \`check_contrast.py --audit\` reads |
| \`rules.json\` | All ${rules.counts.total} rules, machine-readable |
| \`umbral-*.mplstyle\` \`plotly-umbral-*.json\` | Chart themes, per mode |
| \`observable-framework-*.css\` | Framework \`style\` — copy ONE into the source root |
| \`streamlit-config.toml\` | Copy to \`.streamlit/config.toml\` — real keys, correct font |
| \`_brand.yml\` | Quarto brand file |
| \`umbral-*.svg\` | Logo variants, generated from the 5:44 spec |
`);

await fs.writeFile('dist/README.md', `# \`dist/\`

**Generated by \`build/skill.mjs\`. Do not edit.**

| | |
|---|---|
| \`CLAUDE.snippet.md\` | ~40 lines. The minimum any downstream Umbral repo's \`CLAUDE.md\` needs. |

Paste it into the \`CLAUDE.md\` of a repo that consumes the design system. It is **pinned to
${TAG}** and points at raw token URLs at that tag rather than at \`main\`, so a token change cannot
land in a downstream repo without someone choosing it.

Regenerate after a version bump:

\`\`\`bash
npm run build:skill
\`\`\`
`);

const refs = (await fs.readdir(REF)).filter((f) => f.endsWith('.md') && f !== 'README.md');
const assets = await fs.readdir(AST);
console.log(`skill: ${refs.length} references, ${assets.length} pinned assets, `
  + `dist/CLAUDE.snippet.md (pinned ${TAG})`);
