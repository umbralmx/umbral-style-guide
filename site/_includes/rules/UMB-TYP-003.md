<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-TYP-003 data-severity="error"}

**■ UMB-TYP-003** · Tipografía · error

### Se respetan los tamaños mínimos: 12px mono en web, 24px en slides, 11pt en documentos

Debajo de esos tamaños el texto deja de ser legible para una parte del público, y las cifras —que son el argumento— son lo primero que se pierde.

| | |
|---|---|
| **Sí** | Usar font.minimum de los tokens como piso. |
| **No** | Reducir la fuente para que quepa más. |

*Comprobación:* Automática — `umbral-lint`, comprobación `minimum-font-size`.

*Origen:* Brand book p.04; medido: 34 elementos a 11px mono en desaparecidosmx.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
