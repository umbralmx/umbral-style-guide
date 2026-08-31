<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-NUM-006 data-severity="error"}

**■ UMB-NUM-006** · Números y unidades · error

### Cero, nulo y suprimido se escriben distinto y significan distinto

Convertir un nulo en cero es una imputación silenciosa. En datos de desaparición o de delito cambia la afirmación.

| | |
|---|---|
| **Sí** | Escribe 0 · «sin dato» · «suprimido (< umbral de reporte)». |
| **No** | No rellenes los huecos con 0 al construir la serie. |

*Comprobación:* En revisión.

*Origen:* KICKOFF §3.4 (nulo vs cero vs suprimido); cabildo-libre ya declara sus huecos sin imputarlos.

*Ver también:* UMB-COL-010 · UMB-DAT-005

<small>Desde v1.1. Regla normativa: `rules/rules.yaml`.</small>

:::
