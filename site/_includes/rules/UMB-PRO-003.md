<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-PRO-003 data-severity="error"}

**■ UMB-PRO-003** · Proceso · error

### Ningún archivo fuera de tokens/src/ escribe un valor que ya existe como token

Así se produce la deriva. Alguien copia el valor una vez, la fuente cambia, y la copia se queda.

| | |
|---|---|
| **Sí** | Importa el valor desde tokens/build/. |
| **No** | No pegues #128273 en un notebook. |

*Comprobación:* Automática — `umbral-lint`, comprobación `hardcoded-value`.

*Ver también:* UMB-COL-002

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
