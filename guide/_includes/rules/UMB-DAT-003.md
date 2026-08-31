<!-- GENERATED from rules/rules.yaml. Do not edit. -->
::: {.u-rule #UMB-DAT-003 data-severity="error"}

**■ UMB-DAT-003** · Datos y procedencia · error

### Toda figura publicada se reconstruye desde el dato crudo con un solo comando

Si una cifra no se puede reproducir, no se puede defender. Es el criterio que separa un laboratorio de un blog con gráficas.

| | |
|---|---|
| **Sí** | Haz que `make all` reconstruya cada figura desde data/raw/. |
| **No** | No publiques una cifra que salió de una edición manual en una hoja de cálculo. |

*Comprobación:* Manual. Se verifica en revisión de PR ejecutando el comando de build declarado.

<small>Desde v1.0. Regla normativa: `rules/rules.yaml`.</small>

:::
