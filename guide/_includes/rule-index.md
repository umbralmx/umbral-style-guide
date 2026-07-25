<!-- GENERATED from the normative layer. Do not edit. -->

69 reglas · 58 `error` ·
10 `advertencia` · 1 `guía`.

### Marca

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-BRD-001`](#umb-brd-001) | ■ | El wordmark es «umbral_» en minúsculas, Space Grotesk 500, con el guión bajo en signal | review |
| [`UMB-BRD-002`](#umb-brd-002) | ■ | La barra del isotipo guarda proporción 5:44 y cruza a la izquierda del centro | `logo-geometry` |
| [`UMB-BRD-003`](#umb-brd-003) | ▲ | El espacio de respeto es una altura de barra en los cuatro lados | review |
| [`UMB-BRD-004`](#umb-brd-004) | ■ | El logo no se distorsiona, contornea, sombrea ni recolorea fuera de los tokens | review |

### Color

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-COL-001`](#umb-col-001) | ■ | No se usa blanco ni negro puros | `pure-black-white` |
| [`UMB-COL-002`](#umb-col-002) | ■ | Ningún color se escribe a mano: todos vienen de los tokens | `hardcoded-token-hex` |
| [`UMB-COL-003`](#umb-col-003) | ■ | No se usan degradados | `no-gradient` |
| [`UMB-COL-004`](#umb-col-004) | ■ | El color signal se usa en un solo elemento de la capa de datos por vista | `signal-count` |
| [`UMB-COL-005`](#umb-col-005) | ■ | Todo texto alcanza 4.5:1 contra base y contra panel | `contrast-text` |
| [`UMB-COL-006`](#umb-col-006) | ■ | Toda marca de datos alcanza 3:1; el mobiliario de la gráfica está exento y así se declara | `contrast-mark` |
| [`UMB-COL-007`](#umb-col-007) | ■ | No se mezclan los dos modos dentro de un mismo panel | `mode-mixing` |
| [`UMB-COL-008`](#umb-col-008) | ■ | Un color categórico nuevo se deriva en OKLCH y se verifica contra dicromacia | `series-separation` |
| [`UMB-COL-009`](#umb-col-009) | ■ | Las dos rampas secuenciales no codifican dos variables en la misma figura | review |
| [`UMB-COL-010`](#umb-col-010) | ■ | Dato faltante, dato suprimido y cero se distinguen visualmente entre sí | review |

### Tipografía

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-TYP-001`](#umb-typ-001) | ■ | El display es Space Grotesk 500; nunca 700 | `display-weight` |
| [`UMB-TYP-002`](#umb-typ-002) | ■ | Solo se usan Space Grotesk, IBM Plex Sans e IBM Plex Mono | `banned-font-family` |
| [`UMB-TYP-003`](#umb-typ-003) | ■ | Se respetan los tamaños mínimos: 12px mono en web, 24px en slides, 11pt en documentos | `minimum-font-size` |
| [`UMB-TYP-004`](#umb-typ-004) | ▲ | Las cifras que se alinean o se comparan van en mono; una cifra heroica aislada va en display | review |
| [`UMB-TYP-005`](#umb-typ-005) | ■ | Las tres fuentes se auto-hospedan, subconjuntadas a latin y latin-ext | `font-hosting` |
| [`UMB-TYP-006`](#umb-typ-006) | ▲ | El tracking del display va entre −0.02 y −0.03em | `display-tracking` |

### Layout

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-LAY-001`](#umb-lay-001) | ■ | El radio de borde nunca pasa de 2px | `radius-max` |
| [`UMB-LAY-002`](#umb-lay-002) | ■ | No hay sombras; las reglas de 1px hacen el trabajo estructural | `no-drop-shadow` |
| [`UMB-LAY-003`](#umb-lay-003) | ▲ | La medida del texto no pasa de 65 caracteres | `measure-max` |
| [`UMB-LAY-004`](#umb-lay-004) | ▲ | Todo espaciado es múltiplo de 8px | `spacing-scale` |
| [`UMB-LAY-005`](#umb-lay-005) | ■ | No hay emoji, iconos de stock ni ilustración decorativa | `no-emoji` |

### Gráficas

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-CHT-001`](#umb-cht-001) | ■ | El título de la gráfica enuncia el hallazgo como oración completa | `chart-title-present` |
| [`UMB-CHT-002`](#umb-cht-002) | ■ | Toda gráfica lleva subtítulo con geografía, periodo y unidad | `chart-subtitle-present` |
| [`UMB-CHT-003`](#umb-cht-003) | ■ | Toda gráfica lleva su línea de fuente con licencia, sobre una regla de 1px | `chart-source-present` |
| [`UMB-CHT-004`](#umb-cht-004) | ■ | Solo hay líneas de retícula horizontales, con la línea base más oscura | `gridlines-horizontal` |
| [`UMB-CHT-005`](#umb-cht-005) | ■ | Las series se etiquetan directamente al final de la línea; no hay caja de leyenda | `no-legend-box` |
| [`UMB-CHT-006`](#umb-cht-006) | ▲ | Una gráfica lleva como máximo 5 series | `series-count` |
| [`UMB-CHT-007`](#umb-cht-007) | ▲ | Los ejes van en mono, abreviados, con coma como separador de miles | `axis-mono` |
| [`UMB-CHT-008`](#umb-cht-008) | ■ | El eje y de las barras empieza en cero | `bars-from-zero` |
| [`UMB-CHT-009`](#umb-cht-009) | ■ | Cualquier truncamiento del eje se anota en la propia gráfica | review |
| [`UMB-CHT-010`](#umb-cht-010) | ■ | No se usan pastel, 3D ni doble eje | `banned-chart-type` |
| [`UMB-CHT-011`](#umb-cht-011) | ■ | Toda proyección o estimación muestra su incertidumbre | review |
| [`UMB-CHT-012`](#umb-cht-012) | ■ | Toda tasa declara su denominador y su n | review |

### Voz

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-VOZ-001`](#umb-voz-001) | ■ | Español primero; el inglés se añade donde lo gane el público | review |
| [`UMB-VOZ-002`](#umb-voz-002) | ■ | Sin palabras hype, signos de exclamación, emoji ni preguntas retóricas como titular | `hype-language` |
| [`UMB-VOZ-003`](#umb-voz-003) | ▲ | Un adjetivo no sustituye a un número | review |
| [`UMB-VOZ-004`](#umb-voz-004) | ■ | No se publica contenido de relleno | `placeholder-content` |

### Números y unidades

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-NUM-001`](#umb-num-001) | ■ | es-MX y en usan coma para miles y punto para decimales | `number-separators` |
| [`UMB-NUM-002`](#umb-num-002) | ▲ | Las cifras grandes se abrevian en ejes y se escriben completas en el texto | review |
| [`UMB-NUM-003`](#umb-num-003) | ▲ | Las fechas van en ISO dentro de los datos y en prosa dentro del texto | `date-format` |
| [`UMB-NUM-004`](#umb-num-004) | · | El símbolo de porcentaje va pegado a la cifra | `percent-spacing` |
| [`UMB-NUM-005`](#umb-num-005) | ■ | La precisión declarada no excede la del dato | review |
| [`UMB-NUM-006`](#umb-num-006) | ■ | Cero, nulo y suprimido se escriben distinto y significan distinto | `null-vs-zero` |

### Datos y procedencia

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-DAT-001`](#umb-dat-001) | ■ | Todo conjunto de datos lleva su SOURCE.md | `source-md-present` |
| [`UMB-DAT-002`](#umb-dat-002) | ■ | Los snapshots se etiquetan y la gráfica dice cuál usó | `snapshot-tag` |
| [`UMB-DAT-003`](#umb-dat-003) | ■ | Toda figura publicada se reconstruye desde el dato crudo con un solo comando | manual |
| [`UMB-DAT-004`](#umb-dat-004) | ■ | El código va bajo MIT y los datos y el contenido bajo CC BY 4.0 | `license-present` |
| [`UMB-DAT-005`](#umb-dat-005) | ■ | Los datos faltantes o subreportados se declaran; no se omiten ni se imputan en silencio | review |

### Accesibilidad

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-A11Y-001`](#umb-a11y-001) | ■ | El atributo lang corresponde al idioma real del subárbol | `lang-attribute` |
| [`UMB-A11Y-002`](#umb-a11y-002) | ■ | Toda gráfica lleva un aria-label que resume el hallazgo | `chart-aria-label` |
| [`UMB-A11Y-003`](#umb-a11y-003) | ■ | Junto a cada gráfica hay una tabla de datos o un <details> con las cifras | `chart-data-table` |
| [`UMB-A11Y-004`](#umb-a11y-004) | ■ | Junto a cada gráfica se puede descargar su CSV | `chart-csv-download` |
| [`UMB-A11Y-005`](#umb-a11y-005) | ■ | El significado nunca se codifica solo con color | review |
| [`UMB-A11Y-006`](#umb-a11y-006) | ■ | El foco visible se dibuja en signal y los objetivos táctiles miden 44px o más | `focus-and-target` |
| [`UMB-A11Y-007`](#umb-a11y-007) | ■ | Se respeta prefers-reduced-motion | `reduced-motion` |

### Método

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-MET-001`](#umb-met-001) | ■ | Los verbos causales solo se usan con una estrategia de identificación nombrada | `causal-language` |
| [`UMB-MET-002`](#umb-met-002) | ■ | El titular se sostiene con los datos que la gráfica muestra | review |
| [`UMB-MET-003`](#umb-met-003) | ■ | No se comparan conteos crudos entre poblaciones de distinto tamaño | review |
| [`UMB-MET-004`](#umb-met-004) | ■ | Los temas sensibles se tratan con dignidad: se cuenta a las personas, no se les hace espectáculo | review |
| [`UMB-MET-005`](#umb-met-005) | ■ | La terminología sensible sigue el glosario, que es vinculante | `terminology` |

### Proceso

| ID | | Regla | Comprobación |
|---|---|---|---|
| [`UMB-PRO-001`](#umb-pro-001) | ■ | Los archivos generados nunca se editan a mano | `generated-file-edited` |
| [`UMB-PRO-002`](#umb-pro-002) | ■ | La prosa no enuncia ninguna regla que rules.yaml no enuncie también | `prose-rule-drift` |
| [`UMB-PRO-003`](#umb-pro-003) | ■ | Ningún archivo fuera de tokens/src/ escribe un valor que ya existe como token | `hardcoded-value` |
| [`UMB-PRO-004`](#umb-pro-004) | ■ | Cambiar el valor de un token es un cambio MAYOR de versión | manual |
| [`UMB-PRO-005`](#umb-pro-005) | ■ | El capítulo de la guía y la entrada de la regla se actualizan juntos | review |
