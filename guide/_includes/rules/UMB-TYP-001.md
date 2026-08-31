<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-TYP-001 data-severity="error"}

**■ UMB-TYP-001** · Tipografía · error

### El display es Space Grotesk 500; nunca 700

El peso medio es lo que distingue a la marca de un titular genérico. El 700 sube el volumen de la voz sin añadir información.

| | |
|---|---|
| **Sí** | Usa font-weight 500 en titulares. Usa 600 solo en etiquetas pequeñas. |
| **No** | No uses font-weight 700, 800, 900 ni `bold` en un selector de display. |

*Comprobación:* Automática — `umbral-lint`, comprobación `display-weight`.

*Origen:* Brand book p.04 «LA FIRMA».

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
