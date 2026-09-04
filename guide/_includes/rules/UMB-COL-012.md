<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-012 data-severity="warning"}

**▲ UMB-COL-012** · Color · advertencia

### Un color semántico se declara desde su token; no se deriva por fórmula

La compuerta de contraste mide los pares que existen en contrast.json. Un color que un framework calcula con color-mix nunca entra en esa tabla. La compuerta lo declara verde sin haberlo visto. UMB-COL-002 prohíbe el hex escrito a mano, y una fórmula no es un hex.

| | |
|---|---|
| **Sí** | Declara cada propiedad semántica de la superficie con el valor del token que le toca. |
| **No** | No dejes que el tema derive muted, faint o border desde el color de texto. |

*Comprobación:* En revisión.

*Origen:* abstract-light.css de Observable Framework deriva muted, faint, fainter y faintest con color-mix desde un solo foreground. Ver ADR-0004.

*Ver también:* UMB-COL-002 · UMB-COL-005 · UMB-COL-006

<small>Desde v1.4. Regla normativa: `rules/rules.yaml`.</small>

:::
