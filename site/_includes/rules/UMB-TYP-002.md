<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-TYP-002 data-severity="error"}

**■ UMB-TYP-002** · Tipografía · error

### Solo se usan Space Grotesk, IBM Plex Sans e IBM Plex Mono

La tipografía es la mitad de la identidad. Un framework que sustituye la familia por defecto deshace el sistema sin que nadie lo note.

| | |
|---|---|
| **Sí** | Declara las tres familias y auto-hospédalas. |
| **No** | No uses Inter, Roboto, Arial, Helvetica ni la Source Sans por defecto de Streamlit. |

*Comprobación:* Automática — `umbral-lint`, comprobación `banned-font-family`.

*Origen:* Brand book p.04 «NUNCA»; medido: Source Sans renderizando en pautamx por font = "sans serif".

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
