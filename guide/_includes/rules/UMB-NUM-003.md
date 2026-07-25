<!-- GENERATED from rules/rules.yaml. Do not edit. -->
<div class="u-rule" id="UMB-NUM-003" data-severity="warning">

**▲ UMB-NUM-003** · Números y unidades · advertencia

### Las fechas van en ISO dentro de los datos y en prosa dentro del texto

ISO ordena y no es ambiguo entre convenciones; en prosa se lee mal.

| | |
|---|---|
| **Sí** | Datos y etiquetas: 2026-07. Texto: julio de 2026. |
| **No** | 07/06/2026, que significa cosas distintas en México y en Estados Unidos. |

*Comprobación:* Automática — `umbral-lint`, comprobación `date-format`.

*Origen:* KICKOFF §3.4; convención ya usada por desaparecidosmx (2010-01) y cabildo-libre.

<small>Desde v1.1. Regla normativa: <code>rules/rules.yaml</code>.</small>

</div>
