<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-011 data-severity="warning"}

**▲ UMB-COL-011** · Color · advertencia

### El modo lo fija el medio, no la preferencia del sistema del lector

El modo dice qué es la superficie. Laboratorio es lectura y documento. Instrumento es tablero en vivo y pantalla de monitoreo. Si prefers-color-scheme decide, dos lectores ven dos superficies distintas del mismo artefacto. La captura de pantalla deja de ser reproducible y la tarjeta social deja de coincidir con su página.

| | |
|---|---|
| **Sí** | Fija un solo modo por superficie y decláralo en la configuración. |
| **No** | No emparejes un tema claro y uno oscuro bajo prefers-color-scheme. |

*Comprobación:* En revisión.

*Origen:* Observable Framework resuelve theme «dashboard» a air y near-midnight, y envuelve cada import en una consulta prefers-color-scheme. Ver ADR-0004.

*Ver también:* UMB-COL-007 · UMB-COL-012

<small>Desde v1.4. Regla normativa: `rules/rules.yaml`.</small>

:::
