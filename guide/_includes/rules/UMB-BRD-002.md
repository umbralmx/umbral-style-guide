<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-BRD-002" data-severity="error">

**■ UMB-BRD-002** · Marca · error

### La barra del isotipo guarda proporción 5:44 y cruza a la izquierda del centro

La barra es la señal cruzando el umbral de significancia; que cruce a la izquierda del centro es la única regla geométrica que la marca enuncia. En v1.0 los archivos entregados tenían tres proporciones distintas (5:44 documentada, 1:7.13 en el isotipo, 1:6.29 en el lockup) y el lockup cruzaba a la derecha.

| | |
|---|---|
| **Sí** | Generar todas las variantes desde la fuente paramétrica única. |
| **No** | Redibujar el isotipo a mano o escalar la barra por separado. |

*Comprobación:* Automática — `logo-build`, comprobación `logo-geometry`.

*Origen:* audit/2026-07-conformance.md §3.5; decisión OQ-007.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
