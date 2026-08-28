<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-007 data-severity="warning"}

**▲ UMB-LAY-007** · Layout · advertencia

### Una lista de elementos se separa con reglas de 1px, no con tarjetas

Una fila separada por una regla de 1px pesa lo mismo que las demás. Una tarjeta con borde y relleno propios sugiere una jerarquía que la lista no tiene. La regla llega hasta el borde del contenedor, así que el ojo lee una sola columna.

| | |
|---|---|
| **Sí** | Usa border-top de 1px en var(--u-border) sobre cada fila a partir de la segunda. |
| **No** | No envuelvas cada elemento en su propio recuadro, fondo o relleno. |

*Comprobación:* En revisión.

*Origen:* umbral.org.mx, agosto de 2026: la lista de proyectos son filas con regla superior.

*Ver también:* UMB-LAY-002 · UMB-LAY-006

<small>Desde v1.2. Regla normativa: `rules/rules.yaml`.</small>

:::
