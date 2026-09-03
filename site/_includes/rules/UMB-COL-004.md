<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-004 data-severity="error"}

**■ UMB-COL-004** · Color · error

### El color signal se usa en un solo elemento de la capa de datos por vista

La jerarquía visual depende de que haya un único punto de atención. Si todo resalta, nada resalta. La regla se limita a la capa de datos porque un framework suele pintar todo su cromo con un mismo acento. Streamlit lo hace con primaryColor. Framework lo hace con --theme-foreground-focus. La diferencia es que en Framework el acento sí se puede acotar, así que ahí la regla alcanza también a los enlaces y a los controles.

| | |
|---|---|
| **Sí** | Pon en signal una serie, una cifra o un elemento de interfaz. |
| **No** | No pongas signal en el logo, el botón y la serie principal a la vez. |

*Comprobación:* En revisión.

*Origen:* Brand book p.03; medido: 17 elementos en desaparecidosmx, 10 en pautamx, 4 en cabildo-libre.

*Ver también:* UMB-COL-011

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
