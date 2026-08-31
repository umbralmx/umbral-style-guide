---
title: "Datos y procedencia"
lang: es
---

# 12 · Datos y procedencia

> Si una cifra no se puede reproducir, no se publica.

## `SOURCE.md`

{{< include _includes/rules/UMB-DAT-001.md >}}

Todo directorio bajo `data/raw/` lleva el suyo:

```markdown
# RNPDNO — Registro Nacional de Personas Desaparecidas y No Localizadas

- **Origen:** https://versionpublicarnpdno.segob.gob.mx/
<!-- umbral-lint: ignore[terminology] — «Desaparecidas o no localizadas» es la etiqueta del RNPDNO -->
- **Institución:** Comisión Nacional de Búsqueda (CNB) / SEGOB
- **Descargado por:** jballesterosc
- **Fecha de descarga:** 2026-07-09
- **Snapshot:** `rnpdno-2026-07`
- **Licencia:** datos abiertos de gobierno; publicación derivada bajo CC BY 4.0
- **Método:** consulta programada del tablero público; cada respuesta cruda cacheada
- **Limitaciones conocidas:**
  - Registro vivo: los conteos de meses pasados cambian entre consultas.
  - 39,065 registros sin fecha de hechos, excluidos de las series temporales.
  - Los totales se concilian contra el tablero oficial; ver `checks/`.
```

Las **limitaciones conocidas** son la parte que importa. Un `SOURCE.md` sin ellas suele significar
que nadie miró el dato con suficiente cuidado.

## Snapshots

{{< include _includes/rules/UMB-DAT-002.md >}}

Los registros vivos cambian. Sin etiqueta de snapshot, dos gráficas correctas hechas con dos semanas
de diferencia parecen contradecirse. Nadie puede saber cuál estaba bien.

- Formato: `fuente-AAAA-MM` → `rnpdno-2026-07`
- Los datos crudos son **inmutables** una vez etiquetados.
- La etiqueta aparece en la línea de fuente de toda gráfica que la use.

## Estructura del repositorio

```
data/
  raw/           inmutable, tal como se descargó, con SOURCE.md
  processed/     salida del build; regenerable, no se versiona
src/             el pipeline
notebooks/       exploración
output/          figuras y CSV publicados
```

{{< include _includes/rules/UMB-DAT-003.md >}}

`make all` reconstruye cada figura desde `data/raw/`. Toda cifra publicada se rastrea hasta una
transformación programada, nunca hasta una edición manual.

## Nombres y claves

- Archivos y columnas en `snake_case`.
- Español o inglés, pero consistente dentro de un repositorio.
- Fechas ISO.
- Entidades por clave INEGI/CVEGEO, **nunca** por nombre libre. Ver [10 · Mapas](10-mapas.md).
- Claves geográficas como texto, con sus ceros a la izquierda.

## Huecos

{{< include _includes/rules/UMB-DAT-005.md >}}

El hueco es información. Declara su magnitud:

> Vacíos conocidos, declarados y no imputados: 27 sesiones cuyo órden del día no aparece en el
> índice oficial. Una sesión sin fecha publicada. Enlaces PDF de 2013–2014 que el servidor del
> ayuntamiento ya no resuelve. Se conservan en los datos tal como están.

Ese párrafo es de `cabildo-libre` y es el modelo del laboratorio. Dice qué falta, cuánto falta, y
que no se rellenó.

## Licencias

{{< include _includes/rules/UMB-DAT-004.md >}}

- Código: **MIT** (`LICENSE-CODE`)
- Datos y contenido: **CC BY 4.0** (`LICENSE-CONTENT`)

Publica el CSV limpio junto a la figura, no solo la figura.

## Contenido generado por modelos

Si un modelo produjo parte de lo publicado —un resumen, una clasificación, una extracción de OCR—
**dilo en la página**, no en el repositorio.

`cabildo-libre` lo hace bien. Declara cuatro cosas en la propia página:

1. Los resúmenes son generados por IA sobre texto OCR.
2. Pueden contener errores.
3. Un acta que no declara resultado se marca «sin resultado registrado», nunca se inventa.
4. El enlace lleva siempre al documento original.
