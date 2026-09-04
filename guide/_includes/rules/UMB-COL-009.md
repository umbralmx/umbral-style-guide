<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-009 data-severity="error"}

**■ UMB-COL-009** · Color · error

### Las dos rampas secuenciales no codifican dos variables en la misma figura

Las rampas ancladas en signal y en model quedan a 0.014 de separación OKLab bajo tritanopía. Para ese lector, dos mapas codificados con ellas son el mismo mapa.

| | |
|---|---|
| **Sí** | Usa una rampa secuencial por figura. Si necesitas dos, varía también el rango de luminosidad. |
| **No** | No pongas un coroplético en rampa signal junto a otro en rampa model. |

*Comprobación:* En revisión.

*Origen:* Decisión OQ-005.

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
