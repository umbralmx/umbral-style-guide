---
title: "Vocabulario visual"
lang: es
---

# 07 · Vocabulario visual

Un selector de gráfica: de la **intención** al tipo. Inspirado en el *Visual Vocabulary* del FT,
recortado a lo que el laboratorio realmente publica.

Empieza por la pregunta, nunca por el tipo de gráfica.

## Cambio en el tiempo

| Quiero mostrar… | Usa | Notas |
|---|---|---|
| Una serie a lo largo del tiempo | **Línea** | El eje y puede no empezar en cero; anota el corte |
| Varias series comparables | **Líneas múltiples** | Máximo 5; etiqueta directa al final |
| Un total compuesto | **Área apilada** | Solo si el total significa algo |
| Cambio respecto a una base | **Línea indexada** | Declara la base: `2015 = 100` |
| Proyección | **Línea + banda** | Trazo punteado pasado «hoy». Ver [09](09-incertidumbre.md) |
| Datos muy ruidosos | **Línea tenue + media móvil** | Nombra la ventana: `media móvil de 12 meses` |

## Comparación entre categorías

| Quiero mostrar… | Usa | Notas |
|---|---|---|
| Ranking | **Barras horizontales** | Ordenadas por valor, no alfabéticamente |
| Comparar pocas categorías | **Barras verticales** | Desde cero, sin excepción |
| Dos momentos por categoría | **Dumbbell** | Mejor que dos barras juntas |
| Muchas categorías | **Barras horizontales + «otros»** | Agrupa la cola; di cuántas agrupaste |

{{< include _includes/rules/UMB-CHT-008.md >}}

## Composición

| Quiero mostrar… | Usa | Notas |
|---|---|---|
| Partes de un total | **Barra apilada al 100%** | Nunca un pastel |
| Composición en el tiempo | **Área apilada al 100%** | |
| Jerarquía anidada | **Treemap** | Solo si hay una jerarquía real |

## Distribución

| Quiero mostrar… | Usa | Notas |
|---|---|---|
| Forma de una distribución | **Histograma** | Declara el ancho del bin |
| Comparar distribuciones | **Cajas** o **crestas** | Muestra *n* por grupo |
| Todos los puntos, pocos casos | **Puntos con jitter** | Preferible a una caja con n<30 |

## Relación

| Quiero mostrar… | Usa | Notas |
|---|---|---|
| Dos variables | **Dispersión** | Sin línea de tendencia salvo que el modelo esté declarado |
| Añadir una tercera | **Dispersión con tamaño** | El área codifica, no el radio |
| Correlación entre muchas | **Matriz** | Rampa divergente centrada en cero |

## Geografía

| Quiero mostrar… | Usa | Notas |
|---|---|---|
| Intensidad por unidad | **Coroplético de tasas** | Nunca de conteos. Ver [10](10-mapas.md) |
| Comparar unidades directamente | **Barras ordenadas** | Casi siempre se lee mejor que el mapa |

::: {.callout-note}
Antes de hacer un mapa, pregunta si la geografía es la variable de interés o solo el índice. Un
ranking de entidades casi siempre se lee mejor en barras ordenadas. El mapa vale cuando el patrón
**espacial** —vecindad, frontera, corredor— es el hallazgo.
:::

## Lo que no se usa nunca

{{< include _includes/rules/UMB-CHT-010.md >}}

| Prohibido | Por qué | En su lugar |
|---|---|---|
| Pastel y dona | Codifica en ángulo, que se compara mal | Barras, o barra apilada al 100% |
| Cualquier 3D | La perspectiva distorsiona el área | La versión 2D |
| Doble eje | Permite fabricar cualquier correlación aparente eligiendo escalas | Dos paneles alineados en el tiempo |
| Eje truncado sin nota | Multiplica visualmente una diferencia que no existe | Truncar y anotarlo |

## Cuántas series

{{< include _includes/rules/UMB-CHT-006.md >}}

Si hacen falta más de cinco, casi siempre son dos gráficas — o una gráfica con una serie destacada
y el resto en gris de fondo, que es la forma preferida del laboratorio: una en `signal`, las demás
en `muted`.
