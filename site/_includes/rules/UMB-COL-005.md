<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-005 data-severity="error"}

**■ UMB-COL-005** · Color · error

### Todo texto alcanza 4.5:1 contra base y contra panel

Leer al laboratorio no puede depender de tener buena vista ni buena pantalla. v1.0 afirmaba cumplir AA en ambos modos. Cuatro pares no lo cumplían y el 44% del texto del sitio principal fallaba.

| | |
|---|---|
| **Sí** | Usa ink, muted, caption y las variantes *-text. La compuerta ya las verifica. |
| **No** | No uses signal, model ni alert como color de texto pequeño en modo laboratorio. |

*Comprobación:* Automática — `verify-tokens`, comprobación `contrast-text`.

*Origen:* umbral-engineering.md §4 afirmaba lo contrario; audit §2.

*Ver también:* UMB-COL-006 · UMB-A11Y-005

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
