<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-LAY-003" data-severity="warning">

**▲ UMB-LAY-003** · Layout · advertencia

### La medida del texto no pasa de 65 caracteres

Más allá de esa medida el ojo pierde el renglón al volver. Es la diferencia entre un informe que se lee y uno que se hojea.

| | |
|---|---|
| **Sí** | max-width: var(--u-measure). |
| **No** | Párrafos a todo el ancho de la ventana. |

*Comprobación:* Automática — `umbral-lint`, comprobación `measure-max`.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
