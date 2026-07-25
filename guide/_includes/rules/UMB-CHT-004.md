<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-CHT-004" data-severity="error">

**■ UMB-CHT-004** · Gráficas · error

### Solo hay líneas de retícula horizontales, con la línea base más oscura

La retícula vertical rara vez ayuda a leer un valor y sí ensucia. La línea base más oscura ancla el cero.

| | |
|---|---|
| **Sí** | y.grid = true, x.grid = false, base en --u-baseline. |
| **No** | Retícula en ambos ejes, o marco alrededor de la gráfica. |

*Comprobación:* Automática — `umbral-lint`, comprobación `gridlines-horizontal`.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
