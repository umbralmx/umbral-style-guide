---
title: "Superficie · Web"
lang: es
---

# Web

**Modo laboratorio (claro).** El sitio, los micrositios de proyecto y los informes.

La página de entrada tiene su propia hoja: ver [portada](landing.md).

## Arranque

```html
<html lang="es">
<head>
  <link rel="stylesheet" href="/assets/fonts/fonts.css">
  <link rel="stylesheet" href="/assets/tokens.css">
</head>
```

Las fuentes se auto-hospedan (UMB-TYP-005). No copies un `@import` a Google Fonts de ningún
documento antiguo.

```css
body { background: var(--u-base); color: var(--u-ink); font-family: var(--u-font-body); }
h1, h2, h3 {
  font-family: var(--u-font-display);
  font-weight: var(--u-weight-display);
  letter-spacing: var(--u-tracking-display);
}
.mono, [data-numeric] { font-family: var(--u-font-mono); font-variant-numeric: tabular-nums; }
main { max-width: var(--u-measure); }
```

## Estructura

- **Marca:** al principio del contenido, alineada con el titular. Una barra de encabezado solo se
  justifica cuando hay navegación real que mostrar.
- **Héroe:** titular de Space Grotesk 500 en dos líneas como máximo, un acento en señal, y una
  oración de apoyo.
- **Secciones:** etiqueta en mono minúsculas, contenido en filas separadas por reglas de 1px. Ver
  [04 · Layout](../04-layout.md).
- **Pie:** licencia del código, licencia de los datos, enlace al repositorio.

## Secciones oscuras

Una sección con `data-mode="instrumento"` es una superficie distinta, no un panel mezclado. Está
permitido. Lo que no está permitido es una tarjeta clara dentro de una sección oscura.

## Metadatos sociales

```html
<meta property="og:title" content="El hallazgo, como oración">
<meta property="og:description" content="Geografía · periodo · unidad">
<meta property="og:image" content="https://umbral.mx/og/proyecto.png">
<meta name="twitter:card" content="summary_large_image">
```

La tarjeta OG es de 1200×630, en modo instrumento, y lleva **una** cifra grande. Ver
[social.md](social.md).

## Antes de publicar

- [ ] `lang="es"` correcto
- [ ] Fuentes desde `assets/fonts/`, ninguna petición a un CDN
- [ ] Ningún hex escrito a mano
- [ ] Toda gráfica: título-hallazgo, subtítulo, fuente, `aria-label`, CSV
- [ ] Un solo elemento en señal en la capa de datos
- [ ] Etiquetas de sección en mono minúsculas; listas en filas, no en tarjetas
- [ ] `:focus-visible` visible; `prefers-reduced-motion` respetado
