<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-CHT-003 data-severity="error"}

**■ UMB-CHT-003** · Gráficas · error

### Toda gráfica lleva su línea de fuente sobre una regla de 1px, con el sitio a la derecha

La gráfica circula sin su página. La línea de fuente es lo único que viaja con ella. Dice de dónde salió el dato y cuándo se consultó, que es lo que permite rehacer el cálculo. El sitio va a la derecha para que la atribución se lea de un vistazo.

| | |
|---|---|
| **Sí** | A la izquierda, «Fuente: Elaboración propia con datos del RNPDNO (CNB/SEGOB). Consulta realizada el 2026-07-20.» A la derecha, «umbral.org.mx».
 |
| **No** | No publiques una gráfica sin fuente. No dejes la fuente solo en el texto que la rodea. No metas la licencia ni la etiqueta del corte en esta línea: van en la página.
 |

*Comprobación:* Automática — `umbral-lint`, comprobación `chart-source-present`.

*Origen:* En 2.0 la línea se simplificó. La licencia y la etiqueta del corte se movieron a la página, porque una línea de cinco campos no se lee en una tarjeta social ni en una diapositiva. Lo que viaja con la gráfica es el origen, la fecha de consulta y el sitio.

*Ver también:* UMB-DAT-002 · UMB-DAT-004

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
