/**
 * Umbral token build.
 *
 *   tokens/src/*.tokens.json   (authored, W3C DTCG)
 *        ↓  this script
 *   tokens/build/*             (generated, committed, never hand-edited)
 *
 * Run with `npm run build:tokens`. Every downstream target is produced here, so a
 * colour can never be stated in two places and drift — which is exactly how v1.0's
 * mplstyle ended up with a different third series colour from its own brand book.
 */
import StyleDictionary from 'style-dictionary';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import {
  hexToOklch, oklchToHex, gamutFit, contrast, floorRatio,
  simulateCvd, oklabDistance, CVD_KINDS,
} from './lib/color.mjs';

const MODES = ['laboratorio', 'instrumento'];
const OUT = 'tokens/build';

// Style Dictionary v4 reads the DTCG spec natively, so $value / $type / $extensions
// are used directly below — no parser or key rewriting needed.

// ── ramp expansion ────────────────────────────────────────────────────────
// Ramp specs are authored; the concrete steps are derived here so the ramp can be
// rebuilt if a background changes, instead of being a frozen list nobody dares touch.
const lerp = (a, b, t) => a + (b - a) * t;

function expandSequential(spec, mode) {
  const { steps, hue } = spec;
  const { lightness, chroma } = spec[mode];
  return Array.from({ length: steps }, (_, i) => {
    const t = steps === 1 ? 0 : i / (steps - 1);
    return gamutFit(lerp(lightness[0], lightness[1], t), lerp(chroma[0], chroma[1], t), hue);
  });
}

function expandDiverging(spec, mode) {
  const { steps, hueLow, hueHigh } = spec;
  const { lightness, chroma } = spec[mode];
  const mid = (steps - 1) / 2;
  return Array.from({ length: steps }, (_, i) => {
    if (i === mid) return gamutFit(lightness[1], chroma[1], hueLow);
    const low = i < mid;
    const t = low ? 1 - i / mid : (i - mid) / mid;
    // t: 0 at the neutral midpoint, 1 at the extreme
    const L = lerp(lightness[1], low ? lightness[0] : lightness[2], t);
    const C = lerp(chroma[1], low ? chroma[0] : chroma[2], t);
    return gamutFit(L, C, low ? hueLow : hueHigh);
  });
}

StyleDictionary.registerPreprocessor({
  name: 'umbral/expand-ramps',
  preprocessor: (dict) => {
    const ramps = dict.ramp;
    if (!ramps) return dict;
    for (const kind of ['sequential', 'diverging']) {
      if (!ramps[kind]) continue;
      for (const [name, node] of Object.entries(ramps[kind])) {
        const spec = node.$extensions?.umbral?.derive;
        if (!spec) continue;
        for (const mode of MODES) {
          const hexes = spec.kind === 'diverging'
            ? expandDiverging(spec, mode)
            : expandSequential(spec, mode);
          node[mode] = {};
          hexes.forEach((hex, i) => {
            node[mode][String(i)] = {
              $value: hex,
              $type: 'color',
              $description: `${kind} ${name} · ${mode} · step ${i + 1}/${hexes.length} · generated`,
            };
          });
        }
        delete node.$extensions.umbral.derive.laboratorio;
        delete node.$extensions.umbral.derive.instrumento;
      }
    }
    return dict;
  },
});

// ── helpers shared by the formats ─────────────────────────────────────────
const tok = (d, p) => d.allTokens.find((t) => t.path.join('.') === p);
const val = (d, p) => tok(d, p)?.$value;

function semantic(d, mode) {
  const out = {};
  for (const t of d.allTokens) {
    if (t.path[0] === 'semantic' && t.path[1] === mode) out[t.path[2]] = t.$value;
  }
  return out;
}

function rampSteps(d, kind, name, mode) {
  return d.allTokens
    .filter((t) => t.path[0] === 'ramp' && t.path[1] === kind
      && t.path[2] === name && t.path[3] === mode)
    .sort((a, b) => Number(a.path[4]) - Number(b.path[4]))
    .map((t) => t.$value);
}

