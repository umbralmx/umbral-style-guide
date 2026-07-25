<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-COL-004" data-severity="error">

**■ UMB-COL-004** · Color · error

### El color signal se usa en un solo elemento de la capa de datos por vista

La jerarquía visual de Umbral depende de que exista un único punto de atención. Si todo resalta, nada resalta. El alcance se limita a la capa de datos porque Streamlit aplica primaryColor a todos sus widgets a la vez y no existe configuración que lo restrinja a un elemento.

| | |
|---|---|
| **Sí** | Una serie, una cifra o un elemento de UI en signal. |
| **No** | Signal en el logo, el botón y la serie principal a la vez. |

*Comprobación:* Automática — `umbral-lint`, comprobación `signal-count`.

*Nota:* Se evalúa sobre la salida renderizada de la gráfica, no sobre el HTML completo de la página — consecuencia de acotar la regla a la capa de datos (OQ-002).

*Origen:* Brand book p.03 «La señal es sagrada»; medido: 17 elementos en desaparecidosmx, 10 en pautamx, 4 en cabildo-libre.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
