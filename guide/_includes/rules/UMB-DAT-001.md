<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-DAT-001 data-severity="error"}

**■ UMB-DAT-001** · Datos y procedencia · error

### Todo conjunto de datos lleva su SOURCE.md

Sin origen, fecha de descarga, licencia y limitaciones conocidas, nadie puede auditar el dato ni volver a bajarlo igual.

| | |
|---|---|
| **Sí** | Escribe la URL de origen, quién lo descargó, cuándo, bajo qué licencia y qué se sabe que le falta. |
| **No** | No dejes un CSV suelto en data/raw/ sin procedencia. |

*Comprobación:* Automática — `umbral-lint`, comprobación `source-md-present`.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
