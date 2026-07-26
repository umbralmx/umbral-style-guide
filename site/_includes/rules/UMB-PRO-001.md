<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-PRO-001 data-severity="error"}

**■ UMB-PRO-001** · Proceso · error

### Los archivos generados nunca se editan a mano

Editar la salida rompe la cadena normativa en silencio: la fuente y lo publicado dejan de coincidir y nada lo detecta hasta que alguien reconstruye.

| | |
|---|---|
| **Sí** | Cambiar tokens/src/ o rules/rules.yaml y reconstruir. |
| **No** | Corregir un hex en tokens/build/tokens.css. |

*Comprobación:* Automática — `umbral-lint`, comprobación `generated-file-edited`.

*Origen:* CLAUDE.md §2, tercera consecuencia dura; formalizada como regla en 1.1.

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
