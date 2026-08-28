<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-VOZ-004 data-severity="error"}

**■ UMB-VOZ-004** · Voz · error

### No se publica contenido de relleno

Un «Lorem ipsum» en producción dice que nadie revisó la página. Eso contamina la credibilidad de los números que están al lado.

| | |
|---|---|
| **Sí** | Publica la sección cuando su texto exista. |
| **No** | No dejes Lorem ipsum, «foto», «TODO» ni una biografía sin escribir. |

*Comprobación:* Automática — `umbral-lint`, comprobación `placeholder-content`.

*Origen:* Medido: las dos biografías de umbralmx.github.io son Lorem ipsum.

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
