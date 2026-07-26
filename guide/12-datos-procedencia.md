---
title: "Datos y procedencia"
lang: es
---

# 12 · Datos y procedencia

> Si una cifra no se puede reproducir, no se publica.

Es el criterio que separa un laboratorio de un blog con gráficas.

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
de diferencia parecen contradecirse, y no hay forma de saber cuál estaba bien.

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

`make all` reconstruye cada figura desde `data/raw/`. Toda cifra publicada tiene que rastrearse
hasta una transformación programada, nunca hasta una edición manual.

## Nombres y claves

- Archivos y columnas en `snake_case`.
- Español o inglés, pero consistente dentro de un repositorio.
- Fechas ISO.
- Entidades por clave INEGI/CVEGEO, **nunca** por nombre libre. Ver [10 · Mapas](10-mapas.md).
- Claves geográficas como texto, con sus ceros a la izquierda.

## Huecos

{{< include _includes/rules/UMB-DAT-005.md >}}

El hueco es información. Declararlo con su magnitud:

> Vacíos conocidos, declarados y no imputados: 27 sesiones cuyo órden del día no aparece en el
> índice oficial, una sesión sin fecha publicada, y enlaces PDF de 2013–2014 que el servidor del
> ayuntamiento ya no resuelve. Se conservan en los datos tal como están.

Ese párrafo es de `cabildo-libre` y es el modelo del laboratorio: dice qué falta, cuánto falta, y
que no se rellenó.

## Licencias

{{< include _includes/rules/UMB-DAT-004.md >}}

- Código: **MIT** (`LICENSE-CODE`)
- Datos y contenido: **CC BY 4.0** (`LICENSE-CONTENT`)

Los datos públicos regresan al público, mejorados. Publica el CSV limpio junto a la figura, no solo
la figura.

## Contenido generado por modelos

Si un modelo produjo parte de lo publicado —un resumen, una clasificación, una extracción de OCR—
**dilo en la página**, no en el repositorio.

`cabildo-libre` lo hace bien: declara que los resúmenes son generados por IA sobre texto OCR, que
pueden contener errores, que cuando el acta no declara un resultado se marca «sin resultado
registrado» en vez de inventarlo, y que el enlace lleva siempre al documento original.
