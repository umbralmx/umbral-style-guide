<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-CHT-007" data-severity="warning">

**▲ UMB-CHT-007** · Gráficas · advertencia

### Los ejes van en mono, abreviados, con coma como separador de miles

Los numerales tabulares alinean los dígitos y hacen comparable el eje de un vistazo.

| | |
|---|---|
| **Sí** | 12k, 3.7M, 351,057. |
| **No** | 12000, 3700000, o cifras en la tipografía de cuerpo. |

*Comprobación:* Automática — `umbral-lint`, comprobación `axis-mono`.

*Ver también:* UMB-NUM-001 · UMB-NUM-002

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
