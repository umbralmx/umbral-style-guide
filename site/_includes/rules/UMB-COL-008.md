<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-008 data-severity="error"}

**■ UMB-COL-008** · Color · error

### Un color categórico nuevo se deriva en OKLCH y se verifica contra dicromacia

Variar solo el tono no basta: para un dicrómata el tono colapsa a un solo eje. Medido, la mejor quinta serie posible variando solo tono queda en 0.042 de separación OKLab, por debajo del umbral de ~0.10 en el que dos marcas dejan de distinguirse.

| | |
|---|---|
| **Sí** | Variar tono y, si hace falta, luminosidad; verificar con audit/scripts/cvd.py. |
| **No** | Añadir una serie por parecido estético sin medir su separación. |

*Comprobación:* Automática — `verify-tokens`, comprobación `series-separation`.

*Origen:* OQ-009. Sustituye la regla de v1.0 «variando solo el tono» para el caso categórico.

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
