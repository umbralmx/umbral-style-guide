---
title: "Superficie · Streamlit"
lang: es
---

# Streamlit

**Modo instrumento (oscuro).** Los tableros en vivo: `desaparecidosmx`, `pautamx`.

## `.streamlit/config.toml`

Copia el archivo **generado**, no lo escribas:

```bash
cp tokens/build/streamlit-config.toml .streamlit/config.toml
```

```toml
[theme]
base                     = "dark"
primaryColor             = "#5fd4c4"
backgroundColor          = "#101418"
secondaryBackgroundColor = "#171c22"
textColor                = "#edf1f4"
font                     = "IBM Plex Sans, sans-serif"
```

::: {.u-note}
**dos errores heredados de v1.0**

1. Las claves aparecían como `sc-camel-primary-color`. Es un artefacto del export a PDF. Las claves
   reales son las de arriba.
2. El brand book fijaba `font = "sans serif"`. Es un valor válido de Streamlit y significa *la
   Source Sans de Streamlit*. No era una errata: estaba mal. Por eso `pautamx` renderiza Source Sans
   hoy.

Corregir solo los nombres de las claves deja el segundo defecto en pie.
:::

## Fuentes y tipografía

```python
st.markdown("""<style>
@font-face { font-family: 'Space Grotesk'; src: url('app/static/fonts/space-grotesk-500.woff2'); font-weight: 500 }
h1, h2, h3 { font-family: 'Space Grotesk'; font-weight: 500; letter-spacing: -.02em }
[data-testid="stMetricValue"] { font-family: 'IBM Plex Mono'; font-variant-numeric: tabular-nums }
</style>""", unsafe_allow_html=True)
```

Las cifras de `st.metric` van en **mono**, no en display. Son una fila de KPIs que se compara
columna contra columna (UMB-TYP-004).

## El atributo `lang`

Streamlit fija `lang="en"` y no lo expone. Para una app en español hay que corregirlo:

```python
import streamlit.components.v1 as components

components.html(
    "<script>window.parent.document.documentElement.lang = 'es';</script>",
    height=0,
)
```

Una llamada, al principio de la app. Sin esto, un lector de pantalla pronuncia todo el tablero con
fonética inglesa (UMB-A11Y-001).

## La señal en Streamlit

`primaryColor` se aplica a la vez a deslizadores, chips de multiselect, pestañas, enlaces y anillos
de foco. **No existe configuración que lo restrinja a un elemento.**

Por eso UMB-COL-004 está acotada a la capa de datos. En un tablero, la regla significa una sola
serie en señal por gráfica. El cromo de los widgets está exento. No es una licencia: es el
reconocimiento de un límite del framework.

## Gráficas

```python
import json, plotly.graph_objects as go
tpl = json.load(open("tokens/build/plotly-umbral-instrumento.json"))
fig.update_layout(**tpl["layout"])
```

Cada gráfica lleva su título-hallazgo, su subtítulo, su línea de fuente en `st.caption`, y su botón
de descarga:

```python
st.download_button("Descargar CSV", df.to_csv(index=False), "serie.csv", "text/csv")
```

::: {.u-note}
**medido** · `pautamx` no tiene ningún botón de descarga. `desaparecidosmx` sí. Es la diferencia más
visible entre los dos tableros, y la más fácil de corregir (UMB-A11Y-004).
:::

## Antes de publicar

- [ ] `config.toml` copiado del generado; `font` **no** es `"sans serif"`
- [ ] El shim de `lang` está puesto
- [ ] Nada por debajo de 12px
- [ ] Ningún `#ffffff` filtrándose de los valores por defecto de Streamlit
- [ ] Una serie en señal por gráfica
- [ ] Toda gráfica: `aria-label`, `st.caption` con la fuente, botón de CSV
