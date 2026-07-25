---
title: "Color y modos"
lang: es
---

# 02 · Color y modos

Los dos modos comparten tipografía, layout, logo y semántica. **Solo cambian los tokens de color.**

| | Cuándo |
|---|---|
| **modo laboratorio** (claro) — por defecto | Sitio, informes, decks, documentos, prensa |
| **modo instrumento** (oscuro) | Tableros en vivo, tarjetas sociales, pantallas de monitoreo, divisores de sección y diapositivas de cifra grande |

Se cambia con `data-mode="instrumento"` o la clase `.u-dark` sobre un contenedor completo.

{{< include _includes/rules/UMB-COL-007.md >}}

## Los tokens

{{< include _includes/token-table.md >}}

Cada token declara un **rol de contraste**, y ese rol es lo que la compuerta de CI comprueba:

| Rol | Umbral | Qué es |
|---|---|---|
| `texto` | 4.5:1 | Cualquier cosa que se lea |
| `marca` | 3:1 | Series, barras, puntos — el dato mismo |
| `mobiliario` | exento | Retícula, borde, línea base |
| `superficie` | — | Fondos: se mide contra ellos |

La exención del mobiliario es deliberada y se declara token por token. Las líneas de retícula tienen
que quedar **por debajo** del dato; exigirles 3:1 haría que compitieran con él. Esa es también la
razón por la que la compuerta es creíble: si fallara permanentemente en la retícula, alguien la
apagaría, y con ella las comprobaciones que sí importan.

{{< include _includes/rules/UMB-COL-005.md >}}

{{< include _includes/rules/UMB-COL-006.md >}}

## La matriz de contraste

Generada en cada build desde `tokens/build/contrast.json`. No es una opinión de revisión: es una
compuerta que bloquea el release.

{{< include _includes/contrast-matrix.md >}}

::: {.callout-note}
## Qué cambió respecto a v1.0

`caption` pasó de 2.37:1 a 4.51:1 y `muted` de 4.25:1 a 6.08:1 en modo laboratorio; `caption` de
2.93:1 a 4.51:1 en instrumento. Las correcciones mantienen el tono exacto y mueven solo la
luminosidad, de modo que cada token sigue siendo reconociblemente el mismo color.

`muted` se oscureció **más allá** del mínimo a propósito: puesto justo en el umbral quedaba en la
misma luminosidad que `caption` y los dos tokens colapsaban en un solo gris.
:::

## La señal

{{< include _includes/rules/UMB-COL-004.md >}}

`signal` existe en dos variantes porque hace dos trabajos con umbrales distintos:

- **`signal`** es la marca de datos. Le aplica 3:1.
- **`signal-text`** es cualquier texto o enlace en color señal. Le aplica 4.5:1.

Lo mismo vale para `model-text` y `alert-text`. La razón es que la marca obliga a **etiquetar las
series directamente al final de la línea** en vez de usar una caja de leyenda — y una etiqueta de
serie es texto pequeño, no una marca.

## Las series categóricas

{{< include _includes/series-palette.md >}}

{{< include _includes/rules/UMB-COL-008.md >}}

::: {.callout-important}
## El punto débil heredado

`signal` y `model` son **indistinguibles bajo tritanopía** (separación OKLab 0.014). Se hereda de
v1.0 y no puede corregirse sin cambiar un color que define la marca.

La mitigación no es cosmética: es la etiqueta directa obligatoria (UMB-CHT-005) y la prohibición de
codificar significado solo con color (UMB-A11Y-005). Si respetas esas dos reglas, la debilidad de la
paleta no llega al lector.
:::

## Rampas

Tres rampas, todas derivadas en OKLCH con pasos de luminosidad perceptualmente parejos:

| Rampa | Para qué |
|---|---|
| Secuencial `signal` (7 pasos) | Intensidad de una variable. La rampa por defecto de un coroplético. |
| Secuencial `model` (7 pasos) | Una segunda variable, **nunca en la misma figura** que la anterior. |
| Divergente `alert`→neutro→`signal` (9 pasos) | Cambio, superávit/déficit, por encima/por debajo de lo esperado. |

{{< include _includes/rules/UMB-COL-009.md >}}

El punto neutro de la divergente está deliberadamente cerca del fondo de la página, para que «sin
cambio» se lea como ausencia de énfasis y no como una categoría más.

{{< include _includes/rules/UMB-COL-010.md >}}

## Prohibiciones

{{< include _includes/rules/UMB-COL-001.md >}}

{{< include _includes/rules/UMB-COL-003.md >}}

{{< include _includes/rules/UMB-COL-002.md >}}
