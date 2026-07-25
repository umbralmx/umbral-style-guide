<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-COL-005" data-severity="error">

**■ UMB-COL-005** · Color · error

### Todo texto alcanza 4.5:1 contra base y contra panel

Es un laboratorio de interés público: la lectura no puede depender de tener buena vista y una buena pantalla. v1.0 afirmaba cumplir AA en ambos modos y no lo cumplía en cuatro pares; el 44% del texto del sitio principal fallaba.

| | |
|---|---|
| **Sí** | Usar ink, muted, caption y las variantes *-text, que la compuerta ya verifica. |
| **No** | Usar signal, model o alert como color de texto pequeño en modo laboratorio. |

*Comprobación:* Automática — `verify-tokens`, comprobación `contrast-text`.

*Origen:* umbral-engineering.md §4 afirmaba lo contrario; audit §2.

*Ver también:* UMB-COL-006 · UMB-A11Y-005

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
