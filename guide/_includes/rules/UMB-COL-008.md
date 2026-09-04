<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-008 data-severity="error"}

**■ UMB-COL-008** · Color · error

### Un color categórico nuevo se deriva en OKLCH y se verifica contra dicromacia

Variar solo el tono no basta. Para un dicrómata el tono colapsa a un solo eje. La mejor quinta serie posible variando solo tono queda en 0.042 de separación OKLab. Dos marcas dejan de distinguirse por debajo de 0.10.

| | |
|---|---|
| **Sí** | Varía el tono y, si hace falta, la luminosidad. Verifica con audit/scripts/cvd.py. |
| **No** | No añadas una serie por parecido estético sin medir su separación. |

*Comprobación:* Automática — `verify-tokens`, comprobación `series-separation`.

*Origen:* OQ-009. Sustituye la regla de v1.0 «variando solo el tono» para el caso categórico.

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
