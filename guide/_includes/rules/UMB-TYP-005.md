<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-TYP-005 data-severity="error"}

**■ UMB-TYP-005** · Tipografía · error

### Las tres fuentes se auto-hospedan, subconjuntadas a latin y latin-ext

Un producto de interés público tiene que funcionar sin conexión y dentro de redes de gobierno. Un CDN externo además entrega la IP de cada lector a un tercero.

| | |
|---|---|
| **Sí** | Sirve los .woff2 desde assets/fonts/ con su licencia OFL al lado. |
| **No** | No enlaces fonts.googleapis.com. No uses un @import a un CDN. |

*Comprobación:* Automática — `umbral-lint`, comprobación `font-hosting`.

*Origen:* umbral-engineering.md §1 lo pide en prosa. En el bloque de código de la misma sección entrega un <link> a Google Fonts. umbralmx.github.io usa el CDN.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
