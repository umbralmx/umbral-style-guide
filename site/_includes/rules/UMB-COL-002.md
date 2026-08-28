<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-002 data-severity="error"}

**■ UMB-COL-002** · Color · error

### Ningún color se escribe a mano: todos vienen de los tokens

Un valor enunciado en dos lugares deja de coincidir. Así fue como el mplstyle de v1.0 terminó con una tercera serie distinta a la de su propio brand book.

| | |
|---|---|
| **Sí** | Lee el valor desde var(--u-signal), tokens['signal'] o umbral_laboratorio$signal. |
| **No** | No escribas #128273 en una hoja de estilo, un notebook ni una gráfica. |

*Comprobación:* Automática — `umbral-lint`, comprobación `hardcoded-token-hex`.

*Origen:* CLAUDE.md §2; audit §3.5.

*Ver también:* UMB-PRO-003

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
