<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-PRO-004" data-severity="error">

**■ UMB-PRO-004** · Proceso · error

### Cambiar el valor de un token es un cambio MAYOR de versión

El semver aplica al sistema de diseño, no solo al código: un token que cambia re-renderiza todos los productos que lo consumen.

| | |
|---|---|
| **Sí** | MAYOR para un valor de token o una regla que sube a error; MENOR para una regla nueva en warning; PARCHE para prosa. |
| **No** | Cambiar un hex en un parche. |

*Comprobación:* Manual. Se verifica al preparar el release, contra CHANGELOG.md.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
