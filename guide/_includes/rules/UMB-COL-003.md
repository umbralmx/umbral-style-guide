<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-COL-003" data-severity="error">

**■ UMB-COL-003** · Color · error

### No se usan degradados

El degradado introduce una variación de color que no codifica nada. En una gráfica compite con la escala; en la interfaz es decoración.

| | |
|---|---|
| **Sí** | Rellenos sólidos; una rampa secuencial si hay que codificar intensidad. |
| **No** | linear-gradient decorativo, fondos con degradado, barras degradadas. |

**Excepciones**

- Un linear-gradient de un solo color usado para dibujar una regla de 1px es una técnica de layout, no un degradado. cabildo-libre lo usa correctamente.

*Comprobación:* Automática — `umbral-lint`, comprobación `no-gradient`.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
