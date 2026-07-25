<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-CHT-005" data-severity="error">

**■ UMB-CHT-005** · Gráficas · error

### Las series se etiquetan directamente al final de la línea; no hay caja de leyenda

La leyenda obliga a ir y venir entre el dato y su nombre. La etiqueta directa también es la razón por la que los colores de serie cuentan como texto pequeño y deben cumplir 4.5:1, no 3:1.

| | |
|---|---|
| **Sí** | Plot.text en el último dato de cada serie. |
| **No** | Una caja de leyenda al costado. |

*Comprobación:* Automática — `umbral-lint`, comprobación `no-legend-box`.

*Ver también:* UMB-COL-005 · UMB-A11Y-005

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
