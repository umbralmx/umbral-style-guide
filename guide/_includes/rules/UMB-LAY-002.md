<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-LAY-002" data-severity="error">

**■ UMB-LAY-002** · Layout · error

### No hay sombras; las reglas de 1px hacen el trabajo estructural

La profundidad falsa compite con el dato. Una regla de 1px separa igual y no añade ruido visual.

| | |
|---|---|
| **Sí** | 1px sólido en var(--u-border). |
| **No** | box-shadow con desenfoque o desplazamiento; tarjetas elevadas. |

**Excepciones**

- box-shadow con `inset` usado para dibujar una regla —por ejemplo `inset 4px 0 0 var(--u-signal)`— no es una sombra. cabildo-libre lo usa así.

*Comprobación:* Automática — `umbral-lint`, comprobación `no-drop-shadow`.

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
