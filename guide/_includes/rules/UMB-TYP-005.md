<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-TYP-005" data-severity="error">

**■ UMB-TYP-005** · Tipografía · error

### Las tres fuentes se auto-hospedan, subconjuntadas a latin y latin-ext

Un producto de datos de interés público tiene que funcionar sin conexión y dentro de redes de gobierno. Depender de un CDN externo también filtra la IP de cada lector a un tercero.

| | |
|---|---|
| **Sí** | Servir los .woff2 desde assets/fonts/ con su licencia OFL. |
| **No** | fonts.googleapis.com, ni un @import a un CDN. |

*Comprobación:* Automática — `umbral-lint`, comprobación `font-hosting`.

*Origen:* umbral-engineering.md §1 lo pide en prosa y entrega un <link> a Google Fonts en el bloque de código de la misma sección; umbralmx.github.io usa el CDN.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