function roleOf(d, mode, name) {
  return tok(d, `semantic.${mode}.${name}`)?.$extensions?.umbral?.contrastRole ?? 'unknown';
}

const HEADER = (what) => `${what} — GENERATED from tokens/src/. Do not edit.
Umbral design system · https://github.com/umbralmx/umbral-style-guide
Code MIT · content CC BY 4.0`;

const seriesOrder = (d, mode) => d.allTokens
  .filter((t) => t.path[0] === 'semantic' && t.path[1] === mode
    && t.$extensions?.umbral?.series)
  .sort((a, b) => a.$extensions.umbral.series - b.$extensions.umbral.series)
  .map((t) => ({ name: t.path[2], hex: t.$value }));

// ── formats ───────────────────────────────────────────────────────────────
StyleDictionary.registerFormat({
  name: 'umbral/css',
  format: ({ dictionary: d }) => {
    const decl = (o, ind = '  ') => Object.entries(o)
      .map(([k, v]) => `${ind}--u-${k}: ${v};`).join('\n');
    const nonColor = [
      ...d.allTokens.filter((t) => t.path[0] === 'font' && t.path[1] === 'family')
        .map((t) => [`font-${t.path[2]}`, t.$value.map((f) => (f.includes(' ') ? `'${f}'` : f)).join(', ')]),
      ...d.allTokens.filter((t) => t.path[0] === 'font' && t.path[1] === 'weight')
        .map((t) => [`weight-${t.path[2]}`, t.$value]),
      ...d.allTokens.filter((t) => t.path[0] === 'font' && t.path[1] === 'tracking')
        .map((t) => [`tracking-${t.path[2]}`, t.$value]),
      ...d.allTokens.filter((t) => t.path[0] === 'font' && t.path[1] === 'size')
        .map((t) => [`size-${t.path[2]}`, t.$value]),
      ...d.allTokens.filter((t) => t.path[0] === 'space' && t.path[1] !== 'unit')
        .map((t) => [`space-${t.path[1]}`, t.$value]),
      ...d.allTokens.filter((t) => t.path[0] === 'layout')
        .map((t) => [`${t.path[1]}`, t.$value]),
      ['opacity-uncertainty', val(d, 'opacity.uncertainty-band')],
    ];
    const ramps = (mode) => {
      const lines = [];
      for (const [kind, name] of [['sequential', 'signal'], ['sequential', 'model'], ['diverging', 'alert-signal']]) {
        rampSteps(d, kind, name, mode).forEach((hex, i) => {
          lines.push(`  --u-ramp-${name === 'alert-signal' ? 'div' : `seq-${name}`}-${i}: ${hex};`);
        });
      }
      return lines.join('\n');
    };
    return `/*\n${HEADER('tokens.css')}\n*/\n\n:root {\n`
      + `  /* ── modo laboratorio (light) — DEFAULT ── */\n${decl(semantic(d, 'laboratorio'))}\n\n`
      + `${ramps('laboratorio')}\n\n`
      + `  /* ── type, space, layout — identical in both modes ── */\n`
      + `${nonColor.map(([k, v]) => `  --u-${k}: ${v};`).join('\n')}\n}\n\n`
      + `[data-mode="instrumento"], .u-dark {\n`
      + `  /* ── modo instrumento (dark) ── */\n${decl(semantic(d, 'instrumento'))}\n\n`
      + `${ramps('instrumento')}\n}\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/scss',
  format: ({ dictionary: d }) => {
    const lines = [`// ${HEADER('_tokens.scss').split('\n').join('\n// ')}`, ''];
    for (const mode of MODES) {
      lines.push(`$umbral-${mode}: (`);
      for (const [k, v] of Object.entries(semantic(d, mode))) lines.push(`  "${k}": ${v},`);
      lines.push(');', '');
    }
    lines.push(`$umbral-font-display: ${val(d, 'font.family.display').map((f) => `"${f}"`).join(', ')};`);
    lines.push(`$umbral-font-body: ${val(d, 'font.family.body').map((f) => `"${f}"`).join(', ')};`);
    lines.push(`$umbral-font-mono: ${val(d, 'font.family.mono').map((f) => `"${f}"`).join(', ')};`);
    lines.push(`$umbral-weight-display: ${val(d, 'font.weight.display')};`);
    lines.push(`$umbral-radius-max: ${val(d, 'layout.radius-max')};`);
    lines.push(`$umbral-measure: ${val(d, 'layout.measure')};`);
    return `${lines.join('\n')}\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/json',
  format: ({ dictionary: d }) => {
    const out = {
      $generated: HEADER('tokens.json'),
      font: {
        display: val(d, 'font.family.display')[0],
        body: val(d, 'font.family.body')[0],
        mono: val(d, 'font.family.mono')[0],
        displayWeight: val(d, 'font.weight.display'),
        displayTracking: val(d, 'font.tracking.display'),
      },
      scale: {
        unit: parseInt(val(d, 'space.unit'), 10),
        radius: parseInt(val(d, 'layout.radius'), 10),
        radiusMax: parseInt(val(d, 'layout.radius-max'), 10),
        rule: parseInt(val(d, 'layout.rule'), 10),
        measure: val(d, 'layout.measure'),
      },
      uncertaintyBandOpacity: val(d, 'opacity.uncertainty-band'),
      mode: {},
      ramp: {},
    };
    for (const mode of MODES) {
      out.mode[mode] = semantic(d, mode);
      out.ramp[mode] = {
        sequentialSignal: rampSteps(d, 'sequential', 'signal', mode),
        sequentialModel: rampSteps(d, 'sequential', 'model', mode),
        diverging: rampSteps(d, 'diverging', 'alert-signal', mode),
      };
      out.mode[mode].series = seriesOrder(d, mode).map((s) => s.hex);
    }
    return `${JSON.stringify(out, null, 2)}\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/python',
  format: ({ dictionary: d }) => {
    const py = (o) => `{\n${Object.entries(o).map(([k, v]) => `        ${JSON.stringify(k)}: ${JSON.stringify(v)},`).join('\n')}\n    }`;
    return `"""${HEADER('tokens.py')}"""\n\n`
      + `FONT = {\n    "display": ${JSON.stringify(val(d, 'font.family.display')[0])},\n`
      + `    "body": ${JSON.stringify(val(d, 'font.family.body')[0])},\n`
      + `    "mono": ${JSON.stringify(val(d, 'font.family.mono')[0])},\n`
      + `    "display_weight": ${val(d, 'font.weight.display')},\n}\n\n`
      + MODES.map((m) => `${m.toUpperCase()} = ${py(semantic(d, m))}`).join('\n\n')
      + `\n\nMODE = {"laboratorio": LABORATORIO, "instrumento": INSTRUMENTO}\n\n`
      + MODES.map((m) => `SERIES_${m.toUpperCase()} = ${JSON.stringify(seriesOrder(d, m).map((s) => s.hex))}`).join('\n')
      + '\n\n'
      + MODES.map((m) => `RAMP_${m.toUpperCase()} = {\n`
        + `    "sequential_signal": ${JSON.stringify(rampSteps(d, 'sequential', 'signal', m))},\n`
        + `    "sequential_model": ${JSON.stringify(rampSteps(d, 'sequential', 'model', m))},\n`
        + `    "diverging": ${JSON.stringify(rampSteps(d, 'diverging', 'alert-signal', m))},\n}`).join('\n')
      + `\n\nUNCERTAINTY_BAND_OPACITY = ${val(d, 'opacity.uncertainty-band')}\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/r',
  format: ({ dictionary: d }) => {
    const rl = (o) => Object.entries(o).map(([k, v]) => `  \`${k}\` = "${v}"`).join(',\n');
    return `# ${HEADER('tokens.R').split('\n').join('\n# ')}\n\n`
      + MODES.map((m) => `umbral_${m} <- list(\n${rl(semantic(d, m))}\n)`).join('\n\n')
      + `\n\numbral_modes <- list(laboratorio = umbral_laboratorio, instrumento = umbral_instrumento)\n\n`
      + MODES.map((m) => `umbral_series_${m} <- c(${seriesOrder(d, m).map((s) => `"${s.hex}"`).join(', ')})`).join('\n')
      + '\n\n'
      + MODES.map((m) => `umbral_ramp_${m} <- list(\n`
        + `  sequential_signal = c(${rampSteps(d, 'sequential', 'signal', m).map((h) => `"${h}"`).join(', ')}),\n`
        + `  sequential_model = c(${rampSteps(d, 'sequential', 'model', m).map((h) => `"${h}"`).join(', ')}),\n`
        + `  diverging = c(${rampSteps(d, 'diverging', 'alert-signal', m).map((h) => `"${h}"`).join(', ')})\n)`).join('\n')
      + `\n\numbral_font <- list(display = "${val(d, 'font.family.display')[0]}", body = "${val(d, 'font.family.body')[0]}", mono = "${val(d, 'font.family.mono')[0]}")\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/mplstyle',
  format: ({ dictionary: d, options }) => {
    const m = options.mode;
    const s = semantic(d, m);
    const series = seriesOrder(d, m).map((x) => x.hex.replace('#', ''));
    return `# ${HEADER(`umbral-${m}.mplstyle`).split('\n').join('\n# ')}\n`
      + `#\n# v1.0's umbral.mplstyle set xtick/ytick colour to the caption token at 2.37:1\n`
      + `# and used it as the third series. Both are corrected here — see\n`
      + `# audit/2026-07-conformance.md §3.5 and open-questions.md OQ-008.\n\n`
      + `figure.facecolor: none\naxes.facecolor: none\n`
      + `axes.edgecolor: ${s.baseline.replace('#', '')}\naxes.linewidth: 1\n`
      + `axes.grid: True\naxes.grid.axis: y\n`
      + `grid.color: ${s.gridline.replace('#', '')}\ngrid.linewidth: 1\n`
      + `axes.spines.top: False\naxes.spines.right: False\naxes.spines.left: False\n`
      + `font.family: ${val(d, 'font.family.body')[0]}\nfont.size: 12\n`
      + `axes.titlesize: 16\naxes.titleweight: medium\naxes.titlelocation: left\n`
      + `xtick.color: ${s.caption.replace('#', '')}\nytick.color: ${s.caption.replace('#', '')}\n`
      + `xtick.labelsize: 12\nytick.labelsize: 12\n`
      + `text.color: ${s.ink.replace('#', '')}\n`
      + `axes.prop_cycle: cycler('color', [${series.map((h) => `'${h}'`).join(', ')}])\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/plotly',
  format: ({ dictionary: d, options }) => {
    const m = options.mode;
    const s = semantic(d, m);
    const font = val(d, 'font.family.body')[0];
    const mono = val(d, 'font.family.mono')[0];
    return `${JSON.stringify({
      $generated: HEADER(`plotly-umbral-${m}.json`),
      layout: {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        colorway: seriesOrder(d, m).map((x) => x.hex),
        font: { family: font, color: s.ink, size: 13 },
        title: { font: { family: val(d, 'font.family.display')[0], size: 22 }, x: 0, xanchor: 'left' },
        xaxis: {
          showgrid: false,
          zeroline: false,
          linecolor: s.baseline,
          tickfont: { family: mono, size: 12, color: s.caption },
        },
        yaxis: {
          showgrid: true,
          gridcolor: s.gridline,
          zerolinecolor: s.baseline,
          linewidth: 0,
          tickfont: { family: mono, size: 12, color: s.caption },
        },
        showlegend: false,
        margin: { l: 52, b: 34, t: 64, r: 24 },
        colorscale: {
          sequential: rampSteps(d, 'sequential', 'signal', m).map((h, i, a) => [i / (a.length - 1), h]),
          diverging: rampSteps(d, 'diverging', 'alert-signal', m).map((h, i, a) => [i / (a.length - 1), h]),
        },
      },
    }, null, 2)}\n`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/altair',
  format: ({ dictionary: d }) => {
    const block = (m) => {
      const s = semantic(d, m);
      return `    "${m}": {
        "background": "${s.base}",
        "title": {"font": FONT_DISPLAY, "fontSize": 22, "fontWeight": ${val(d, 'font.weight.display')}, "anchor": "start", "color": "${s.ink}"},
        "axis": {
            "labelFont": FONT_MONO, "labelFontSize": 12, "labelColor": "${s.caption}",
            "titleFont": FONT_BODY, "titleFontSize": 12, "titleColor": "${s.muted}",
            "domainColor": "${s.baseline}", "gridColor": "${s.gridline}",
            "tickColor": "${s.baseline}", "grid": False,
        },
        "axisY": {"grid": True, "domain": False, "ticks": False},
        "axisX": {"grid": False},
        "range": {
            "category": ${JSON.stringify(seriesOrder(d, m).map((x) => x.hex))},
            "heatmap": ${JSON.stringify(rampSteps(d, 'sequential', 'signal', m))},
            "ramp": ${JSON.stringify(rampSteps(d, 'sequential', 'signal', m))},
            "diverging": ${JSON.stringify(rampSteps(d, 'diverging', 'alert-signal', m))},
        },
        "legend": {"disable": True},
        "view": {"stroke": None},
    },`;
    };
    return `"""${HEADER('altair-umbral.py')}

Direct series labels are the Umbral default, so legends are disabled in this theme.
If you genuinely need one, re-enable it explicitly at the chart level.
"""
import altair as alt

FONT_DISPLAY = ${JSON.stringify(val(d, 'font.family.display')[0])}
FONT_BODY = ${JSON.stringify(val(d, 'font.family.body')[0])}
FONT_MONO = ${JSON.stringify(val(d, 'font.family.mono')[0])}

_CONFIG = {
${MODES.map(block).join('\n')}
}


def umbral_theme(mode: str = "laboratorio"):
    """Return an Altair theme config for the given Umbral mode."""
    return {"config": _CONFIG[mode]}


def enable(mode: str = "laboratorio") -> None:
    """Register and activate the Umbral theme."""
    alt.themes.register("umbral", lambda: umbral_theme(mode))
    alt.themes.enable("umbral")
`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/streamlit',
  format: ({ dictionary: d }) => {
    const s = semantic(d, 'instrumento');
    return `# ${HEADER('streamlit-config.toml').split('\n').join('\n# ')}
#
# Copy to .streamlit/config.toml.
#
# Two corrections to the v1.0 brand book (p.10):
#   1. Its keys were rendered "sc-camel-primary-color" etc. — a camelCase artifact
#      of the PDF export. The real Streamlit keys are below.
#   2. It set font = "sans serif", which is a VALID Streamlit value meaning
#      Streamlit's own Source Sans — not a mangling, just wrong. That is why
#      pautamx renders Source Sans today. Fixed here.
#
# Note: Streamlit maps primaryColor onto every widget accent simultaneously, so
# the one-signal-per-view rule is scoped to the data layer — see OQ-002.

[theme]
base                     = "dark"
primaryColor             = "${s.signal}"
backgroundColor          = "${s.base}"
secondaryBackgroundColor = "${s.panel}"
textColor                = "${s.ink}"
font                     = "${val(d, 'font.family.body')[0]}, sans-serif"
`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/framework',
  format: ({ dictionary: d, options }) => {
    const { mode } = options;
    const s = semantic(d, mode);
    const stack = (k) => val(d, `font.family.${k}`)
      .map((f) => (f.includes(' ') ? `"${f}"` : f)).join(', ');
    const light = mode === 'laboratorio';
    // Aligned trailing comments: each names the token the value came from, so a
    // reader can check the mapping without opening tokens.json.
    const themeMap = [
      ['--theme-foreground', s.ink, 'ink'],
      ['--theme-background', s.base, 'base'],
      ['--theme-background-alt', s.panel, 'panel'],
      ['--theme-foreground-alt', s.ink, 'ink — headings'],
      ['--theme-foreground-muted', s.caption, 'caption — secondary TEXT, clears 4.5:1'],
      ['--theme-foreground-faint', s.baseline, 'baseline'],
      ['--theme-foreground-fainter', s.border, 'border'],
      ['--theme-foreground-faintest', s.gridline, 'gridline'],
      ['--theme-foreground-focus', s['signal-text'], 'signal-text, not signal — links are text'],
    ];
    const w = Math.max(...themeMap.map(([k, v]) => `  ${k}: ${v};`.length));
    const themeDecls = themeMap
      .map(([k, v, why]) => `${`  ${k}: ${v};`.padEnd(w)}  /* ${why} */`).join('\n');
    return `/*
${HEADER(`observable-framework-${mode}.css`)}

Observable Framework — modo ${mode} (${light ? 'light' : 'dark'}).

  // observablehq.config.js
  export default {
    style: "observable-framework-${mode}.css",
    globalStylesheets: []
  };

Three deliberate choices are baked in here.

1. This is a \`style\`, not a \`theme\`. \`style\` overrides \`theme\`, so no built-in
   theme loads. Framework's themes derive muted / faint / fainter / faintest with
   color-mix() from one foreground, and a derived colour never reaches
   contrast.json, so the gate cannot measure it (UMB-COL-012). All nine
   --theme-* properties are declared below instead.

2. One file per mode. Import exactly one. Framework's default pairs a light and a
   dark theme under prefers-color-scheme, which lets the reader's operating system
   pick the mode. The medium picks the mode (UMB-COL-011).

3. \`globalStylesheets\` must be []. Its default loads Source Serif 4 from Google
   Fonts. Self-host the three families instead (UMB-TYP-005).
*/

@import url("observablehq:default.css");

:root {
  color-scheme: ${light ? 'light' : 'dark'};

  /* ── the nine --theme-* properties: declared, never derived (UMB-COL-012) ── */
${themeDecls}

  /* Framework's four accents. Umbral has no green and no yellow, so .green and
     .yellow render as plain ink: they encode meaning by colour alone, which
     UMB-A11Y-005 forbids, and rendering them prettily would hide that. */
  --theme-blue: ${s.model};
  --theme-red: ${s.alert};
  --theme-green: ${s.ink};
  --theme-yellow: ${s.ink};

  /* ── type ── */
  --u-font-display: ${stack('display')};
  /* Umbral has no serif. --serif points at the body stack so a stray var(--serif)
     left over from a Framework example cannot summon Times (UMB-TYP-002). */
  --serif: ${stack('body')};
  --sans-serif: ${stack('body')};
  --monospace: ${stack('mono')};
  --monospace-font: 14px/1.5 var(--monospace);

  /* A row of KPIs is compared column against column, so .big is mono, not
     display (UMB-TYP-004). Framework's default is 700 weight (UMB-TYP-001). */
  --font-big: ${val(d, 'font.weight.mono-medium')} 32px/1 var(--monospace);
  --font-small: 14px var(--sans-serif);

  --u-measure: ${val(d, 'layout.measure')};
  --u-radius-max: ${val(d, 'layout.radius-max')};
  --u-touch-target: ${val(d, 'layout.touch-target')};
}

/* ── corrections to Framework's defaults ── */

/* global.css sets 17px/1.5 var(--serif) on the body. */
body {
  font: 16px/1.5 var(--sans-serif);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--u-font-display);
  font-weight: ${val(d, 'font.weight.display')};
  letter-spacing: ${val(d, 'font.tracking.display')};
}

.big {
  font-variant-numeric: tabular-nums;
}

/* card.css sets border-radius: 0.75rem — twelve times the maximum (UMB-LAY-001).
   A card is still not the way to render a LIST; that stays rows separated by 1px
   rules (UMB-LAY-007). */
.card {
  border-radius: var(--u-radius-max);
  border-color: var(--theme-foreground-fainter);
  box-shadow: none;
}

/* layout.css paints the footer in --theme-foreground-faint, which is furniture and
   is exempt from 4.5:1. Footer text is text (UMB-COL-005). */
#observablehq-footer {
  color: var(--theme-foreground-muted);
}

/* Framework leaves prose unconstrained out to --observablehq-max-width, so the
   measure has to be set here (UMB-LAY-003). Wide elements opt back out. */
#observablehq-main > p,
#observablehq-main > ul,
#observablehq-main > ol,
#observablehq-main > blockquote,
#observablehq-main > h1,
#observablehq-main > h2,
#observablehq-main > h3 {
  max-width: var(--u-measure);
}

