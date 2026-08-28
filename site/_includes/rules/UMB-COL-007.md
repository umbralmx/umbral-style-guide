<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-COL-007 data-severity="error"}

**■ UMB-COL-007** · Color · error

### No se mezclan los dos modos dentro de un mismo panel

Los tokens cascadean por subárbol. Mezclarlos dentro de una superficie pone texto de un modo sobre fondo del otro. La compuerta de contraste no puede prever ese caso.

| | |
|---|---|
| **Sí** | Pon data-mode="instrumento" sobre un contenedor completo. |
| **No** | No pongas una tarjeta oscura dentro de un panel claro, ni al revés. |

**Excepciones**

- Dos secciones alternas de una misma página son superficies distintas, no un mismo panel.

*Comprobación:* En revisión.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
