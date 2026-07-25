<!-- GENERATED from the normative layer. Do not edit. -->

#### modo laboratorio

| Token | Sobre | Ratio | Rol | Umbral | |
|---|---|---|---|---|---|
| `ink` | `base` | 15.85:1 | texto | 4.5:1 | pasa |
| `ink` | `panel` | 16.88:1 | texto | 4.5:1 | pasa |
| `muted` | `base` | 6.08:1 | texto | 4.5:1 | pasa |
| `muted` | `panel` | 6.48:1 | texto | 4.5:1 | pasa |
| `caption` | `base` | 4.51:1 | texto | 4.5:1 | pasa |
| `caption` | `panel` | 4.81:1 | texto | 4.5:1 | pasa |
| `border` | `base` | 1.19:1 | mobiliario | — | exento |
| `border` | `panel` | 1.27:1 | mobiliario | — | exento |
| `gridline` | `base` | 1.10:1 | mobiliario | — | exento |
| `gridline` | `panel` | 1.18:1 | mobiliario | — | exento |
| `baseline` | `base` | 1.50:1 | mobiliario | — | exento |
| `baseline` | `panel` | 1.60:1 | mobiliario | — | exento |
| `signal` | `base` | 4.22:1 | marca | 3:1 | pasa |
| `signal` | `panel` | 4.49:1 | marca | 3:1 | pasa |
| `signal-text` | `base` | 4.51:1 | texto | 4.5:1 | pasa |
| `signal-text` | `panel` | 4.80:1 | texto | 4.5:1 | pasa |
| `model` | `base` | 4.48:1 | marca | 3:1 | pasa |
| `model` | `panel` | 4.77:1 | marca | 3:1 | pasa |
| `model-text` | `base` | 4.54:1 | texto | 4.5:1 | pasa |
| `model-text` | `panel` | 4.83:1 | texto | 4.5:1 | pasa |
| `alert` | `base` | 4.03:1 | marca | 3:1 | pasa |
| `alert` | `panel` | 4.29:1 | marca | 3:1 | pasa |
| `alert-text` | `base` | 4.55:1 | texto | 4.5:1 | pasa |
| `alert-text` | `panel` | 4.84:1 | texto | 4.5:1 | pasa |
| `series-4` | `base` | 7.49:1 | marca | 3:1 | pasa |
| `series-4` | `panel` | 7.98:1 | marca | 3:1 | pasa |
| `series-5` | `base` | 7.61:1 | marca | 3:1 | pasa |
| `series-5` | `panel` | 8.11:1 | marca | 3:1 | pasa |
| `missing` | `base` | 1.13:1 | mobiliario | — | exento |
| `missing` | `panel` | 1.21:1 | mobiliario | — | exento |

#### modo instrumento

| Token | Sobre | Ratio | Rol | Umbral | |
|---|---|---|---|---|---|
| `ink` | `base` | 16.28:1 | texto | 4.5:1 | pasa |
| `ink` | `panel` | 15.08:1 | texto | 4.5:1 | pasa |
| `muted` | `base` | 6.08:1 | texto | 4.5:1 | pasa |
| `muted` | `panel` | 5.63:1 | texto | 4.5:1 | pasa |
| `caption` | `base` | 4.86:1 | texto | 4.5:1 | pasa |
| `caption` | `panel` | 4.50:1 | texto | 4.5:1 | pasa |
| `border` | `base` | 1.40:1 | mobiliario | — | exento |
| `border` | `panel` | 1.30:1 | mobiliario | — | exento |
| `gridline` | `base` | 1.27:1 | mobiliario | — | exento |
| `gridline` | `panel` | 1.18:1 | mobiliario | — | exento |
| `baseline` | `base` | 1.83:1 | mobiliario | — | exento |
| `baseline` | `panel` | 1.70:1 | mobiliario | — | exento |
| `signal` | `base` | 10.30:1 | marca | 3:1 | pasa |
| `signal` | `panel` | 9.54:1 | marca | 3:1 | pasa |
| `signal-text` | `base` | 10.30:1 | texto | 4.5:1 | pasa |
| `signal-text` | `panel` | 9.54:1 | texto | 4.5:1 | pasa |
| `model` | `base` | 6.71:1 | marca | 3:1 | pasa |
| `model` | `panel` | 6.22:1 | marca | 3:1 | pasa |
| `model-text` | `base` | 6.71:1 | texto | 4.5:1 | pasa |
| `model-text` | `panel` | 6.22:1 | texto | 4.5:1 | pasa |
| `alert` | `base` | 5.67:1 | marca | 3:1 | pasa |
| `alert` | `panel` | 5.25:1 | marca | 3:1 | pasa |
| `alert-text` | `base` | 5.67:1 | texto | 4.5:1 | pasa |
| `alert-text` | `panel` | 5.25:1 | texto | 4.5:1 | pasa |
| `series-4` | `base` | 12.43:1 | marca | 3:1 | pasa |
| `series-4` | `panel` | 11.51:1 | marca | 3:1 | pasa |
| `series-5` | `base` | 4.28:1 | marca | 3:1 | pasa |
| `series-5` | `panel` | 3.96:1 | marca | 3:1 | pasa |
| `missing` | `base` | 1.17:1 | mobiliario | — | exento |
| `missing` | `panel` | 1.09:1 | mobiliario | — | exento |

Comprobados 44 pares · 0 fallos ·
8 tokens de mobiliario exentos por declaración explícita.

Los tokens con rol `mobiliario` —retícula, borde, línea base— están **deliberadamente** por debajo
de 3:1: deben quedar por debajo del dato. La exención se declara token por token en
`tokens/src/semantic.color.tokens.json` y nunca se hereda.
