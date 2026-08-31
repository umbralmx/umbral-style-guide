<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-008 data-severity="warning"}

**▲ UMB-LAY-008** · Layout · advertencia

### Los controles secundarios son mono con borde de 1px y pasan a signal al enfocarse

Un control con borde de 1px y sin relleno se lee como control sin competir con el dato. Reservar signal para el estado activo mantiene libre el único punto de atención de la vista, que UMB-COL-004 asigna a la capa de datos.

| | |
|---|---|
| **Sí** | Dibuja el control con 1px en var(--u-baseline) y pasa el borde y el texto a signal en hover y en focus-visible. |
| **No** | No rellenes un control secundario con un color sólido. No lo dejes en signal en reposo. |

*Comprobación:* En revisión.

*Origen:* umbral.org.mx, agosto de 2026: los enlaces «Dashboard» y «Código» son botones de 1px.

*Ver también:* UMB-COL-004 · UMB-LAY-001 · UMB-A11Y-006

<small>Desde v1.2. Regla normativa: `rules/rules.yaml`.</small>

:::
