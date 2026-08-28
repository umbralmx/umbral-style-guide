<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-PRO-004 data-severity="error"}

**■ UMB-PRO-004** · Proceso · error

### Cambiar el valor de un token es un cambio MAYOR de versión

El semver aplica al sistema de diseño, no solo al código. Un token que cambia re-renderiza todos los productos que lo consumen.

| | |
|---|---|
| **Sí** | Sube MAYOR por un valor de token o por una regla que pasa a error. Sube MENOR por una regla nueva en warning. Sube PARCHE por prosa. |
| **No** | No cambies un hex en un parche. |

*Comprobación:* Manual. Se verifica al preparar el release, contra CHANGELOG.md.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
