<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-DAT-002" data-severity="error">

**■ UMB-DAT-002** · Datos y procedencia · error

### Los snapshots se etiquetan y la gráfica dice cuál usó

El RNPDNO es un registro vivo: los conteos cambian entre consultas. Sin la etiqueta del snapshot, dos gráficas correctas parecen contradecirse.

| | |
|---|---|
| **Sí** | rnpdno-2026-07, y esa etiqueta en la línea de fuente. |
| **No** | «Fuente: RNPDNO» sin fecha de consulta. |

*Comprobación:* Automática — `umbral-lint`, comprobación `snapshot-tag`.

*Origen:* desaparecidosmx ya lo hace: «consultado 2026-07-09 · rnpdno-2026-07».

*Ver también:* UMB-CHT-003

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
