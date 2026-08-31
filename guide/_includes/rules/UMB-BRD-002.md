<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-BRD-002 data-severity="error"}

**■ UMB-BRD-002** · Marca · error

### La barra del isotipo guarda proporción 5:44 y cruza a la izquierda del centro

Es la única regla geométrica que la marca enuncia sobre sí misma. En v1.0 los archivos entregados tenían tres proporciones distintas: 5:44 documentada, 1:7.13 en el isotipo y 1:6.29 en el lockup. El lockup además cruzaba a la derecha.

| | |
|---|---|
| **Sí** | Genera todas las variantes desde la fuente paramétrica única. |
| **No** | No redibujes el isotipo a mano. No escales la barra por separado. |

*Comprobación:* Automática — `logo-build`, comprobación `logo-geometry`.

*Origen:* audit/2026-07-conformance.md §3.5; decisión OQ-007.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
