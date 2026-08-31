---
title: "Tipografía"
lang: es
---

# 03 · Tipografía

Tres familias. Cada caso tiene una sola familia correcta.

| Familia | Úsala para |
|---|---|
| **Space Grotesk** | Wordmark, titulares, títulos de gráfica, una cifra heroica suelta |
| **IBM Plex Sans** | Texto de lectura, interfaz, etiquetas |
| **IBM Plex Mono** | Ejes, líneas de fuente, código, y toda cifra que se alinee o se compare |

{{< include _includes/rules/UMB-TYP-002.md >}}

## El peso 500

Usa Space Grotesk 500 en display, siempre. El 600 existe solo para etiquetas pequeñas. El 700 no
existe en el sistema.

Un titular no necesita subir de peso si la cifra que lo acompaña es correcta. El 700 cambia el
registro de la voz entera.

{{< include _includes/rules/UMB-TYP-001.md >}}

{{< include _includes/rules/UMB-TYP-006.md >}}

## La escala

{{< include _includes/type-scale.md >}}

{{< include _includes/rules/UMB-TYP-003.md >}}

## Cifras: mono o display

La pregunta no es el tamaño. La pregunta es si la cifra se compara.

| Situación | Familia | Por qué |
|---|---|---|
| Fila de KPIs, columna de tabla, eje | **Plex Mono** | Los numerales tabulares alinean los dígitos. Comparar es el punto. |
| Una cifra suelta dentro de un titular | **Space Grotesk 500** | Se lee como lenguaje, no como dato a cotejar. |
| Texto corrido | Plex Sans | |

{{< include _includes/rules/UMB-TYP-004.md >}}

::: {.u-note}
**v1.0** · Decía a la vez «Space Grotesk para cifras grandes» e «IBM Plex Mono para todas las cifras
tabulares». Un KPI es las dos cosas. Los dos tableros lo resolvieron distinto: `pautamx` en mono y
`desaparecidosmx` en Plex Sans, que no era ninguna de las dos. El criterio de alineación resuelve el
caso.
:::

## Etiquetas de estructura

Una etiqueta de sección nombra la estructura de la página. No es un titular.

{{< include _includes/rules/UMB-LAY-006.md >}}

Ver [04 · Layout](04-layout.md) para cómo se construye la sección que la etiqueta encabeza.

## Auto-hospedaje

{{< include _includes/rules/UMB-TYP-005.md >}}

Entregar la IP de cada lector a un tercero es difícil de justificar publicando sobre
desapariciones.

Las tres familias son OFL. Se sirven desde `assets/fonts/`, subconjuntadas a `latin` y `latin-ext`.
`latin-ext` es la que trae los diacríticos del español. El archivo de licencia va al lado.

```html
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/tokens.css">
```

::: {.u-note}
<!-- umbral-lint: ignore[font-hosting] — se cita el CDN precisamente para prohibirlo -->
**cuidado** · No copies un `@import` de `fonts.googleapis.com` de ningún documento antiguo. El
documento de ingeniería de v1.0 pedía auto-hospedar en prosa y entregaba el enlace al CDN en el
bloque de código de la misma sección. El sitio principal copió el bloque de código y ahí sigue.
:::
