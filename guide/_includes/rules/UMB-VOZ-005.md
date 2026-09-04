<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-VOZ-005 data-severity="warning"}

**▲ UMB-VOZ-005** · Voz · advertencia

### Una oración enuncia una sola cosa y no pasa de 25 palabras

Es la disciplina de ASD-STE100 aplicada al español. Una oración larga con subordinadas admite más de una lectura, y el lector no tiene a quién preguntarle. La regla vale para la prosa técnica del laboratorio, no para una cita textual.

| | |
|---|---|
| **Sí** | Corta en la conjunción. Usa voz activa. Nombra la misma cosa con la misma palabra en todo el documento. |
| **No** | No uses punto y coma para unir dos ideas. No apiles metáforas donde cabe un dato. |

**Excepciones**

- Una cita textual se reproduce como está. Acortarla la deja de ser una cita.
- Un ADR aceptado y un registro de auditoría no se editan después de escribirse (docs/adr/README.md). La regla se aplica a los ADR nuevos, no a los ya aceptados.
- El texto de una licencia de terceros se reproduce literalmente por obligación legal.

*Comprobación:* Automática — `umbral-lint`, comprobación `long-sentence`.

*Origen:* ASD-STE100 Issue 9 (2025), reglas 5.x y 6.x. Adoptada tras reescribir la guía completa en agosto de 2026.

*Ver también:* UMB-VOZ-003 · UMB-MET-005

<small>Desde v1.2. Regla normativa: `rules/rules.yaml`.</small>

:::
