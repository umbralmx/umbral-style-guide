<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-003 data-severity="error"}

**■ UMB-COL-003** · Color · error

### No se usan degradados

El degradado varía el color sin codificar nada. En una gráfica compite con la escala. En la interfaz es decoración.

| | |
|---|---|
| **Sí** | Usa rellenos sólidos. Usa una rampa secuencial si tienes que codificar intensidad. |
| **No** | No uses linear-gradient decorativo, fondos con degradado ni barras degradadas. |

**Excepciones**

- Un linear-gradient de un solo color que dibuja una regla de 1px es una técnica de layout, no un degradado. cabildo-libre lo usa así.

*Comprobación:* Automática — `umbral-lint`, comprobación `no-gradient`.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
