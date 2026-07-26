<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-DAT-003 data-severity="error"}

**■ UMB-DAT-003** · Datos y procedencia · error

### Toda figura publicada se reconstruye desde el dato crudo con un solo comando

Es el criterio que separa un laboratorio de un blog. Si no se puede reproducir, no se publica.

| | |
|---|---|
| **Sí** | make all reconstruye cada figura desde data/raw/. |
| **No** | Una cifra que salió de una edición manual en una hoja de cálculo. |

*Comprobación:* Manual. Se verifica en revisión de PR ejecutando el comando de build declarado.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
