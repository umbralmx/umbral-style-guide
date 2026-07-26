<!-- references/charts.md — GENERATED from the normative layer of
     umbralmx/umbral-style-guide v1.1.0. Do not edit; regenerate. -->

# Charts

**Read this before writing any chart code.**

## The frame every chart carries

```
Title that states the finding, as a sentence      Space Grotesk 500, 22px, left-aligned
Geography · period · unit                         Plex Sans, muted
[ plot area ]                                     horizontal gridlines only,
                                                  darker baseline, no border, no fill
──────────────────────────────────────            1px rule
Fuente: … · umbral.mx · datos CC BY 4.0           Plex Mono 12px, caption
```

Plus, always:

- `aria-label` carrying the same claim as the title — not "line chart";
- an adjacent data table or `<details>`;
- a downloadable CSV.

## Source line format

```
Fuente: ORIGEN (INSTITUCIÓN) · consultado AAAA-MM-DD · SNAPSHOT-TAG · umbral.mx · datos CC BY 4.0
```

The snapshot tag matters for live registers: the RNPDNO's counts for past months change between
queries, so two correct charts made weeks apart appear to contradict each other without it.

## Uncertainty

- Band at **0.15** opacity of the series colour, no border.
- Dashed stroke (`7 5`) past the last observed datum.
- Dashed vertical rule labelled `hoy`.
- The subtitle must say **what the band is**: `IC 95%`, `intervalo de predicción 80%`, or the
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

## Rules

- **UMB-CHT-001** (**must**) — The chart title states the finding as a full sentence
  - do: «El gasto observable acumula ≥ 107.6 M MXN».
  - don't: «Gasto por mes».
- **UMB-CHT-002** (**must**) — Every chart carries a subtitle with geography, period and unit
  - do: «México · registros por mes de la fecha de hechos · el registro se actualiza retroactivamente».
  - don't: Dejar la unidad implícita en el eje.
- **UMB-CHT-003** (**must**) — Every chart carries its source line with licence, above a 1px rule
  - do: «Fuente: RNPDNO (CNB/SEGOB) · consultado 2026-07-09 · rnpdno-2026-07 · umbral.mx · datos CC BY 4.0».
  - don't: Publicar una gráfica sin fuente, o con la fuente solo en el texto que la rodea.
- **UMB-CHT-004** (**must**) — Horizontal gridlines only, with a darker baseline
  - do: y.grid = true, x.grid = false, base en --u-baseline.
  - don't: Retícula en ambos ejes, o marco alrededor de la gráfica.
- **UMB-CHT-005** (**must**) — Series are labelled directly at line ends; no legend box
  - do: Plot.text en el último dato de cada serie.
  - don't: Una caja de leyenda al costado.
- **UMB-CHT-006** (should) — A chart carries at most 5 series
  - do: Una serie en signal, el resto en model/muted; el resto agrupado en «otros».
  - don't: Ocho líneas y una leyenda para desenredarlas.
- **UMB-CHT-007** (should) — Axis ticks are mono, abbreviated, with comma thousands separators
  - do: 12k, 3.7M, 351,057.
  - don't: 12000, 3700000, o cifras en la tipografía de cuerpo.
- **UMB-CHT-008** (**must**) — The y-axis starts at zero for bars
  - do: Barras desde 0, siempre.
  - don't: Empezar el eje en el mínimo observado para «que se note la diferencia».
- **UMB-CHT-009** (**must**) — Any axis truncation is annotated on the chart itself
  - do: Marcar el corte y decirlo junto al eje.
  - don't: Truncar en silencio.
- **UMB-CHT-010** (**must**) — No pie charts, 3D or dual axes
  - do: Barras para composición, líneas para tiempo, dos paneles para dos unidades.
  - don't: Pastel, dona, barras 3D, dos ejes y verticales con escalas distintas.
- **UMB-CHT-011** (**must**) — Every projection or estimate shows its uncertainty
  - do: Banda al 15% de opacidad del color de la serie; trazo punteado más allá del presente; regla vertical punteada etiquetada «hoy».
  - don't: Una línea sólida que cruza hacia el futuro sin distinguirse del dato observado.
- **UMB-CHT-012** (**must**) — Every rate states its denominator and n
  - do: «tasa por 100 mil habitantes · denominador CONAPO 2026 · n = 1,204».
  - don't: Publicar la tasa sola.
