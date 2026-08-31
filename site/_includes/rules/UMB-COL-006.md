<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-006 data-severity="error"}

**■ UMB-COL-006** · Color · error

### Toda marca de datos alcanza 3:1; el mobiliario de la gráfica está exento y así se declara

WCAG 1.4.11 aplica a los gráficos necesarios para entender el contenido. Las líneas de retícula no lo son y tienen que quedar por debajo del dato. Distinguir ambos casos mantiene la compuerta de contraste encendida.

| | |
|---|---|
| **Sí** | Declara contrastRole en cada token: text, mark, furniture o surface. |
| **No** | No exijas 3:1 a una retícula. No eximas a una serie de datos. |

*Comprobación:* Automática — `verify-tokens`, comprobación `contrast-mark`.

*Origen:* Decisión OQ-001.

*Ver también:* UMB-COL-005

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
