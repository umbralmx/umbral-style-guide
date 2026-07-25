<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-COL-002" data-severity="error">

**■ UMB-COL-002** · Color · error

### Ningún color se escribe a mano: todos vienen de los tokens

Un valor enunciado en dos lugares deja de coincidir. Así fue como el mplstyle de v1.0 terminó con una tercera serie distinta a la de su propio brand book.

| | |
|---|---|
| **Sí** | var(--u-signal), tokens['signal'], umbral_laboratorio$signal. |
| **No** | #128273 escrito directamente en una hoja de estilo, un notebook o una gráfica. |

*Comprobación:* Automática — `umbral-lint`, comprobación `hardcoded-token-hex`.

*Origen:* CLAUDE.md §2; audit §3.5.

*Ver también:* UMB-PRO-003

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
