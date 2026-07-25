---
title: "Superficie · Social"
lang: es
---

# Social

**Modo instrumento (oscuro).** Tarjetas para redes y previsualizaciones OG.

Una tarjeta social viaja sola, sin su página. Todo lo necesario para no malinterpretarla tiene que
estar dentro de la imagen.

## Formatos

| Uso | Tamaño |
|---|---|
| Post cuadrado | 1080 × 1080 |
| Previsualización OG / Twitter | 1200 × 630 |
| Story | 1080 × 1920 |

## Composición

```
┌──────────────────────────────────┐
│  ─┼─                             │   isotipo, arriba a la izquierda
│                                  │
│  351,057                         │   UNA cifra, Space Grotesk 500, enorme
│                                  │
│  registros en el RNPDNO con      │   una línea de explicación
│  hechos entre 2010 y 2026        │
│                                  │
│  Fuente: RNPDNO · rnpdno-2026-07 │   fuente en mono, siempre
│  umbral_                    ─────│
└──────────────────────────────────┘
```

- **Una** cifra. Si hay dos, son dos tarjetas.
- La cifra en Space Grotesk 500 — es una cifra heroica suelta, no una columna que se compara
  (UMB-TYP-004).
- Una línea de explicación que incluya periodo y unidad.
- Línea de fuente en mono, con la etiqueta del snapshot. **No es opcional en social**: es
  precisamente donde la gráfica se separa de su contexto.
- `umbral_` en mono abajo.

## Gráficas en social

Si la tarjeta lleva gráfica en vez de cifra: mismo marco de siempre —título-hallazgo, subtítulo,
línea de fuente— con tipografía más grande. Nada por debajo de 24px al tamaño de exportación.

Sin leyenda: etiqueta directa, como en cualquier otra superficie.

## Accesibilidad

Una imagen no tiene tabla ni CSV, así que:

- El texto alternativo del post lleva **el hallazgo y la cifra**, no «gráfica de líneas».
- El post enlaza a la página donde están el CSV y la tabla.
- Contraste comprobado igual que en cualquier otra superficie: la tarjeta usa los mismos tokens.

## Lo que no se hace

- Emoji, ni en la imagen ni en el texto del post.
- Signos de exclamación.
- Cifras sin periodo o sin unidad.
- Recortar una gráfica para que quepa y perder la línea de fuente.
- Publicar una proyección sin su banda.
