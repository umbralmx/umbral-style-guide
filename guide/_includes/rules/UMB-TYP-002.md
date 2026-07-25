<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-TYP-002" data-severity="error">

**■ UMB-TYP-002** · Tipografía · error

### Solo se usan Space Grotesk, IBM Plex Sans e IBM Plex Mono

La tipografía es la mitad de la identidad. Una sustitución silenciosa por la fuente por defecto del framework deshace el sistema sin que nadie lo note.

| | |
|---|---|
| **Sí** | Declarar las tres familias y auto-hospedarlas. |
| **No** | Inter, Roboto, Arial, Helvetica, o la Source Sans que Streamlit trae por defecto. |

*Comprobación:* Automática — `umbral-lint`, comprobación `banned-font-family`.

*Origen:* Brand book p.04 «NUNCA»; medido: Source Sans renderizando en pautamx por font = "sans serif".

<small>Desde v1.0. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
