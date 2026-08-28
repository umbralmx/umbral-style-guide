<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-001 data-severity="error"}

**■ UMB-LAY-001** · Layout · error

### El radio de borde nunca pasa de 2px

La marca es plana y recta. Un radio grande, y sobre todo un botón tipo píldora, se lee como producto de consumo y no como instrumento.

| | |
|---|---|
| **Sí** | Usa var(--u-radius). Como mucho, usa var(--u-radius-max). |
| **No** | No uses border-radius de 8px, de 999px ni ninguna píldora. |

*Comprobación:* Automática — `umbral-lint`, comprobación `radius-max`.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
