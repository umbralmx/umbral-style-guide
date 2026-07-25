---
title: "Interpretabilidad y honestidad"
lang: es
---

# 13 · Interpretabilidad y honestidad

Es la credibilidad del laboratorio. Se aplica en revisión, no solo en diseño.

## Descriptivo o causal

{{< include _includes/rules/UMB-MET-001.md >}}

| Diseño | Verbos permitidos |
|---|---|
| Serie de tiempo, corte transversal, correlación | «asociado con», «coincide con», «correlaciona», «es mayor en» |
| RCT, diferencias-en-diferencias, regresión discontinua, variables instrumentales | «efecto», «reduce», «aumenta», «causa» |

Cuando uses un verbo causal, la estrategia y su supuesto clave van **junto al estimado**:

> El programa redujo los homicidios en 2.4 por 100 mil (IC 95%: 0.7 a 4.1), estimado con
> diferencias-en-diferencias contra municipios vecinos que no lo adoptaron. El supuesto clave es que
> ambos grupos habrían seguido tendencias paralelas; la figura 3 muestra las tendencias previas.

Sin esa oración, el estimado no es interpretable. Con ella, alguien puede discutirlo — que es el
punto.

## El titular responde por la figura

{{< include _includes/rules/UMB-MET-002.md >}}

Un titular causal sobre una gráfica descriptiva es la forma más común de esta falla, y no se
corrige poniendo un descargo debajo: el titular es lo que la gente lee y comparte.

## Denominadores

{{< include _includes/rules/UMB-MET-003.md >}}

Comparar el conteo del Estado de México con el de Colima mide población, no incidencia. Ver
[06 · Números](06-numeros.md) y [10 · Mapas](10-mapas.md).

## Ejes honestos

- Barras desde cero, sin excepción.
- Cualquier truncamiento anotado en la propia figura.
- Sin doble eje.
- Escala logarítmica solo cuando el crecimiento multiplicativo es el punto, y siempre etiquetada.

## Los huecos se muestran

Un hueco declarado es un dato. Un hueco recortado es una afirmación falsa por omisión. Ver
[12 · Datos y procedencia](12-datos-procedencia.md).

Cuidado especial con el subreporte reciente: en un registro vivo, el último tramo de la serie
siempre baja, y siempre se lee como una mejora. Ver [09 · Incertidumbre](09-incertidumbre.md).

## Dignidad

{{< include _includes/rules/UMB-MET-004.md >}}

Detrás de cada registro del RNPDNO hay una persona y una familia, y muchas veces una búsqueda en
curso.

- Se cuenta a las personas; no se hace espectáculo con ellas.
- Sin mapeo a individuos identificables, ni siquiera con datos técnicamente públicos: la agregación
  a nivel municipal es el piso.
- Sin fotografías, sin narrativas de caso para ilustrar una tendencia.
- Sin adjetivos que dramaticen el conteo. La cifra ya es grave.
- Antes de publicar un desglose fino, pregunta si puede poner a alguien en riesgo. Ante la duda,
  agrega.

{{< include _includes/rules/UMB-MET-005.md >}}

La terminología no es preferencia de estilo: ver [15 · Terminología](15-terminologia.md).

## Antes de publicar

- [ ] ¿El titular se sostiene con la figura que está debajo?
- [ ] ¿Los verbos coinciden con el diseño de identificación que realmente se usó?
- [ ] ¿Está visible la incertidumbre?
- [ ] ¿Las comparaciones están normalizadas?
- [ ] ¿Los huecos están declarados?
- [ ] ¿Alguien podría ser identificado a partir de esto?
- [ ] ¿La terminología sigue el glosario?
