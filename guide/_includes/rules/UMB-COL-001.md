<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-001 data-severity="error"}

**■ UMB-COL-001** · Color · error

### No se usa blanco ni negro puros

El blanco y el negro puros dan un contraste duro que cansa en lecturas largas. Su presencia indica además que el color no vino de los tokens.

| | |
|---|---|
| **Sí** | Usa var(--u-base) y var(--u-ink). |
| **No** | No escribas #fff, #ffffff, #000, white ni black. |

*Comprobación:* Automática — `umbral-lint`, comprobación `pure-black-white`.

*Origen:* Brand book p.03; medido en desaparecidosmx (6 elementos en #FFFFFF).

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
