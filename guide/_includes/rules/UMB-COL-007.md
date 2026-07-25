<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-COL-007" data-severity="error">

**■ UMB-COL-007** · Color · error

### No se mezclan los dos modos dentro de un mismo panel

Los tokens cascadean por subárbol. Mezclarlos dentro de una superficie produce texto de un modo sobre fondo del otro, que es exactamente el caso que la compuerta de contraste no puede prever.

| | |
|---|---|
| **Sí** | data-mode="instrumento" sobre un contenedor completo. |
| **No** | Un panel claro con una tarjeta oscura dentro, o al revés. |

**Excepciones**

- Secciones alternas de una misma página son superficies distintas, no un mismo panel.

*Comprobación:* Automática — `umbral-lint`, comprobación `mode-mixing`.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
