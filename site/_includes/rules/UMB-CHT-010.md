<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-CHT-010 data-severity="error"}

**■ UMB-CHT-010** · Gráficas · error

### No se usan pastel, 3D ni doble eje

El pastel codifica en ángulo, que se compara mal; el 3D distorsiona el área; el doble eje permite fabricar cualquier correlación aparente eligiendo las escalas.

| | |
|---|---|
| **Sí** | Barras para composición, líneas para tiempo, dos paneles para dos unidades. |
| **No** | Pastel, dona, barras 3D, dos ejes y verticales con escalas distintas. |

*Comprobación:* Automática — `umbral-lint`, comprobación `banned-chart-type`.

*Origen:* Brand book p.08 «Nunca: pastel · 3D · doble eje · eje-y truncado sin nota».

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
