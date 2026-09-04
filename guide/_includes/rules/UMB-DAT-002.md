<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-DAT-002 data-severity="error"}

**■ UMB-DAT-002** · Datos y procedencia · error

### Los snapshots se etiquetan y la página dice cuál usó

El RNPDNO es un registro vivo y sus conteos cambian entre consultas. Sin la etiqueta del snapshot, dos gráficas correctas parecen contradecirse.

| | |
|---|---|
| **Sí** | Etiqueta el corte como rnpdno-2026-07 y declara esa etiqueta en la página, junto al enlace al CSV. La línea de fuente de la gráfica lleva la fecha de consulta.
 |
| **No** | No publiques una cifra de un registro vivo sin decir de qué corte salió. No escribas «Fuente: RNPDNO» sin fecha de consulta.
 |

*Comprobación:* Automática — `umbral-lint`, comprobación `snapshot-tag`.

*Origen:* desaparecidosmx ya lo hacía en la línea de fuente. En 2.0 la etiqueta se movió a la página, donde cabe junto al CSV y al SOURCE.md que la explican.

*Ver también:* UMB-CHT-003

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
