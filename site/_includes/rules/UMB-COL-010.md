<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-010 data-severity="error"}

**■ UMB-COL-010** · Color · error

### Dato faltante, dato suprimido y cero se distinguen visualmente entre sí

En datos de desaparición y de delito la diferencia entre «no hay registro», «se suprimió por debajo del umbral de reporte» y «ocurrieron cero casos» es sustantiva. Representarlas igual es afirmar algo falso.

| | |
|---|---|
| **Sí** | missing como relleno plano; suppressed con la trama de 45°; cero en el extremo de la rampa. |
| **No** | Pintar el faltante como el valor más bajo de la escala. |

*Comprobación:* En revisión.

*Origen:* KICKOFF §3.3 pide un relleno de faltante y una trama de suprimido; v1.0 no definía ninguno.

*Ver también:* UMB-NUM-006

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
