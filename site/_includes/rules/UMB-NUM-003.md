<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-NUM-003 data-severity="warning"}

**▲ UMB-NUM-003** · Números y unidades · advertencia

### Las fechas van en ISO dentro de los datos y en prosa dentro del texto

ISO ordena y no es ambiguo entre convenciones. En prosa se lee mal.

| | |
|---|---|
| **Sí** | Escribe 2026-07 en datos y etiquetas. Escribe julio de 2026 en el texto. |
| **No** | No escribas 07/06/2026. Significa cosas distintas en México y en Estados Unidos. |

*Comprobación:* Automática — `umbral-lint`, comprobación `date-format`.

*Origen:* KICKOFF §3.4; convención ya usada por desaparecidosmx (2010-01) y cabildo-libre.

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
