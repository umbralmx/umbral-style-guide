<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-CHT-002" data-severity="error">

**■ UMB-CHT-002** · Gráficas · error

### Toda gráfica lleva subtítulo con geografía, periodo y unidad

Sin unidad y sin periodo la cifra no significa nada, y la gráfica circula sin su contexto en cuanto alguien la captura de pantalla.

| | |
|---|---|
| **Sí** | «México · registros por mes de la fecha de hechos · el registro se actualiza retroactivamente». |
| **No** | Dejar la unidad implícita en el eje. |

*Comprobación:* Automática — `umbral-lint`, comprobación `chart-subtitle-present`.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
