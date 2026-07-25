<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-PRO-003" data-severity="error">

**■ UMB-PRO-003** · Proceso · error

### Ningún archivo fuera de tokens/src/ escribe un valor que ya existe como token

Es la forma concreta que toma la deriva: el valor se copia una vez, la fuente cambia, y la copia se queda.

| | |
|---|---|
| **Sí** | Importar desde tokens/build/. |
| **No** | Pegar #128273 en un notebook. |

*Comprobación:* Automática — `umbral-lint`, comprobación `hardcoded-value`.

*Ver también:* UMB-COL-002

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
