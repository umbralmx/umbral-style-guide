<!-- references/color.md — GENERATED from the normative layer of
     umbralmx/umbral-style-guide v1.1.0. Do not edit; regenerate. -->

# Color

Read `assets/tokens.json` for machine-readable values. Never retype a hex.

| Token | laboratorio (light) | instrumento (dark) | Contrast role |
|---|---|---|---|
| `base` | `#f2f3f1` | `#101418` | surface |
| `panel` | `#fafaf8` | `#171c22` | surface |
| `ink` | `#16191c` | `#edf1f4` | text |
| `muted` | `#565d57` | `#8b95a0` | text |
| `caption` | `#6c706d` | `#7a848f` | text |
| `border` | `#dde0dc` | `#2a3138` | furniture |
| `gridline` | `#e6e8e4` | `#232a31` | furniture |
| `baseline` | `#c4c9c4` | `#3a434c` | furniture |
| `signal` | `#128273` | `#5fd4c4` | mark |
| `signal-text` | `#227c6f` | `#5fd4c4` | text |
| `model` | `#5a63d8` | `#8b93f8` | mark |
| `model-text` | `#5962d7` | `#8b93f8` | text |
| `alert` | `#c8503f` | `#e26a5a` | mark |
| `alert-text` | `#be4737` | `#e26a5a` | text |
| `series-4` | `#902a00` | `#ffce2c` | mark |
| `series-5` | `#6331a0` | `#b454b3` | mark |
| `missing` | `#e3e5e1` | `#1d242b` | furniture |

## Roles decide the threshold

| Role | Threshold | Meaning |
|---|---|---|
| `text` | 4.5:1 | anything read |
| `mark` | 3:1 | data marks — series, bars, points |
| `furniture` | exempt | gridlines, borders, baselines. Deliberately low-contrast; do not "fix" |
| `surface` | — | backgrounds; measured against |

Verified in CI: 44 pairs, 0 failing,
8 furniture tokens exempt by explicit declaration.

## The text variants

`signal` clears 3:1 as a mark but not 4.5:1 as text. Because the brand mandates **direct series
labels instead of legend boxes**, series colours end up as small text — so:

- use `signal` / `model` / `alert` for the mark;
- use `signal-text` / `model-text` / `alert-text` for any text, link, or direct series label.

## Series order

`#128273` · `#5a63d8` · `#565d57` · `#c8503f` · `#902a00` · `#6331a0` (laboratorio)

Semantic order: signal, model, muted, alert, series-4, series-5. Maximum 5 in one chart.

The third series is **`muted`**, not `caption`. v1.0's matplotlib and Observable Plot themes used
`caption`, which sits below the 3:1 a data mark needs.

## Colour-vision deficiency

- **laboratorio**: worst-separated pair is `signal`/`model` at 0.014 (OKLab, worst case across normal vision and simulated dichromacy)
- **instrumento**: worst-separated pair is `signal`/`model` at 0.076 (OKLab, worst case across normal vision and simulated dichromacy)

Below ~0.10 two marks are not reliably separable. The mitigation is not cosmetic — it is the
mandatory direct label (UMB-CHT-005) and the ban on colour-only encoding (UMB-A11Y-005).

## Ramps

| Ramp | Steps | Use |
|---|---|---|
| sequential `signal` | 7 | intensity of one variable; the default choropleth |
| sequential `model` | 7 | a second variable — **never in the same figure** as the above |
| diverging | 9 | change, surplus/deficit, above/below expectation |

Plus `missing` for absent data and a 45° hatch for suppressed values. Missing, suppressed and zero
must look different from one another.

## Rules

- **UMB-COL-001** (**must**) — Pure white and pure black are never used
  - do: var(--u-base) y var(--u-ink).
  - don't: #fff, #ffffff, #000, white, black.
- **UMB-COL-002** (**must**) — No colour is hand-typed; every value comes from the tokens
  - do: var(--u-signal), tokens['signal'], umbral_laboratorio$signal.
  - don't: #128273 escrito directamente en una hoja de estilo, un notebook o una gráfica.
- **UMB-COL-003** (**must**) — No gradients
  - do: Rellenos sólidos; una rampa secuencial si hay que codificar intensidad.
  - don't: linear-gradient decorativo, fondos con degradado, barras degradadas.
- **UMB-COL-004** (**must**) — signal is used on exactly one element of the data layer per view
  - do: Una serie, una cifra o un elemento de UI en signal.
  - don't: Signal en el logo, el botón y la serie principal a la vez.
- **UMB-COL-005** (**must**) — All text clears 4.5:1 against both base and panel
  - do: Usar ink, muted, caption y las variantes *-text, que la compuerta ya verifica.
  - don't: Usar signal, model o alert como color de texto pequeño en modo laboratorio.
- **UMB-COL-006** (**must**) — Every data mark clears 3:1; chart furniture is exempt and says so
  - do: Declarar contrastRole en cada token: text, mark, furniture o surface.
  - don't: Exigir 3:1 a una retícula, ni eximir a una serie de datos.
- **UMB-COL-007** (**must**) — The two modes are never mixed inside one panel
  - do: data-mode="instrumento" sobre un contenedor completo.
  - don't: Un panel claro con una tarjeta oscura dentro, o al revés.
- **UMB-COL-008** (**must**) — A new categorical colour is derived in OKLCH and verified against dichromacy
  - do: Variar tono y, si hace falta, luminosidad; verificar con audit/scripts/cvd.py.
  - don't: Añadir una serie por parecido estético sin medir su separación.
- **UMB-COL-009** (**must**) — The two sequential ramps never encode two variables in one figure
  - do: Una rampa secuencial por figura; si hacen falta dos, variar también el rango de luminosidad.
  - don't: Un coroplético en rampa signal junto a otro en rampa model.
- **UMB-COL-010** (**must**) — Missing, suppressed and zero are visually distinct from one another
  - do: missing como relleno plano; suppressed con la trama de 45°; cero en el extremo de la rampa.
  - don't: Pintar el faltante como el valor más bajo de la escala.