#observablehq-main > .grid,
#observablehq-main > figure,
#observablehq-main > table,
#observablehq-main > pre {
  max-width: none;
}

/* UMB-A11Y-006 — 44px is a floor, not a suggestion. Framework's sidebar links and
   form inputs ship well under it. */
#observablehq-sidebar a,
input, select, button, .observablehq-input input {
  min-height: var(--u-touch-target);
}

/* UMB-A11Y-006 — focus is drawn in signal, and it is drawn everywhere. */
:focus-visible {
  outline: 2px solid var(--theme-foreground-focus);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
`;
  },
});

StyleDictionary.registerFormat({
  name: 'umbral/quarto-brand',
  format: ({ dictionary: d }) => {
    const l = semantic(d, 'laboratorio');
    const i = semantic(d, 'instrumento');
    return `# ${HEADER('_brand.yml').split('\n').join('\n# ')}
#
# Quarto brand file. Include with "brand: _brand.yml" in _quarto.yml.
# Documents are modo laboratorio (light) by default — see guide/14-superficies/quarto.md.

meta:
  name: umbral_
  link: https://umbral.mx

logo:
  images:
    isotype: assets/logo/umbral-isotype-light.svg
    lockup: assets/logo/umbral-lockup-light.svg
  small: isotype
  medium: lockup
  large: lockup

color:
  palette:
    ink: "${l.ink}"
    base: "${l.base}"
    panel: "${l.panel}"
    border: "${l.border}"
    muted: "${l.muted}"
    caption: "${l.caption}"
    signal: "${l.signal}"
    signal-text: "${l['signal-text']}"
    model: "${l.model}"
    alert: "${l.alert}"
    ink-dark: "${i.ink}"
    base-dark: "${i.base}"
  foreground: ink
  background: base
  primary: signal-text
  secondary: muted
  danger: "${l['alert-text']}"

typography:
  fonts:
    - family: ${val(d, 'font.family.display')[0]}
      source: file
      files:
        - path: assets/fonts/space-grotesk-500-latin.woff2
          weight: 500
    - family: ${val(d, 'font.family.body')[0]}
      source: file
      files:
        - path: assets/fonts/ibm-plex-sans-400-latin.woff2
          weight: 400
        - path: assets/fonts/ibm-plex-sans-600-latin.woff2
          weight: 600
    - family: ${val(d, 'font.family.mono')[0]}
      source: file
      files:
        - path: assets/fonts/ibm-plex-mono-400-latin.woff2
          weight: 400
  base:
    family: ${val(d, 'font.family.body')[0]}
    size: 11pt
    line-height: ${val(d, 'font.line-height.body')}
  headings:
    family: ${val(d, 'font.family.display')[0]}
    weight: ${val(d, 'font.weight.display')}
    color: ink
  monospace:
    family: ${val(d, 'font.family.mono')[0]}
    size: 0.9em
  link:
    color: signal-text
`;
  },
});

// ── the contrast gate ─────────────────────────────────────────────────────
const THRESHOLD = { text: 4.5, mark: 3.0 };

StyleDictionary.registerFormat({
  name: 'umbral/contrast',
  format: ({ dictionary: d }) => {
    const report = { $generated: HEADER('contrast.json'), thresholds: THRESHOLD, modes: {}, cvd: {}, summary: {} };
    let failures = 0;
    let checked = 0;
    for (const mode of MODES) {
      const s = semantic(d, mode);
      const pairs = [];
      for (const [name, hex] of Object.entries(s)) {
        const role = roleOf(d, mode, name);
        if (role === 'surface') continue;
        for (const bg of ['base', 'panel']) {
          const ratio = floorRatio(contrast(hex, s[bg]));
          const need = THRESHOLD[role] ?? null;
          const pass = need === null ? null : ratio >= need;
          if (pass === false) failures += 1;
          if (need !== null) checked += 1;
          pairs.push({
            token: name, on: bg, fg: hex, bg: s[bg], role, ratio, threshold: need, pass,
          });
        }
      }
      report.modes[mode] = pairs;

      // series separability, including under simulated dichromacy
      const series = seriesOrder(d, mode);
      const sep = [];
      for (let i = 0; i < series.length; i += 1) {
        for (let j = i + 1; j < series.length; j += 1) {
          const row = { a: series[i].name, b: series[j].name, normal: +oklabDistance(series[i].hex, series[j].hex).toFixed(3) };
          for (const k of CVD_KINDS) {
            row[k] = +oklabDistance(simulateCvd(series[i].hex, k), simulateCvd(series[j].hex, k)).toFixed(3);
          }
          row.worst = Math.min(row.normal, ...CVD_KINDS.map((k) => row[k]));
          sep.push(row);
        }
      }
      report.cvd[mode] = sep;
    }
    report.summary = {
      pairsChecked: checked,
      failures,
      exempt: d.allTokens.filter((t) => t.$extensions?.umbral?.contrastRole === 'furniture').length,
      worstSeriesSeparation: Math.min(...MODES.flatMap((m) => report.cvd[m].map((r) => r.worst))),
      note: 'furniture-role tokens are exempt by assertion — see audit/open-questions.md OQ-001',
    };
    return `${JSON.stringify(report, null, 2)}\n`;
  },
});

// ── run ───────────────────────────────────────────────────────────────────
const platformBase = { transformGroup: 'js', buildPath: `${OUT}/` };

const sd = new StyleDictionary({
  source: ['tokens/src/*.tokens.json'],
  preprocessors: ['umbral/expand-ramps'],
  platforms: {
    css: { ...platformBase, files: [{ destination: 'tokens.css', format: 'umbral/css' }] },
    scss: { ...platformBase, files: [{ destination: '_tokens.scss', format: 'umbral/scss' }] },
    json: { ...platformBase, files: [{ destination: 'tokens.json', format: 'umbral/json' }] },
    python: { ...platformBase, files: [{ destination: 'tokens.py', format: 'umbral/python' }] },
    r: { ...platformBase, files: [{ destination: 'tokens.R', format: 'umbral/r' }] },
    mpl: {
      ...platformBase,
      files: MODES.map((mode) => ({
        destination: `umbral-${mode}.mplstyle`, format: 'umbral/mplstyle', options: { mode },
      })),
    },
    plotly: {
      ...platformBase,
      files: MODES.map((mode) => ({
        destination: `plotly-umbral-${mode}.json`, format: 'umbral/plotly', options: { mode },
      })),
    },
    altair: { ...platformBase, files: [{ destination: 'altair-umbral.py', format: 'umbral/altair' }] },
    streamlit: { ...platformBase, files: [{ destination: 'streamlit-config.toml', format: 'umbral/streamlit' }] },
    framework: {
      ...platformBase,
      files: MODES.map((mode) => ({
        destination: `observable-framework-${mode}.css`, format: 'umbral/framework', options: { mode },
      })),
    },
    quarto: { ...platformBase, files: [{ destination: '_brand.yml', format: 'umbral/quarto-brand' }] },
    contrast: { ...platformBase, files: [{ destination: 'contrast.json', format: 'umbral/contrast' }] },
  },
});

await fs.mkdir(OUT, { recursive: true });
await sd.buildAllPlatforms();

// The gate itself: fail the build, not just the report.
const report = JSON.parse(await fs.readFile(path.join(OUT, 'contrast.json'), 'utf8'));
const failed = MODES.flatMap((m) => report.modes[m].filter((p) => p.pass === false));
console.log(`\ncontrast: ${report.summary.pairsChecked} pairs checked, `
  + `${report.summary.exempt} furniture tokens exempt, ${failed.length} failing`);
if (failed.length) {
  for (const f of failed) {
    console.error(`  FAIL  ${f.token} on ${f.on} (${f.role})  ${f.ratio}:1 < ${f.threshold}:1`);
  }
  process.exitCode = 1;
} else {
  console.log('contrast gate: PASS');
}
console.log(`worst series separation incl. CVD: ${report.summary.worstSeriesSeparation}`);
