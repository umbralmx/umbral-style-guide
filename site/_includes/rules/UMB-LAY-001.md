<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-001 data-severity="error"}

**■ UMB-LAY-001** · Layout · error

### El radio de borde nunca pasa de 2px

La marca es plana y recta. El radio grande —y sobre todo el botón tipo píldora— lee como producto de consumo, no como instrumento.

| | |
|---|---|
| **Sí** | var(--u-radius); como mucho var(--u-radius-max). |
| **No** | border-radius: 8px, 999px, o cualquier píldora. |

*Comprobación:* Automática — `umbral-lint`, comprobación `radius-max`.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
