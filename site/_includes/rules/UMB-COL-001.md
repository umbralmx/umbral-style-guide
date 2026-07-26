<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-001 data-severity="error"}

**■ UMB-COL-001** · Color · error

### No se usa blanco ni negro puros

El blanco y el negro puros producen un contraste duro que cansa la lectura larga y delatan que el color no vino de los tokens. base e ink existen precisamente para eso.

| | |
|---|---|
| **Sí** | var(--u-base) y var(--u-ink). |
| **No** | #fff, #ffffff, #000, white, black. |

*Comprobación:* Automática — `umbral-lint`, comprobación `pure-black-white`.

*Origen:* Brand book p.03; medido en desaparecidosmx (6 elementos en #FFFFFF).

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
