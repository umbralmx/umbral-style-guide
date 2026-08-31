<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-003 data-severity="warning"}

**▲ UMB-LAY-003** · Layout · advertencia

### La medida del texto no pasa de 65 caracteres

Pasados los 65 caracteres, el ojo pierde el renglón al volver a la izquierda.

| | |
|---|---|
| **Sí** | Pon max-width: var(--u-measure) en la columna de texto. |
| **No** | No dejes párrafos a todo el ancho de la ventana. |

*Comprobación:* Automática — `umbral-lint`, comprobación `measure-max`.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
