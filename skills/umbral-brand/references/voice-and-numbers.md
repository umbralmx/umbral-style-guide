<!-- references/voice-and-numbers.md — GENERATED from the normative layer of
     umbralmx/umbral-style-guide v1.1.0. Do not edit; regenerate. -->

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
| Thousands / decimals | `351,057` · `3.7` — Mexico uses the anglophone convention, unlike Spain |
| Axis abbreviation | `12k` · `3.7M`; write figures in full in prose |
| Percent | `9.2%`, tight. Distinguish **per cent** from **percentage points** |
| Precision | 2–3 significant figures unless the data supports more |
| Money | Always name the currency: `107.6 M MXN`. In long series use real pesos with a stated base year |
| Dates | ISO in data and axes (`2026-07`); prose in text (`julio de 2026`). Never `07/06/2026` |
| Ranges | `2010–2026` with an en dash |
| Censored values | `≥ 107.6 M` — a lower bound is not an estimate |

**Zero, null and suppressed are three different things** and must be written differently:
`0` · `sin dato` · `suprimido (< umbral)`. Filling a null with zero is a silent imputation, and
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

- **UMB-VOZ-001** (**must**) — Spanish first; English is added where the audience earns it
  - do: guide/ en español; inglés en código, commits y la capa meta.
  - don't: Traducir del inglés al español como paso final.
- **UMB-VOZ-002** (**must**) — No hype words, exclamation marks, emoji or rhetorical-question headlines
  - do: «Los registros crecen 9% anual desde 2015».
  - don't: «¿Sabías que los registros se DISPARARON? 🚨»
- **UMB-VOZ-003** (should) — An adjective never replaces a number
  - do: Cuantificar.
  - don't: «dramático», «masivo», «considerable» sin la cifra al lado.
- **UMB-VOZ-004** (**must**) — Placeholder content is never published
  - do: Publicar la sección cuando su texto exista.
  - don't: Lorem ipsum, «foto», «TODO», o una biografía sin escribir.
- **UMB-NUM-001** (**must**) — es-MX and en both use comma for thousands and point for decimals
  - do: 351,057 · 3.7 · 12.5%
  - don't: 351.057 · 3,7
- **UMB-NUM-002** (should) — Large figures are abbreviated on axes and written in full in prose
  - do: Eje: 12k, 3.7M. Texto: 351,057 registros.
  - don't: «351.1k registros» en una oración.
- **UMB-NUM-003** (should) — Dates are ISO in data and prose-formatted in text
  - do: Datos y etiquetas: 2026-07. Texto: julio de 2026.
  - don't: 07/06/2026, que significa cosas distintas en México y en Estados Unidos.
- **UMB-NUM-004** (may) — The percent sign is set tight against the figure
  - do: 9.2% — sin espacio entre la cifra y el símbolo.
  - don't: 9.2 % con espacio.
- **UMB-NUM-005** (**must**) — Stated precision never exceeds the precision of the data
  - do: Redondear a la precisión que el método sostiene y decir cuál es.
  - don't: Arrastrar todos los decimales que devuelve el cálculo.
- **UMB-NUM-006** (**must**) — Zero, null and suppressed are written differently and mean differently
  - do: 0 · «sin dato» · «suprimido (< umbral de reporte)».
  - don't: Rellenar los huecos con 0 al construir la serie.
- **UMB-MET-001** (**must**) — Causal verbs are used only with a named identification strategy
  - do: «asociado con» / «correlaciona» para lo descriptivo; «efecto» / «reduce» solo con RCT, dif-en-dif, RD o VI declarada.
  - don't: «X redujo Y» a partir de una serie de tiempo descriptiva.
- **UMB-MET-002** (**must**) — The headline is defensible from the data the chart shows
  - do: Que el lector pueda comprobar el título mirando la figura.
  - don't: Un titular sobre causas encima de una gráfica descriptiva.
- **UMB-MET-003** (**must**) — Raw counts are never compared across differently sized populations
  - do: Tasa por 100 mil con denominador declarado, o comparar dentro de la misma unidad en el tiempo.
  - don't: Un ranking de entidades por conteo absoluto.
- **UMB-MET-004** (**must**) — Sensitive topics are handled with dignity: people are counted, never made spectacle
  - do: Agregados, lenguaje sobrio, terminología del glosario.
  - don't: Mapas a nivel de individuo, fotografías, o adjetivos que dramatizan el conteo.
- **UMB-MET-005** (**must**) — Sensitive terminology follows the glossary, which is binding
  - do: Consultar guide/15-terminologia.md y usar la forma preferida.
  - don't: Elegir el término por brevedad o por costumbre.
