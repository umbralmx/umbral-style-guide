<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-002 data-severity="error"}

**■ UMB-LAY-002** · Layout · error

### No hay sombras; las reglas de 1px hacen el trabajo estructural

La profundidad falsa compite con el dato. Una regla de 1px separa igual y no añade ruido.

| | |
|---|---|
| **Sí** | Usa una regla sólida de 1px en var(--u-border). |
| **No** | No uses box-shadow con desenfoque ni con desplazamiento. No eleves tarjetas. |

**Excepciones**

- Un box-shadow con `inset` que dibuja una regla, por ejemplo `inset 4px 0 0 var(--u-signal)`, no es una sombra. cabildo-libre lo usa así.

*Comprobación:* Automática — `umbral-lint`, comprobación `no-drop-shadow`.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
