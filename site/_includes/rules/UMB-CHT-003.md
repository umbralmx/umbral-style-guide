<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-CHT-003 data-severity="error"}

**■ UMB-CHT-003** · Gráficas · error

### Toda gráfica lleva su línea de fuente con licencia, sobre una regla de 1px

Nombrar la fuente y su licencia es la mitad de la credibilidad del laboratorio, y es lo que permite que alguien más rehaga el cálculo.

| | |
|---|---|
| **Sí** | «Fuente: RNPDNO (CNB/SEGOB) · consultado 2026-07-09 · rnpdno-2026-07 · umbral.mx · datos CC BY 4.0». |
| **No** | Publicar una gráfica sin fuente, o con la fuente solo en el texto que la rodea. |

*Comprobación:* Automática — `umbral-lint`, comprobación `chart-source-present`.

*Origen:* desaparecidosmx es el mejor ejemplo del portafolio: incluye la etiqueta del snapshot.

*Ver también:* UMB-DAT-002

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
