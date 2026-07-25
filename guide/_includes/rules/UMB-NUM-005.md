<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-NUM-005" data-severity="error">

**■ UMB-NUM-005** · Números y unidades · error

### La precisión declarada no excede la del dato

Escribir 9.24% sobre una muestra que sostiene un dígito significativo inventa exactitud. En un registro vivo que se revisa retroactivamente, además, cambia.

| | |
|---|---|
| **Sí** | Redondear a la precisión que el método sostiene y decir cuál es. |
| **No** | Arrastrar todos los decimales que devuelve el cálculo. |

*Comprobación:* En revisión.

*Origen:* KICKOFF §3.4 (redondeo y cifras significativas).

*Ver también:* UMB-CHT-012

<small>Desde v1.1. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
