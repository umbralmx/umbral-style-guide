<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-LAY-009 data-severity="warning"}

**▲ UMB-LAY-009** · Layout · advertencia

### La retícula de puntos solo ocupa el margen exterior de la hoja

La retícula de puntos marca el papel milimétrico del instrumento. Debajo del texto reduce el contraste efectivo y contradice UMB-LAY-005, que prohíbe la decoración. En el margen no toca ningún texto y no cambia ningún contraste medido.

| | |
|---|---|
| **Sí** | Dibuja la retícula en var(--u-baseline) detrás de la página y tápala con var(--u-base) bajo el contenido. |
| **No** | No pongas la retícula debajo de texto, de una tabla ni de una gráfica. |

*Comprobación:* En revisión.

*Origen:* umbral.org.mx, agosto de 2026: la retícula vive fuera de .sheet y desaparece en móvil.

*Ver también:* UMB-LAY-005 · UMB-COL-005

<small>Desde v1.2. Regla normativa: `rules/rules.yaml`.</small>

:::
