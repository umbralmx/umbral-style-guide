<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-010 data-severity="error"}

**■ UMB-COL-010** · Color · error

### Dato faltante, dato suprimido y cero se distinguen visualmente entre sí

«No hay registro», «se suprimió por debajo del umbral de reporte» y «ocurrieron cero casos» son tres hechos distintos. Representarlos igual afirma algo falso.

| | |
|---|---|
| **Sí** | Usa missing como relleno plano, la trama de 45° para suprimido, y el extremo de la rampa para cero. |
| **No** | No pintes el faltante como el valor más bajo de la escala. |

*Comprobación:* En revisión.

*Origen:* KICKOFF §3.3 pide un relleno de faltante y una trama de suprimido; v1.0 no definía ninguno.

*Ver también:* UMB-NUM-006

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
