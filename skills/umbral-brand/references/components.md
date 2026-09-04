<!-- references/components.md — GENERATED from the normative layer of
     umbralmx/umbral-style-guide v1.6.0. Do not edit; regenerate. -->

# Components

The shadcn/ui catalogue mapped against the rules. The normative text is
`guide/16-componentes.md`; this is its index.

shadcn/ui is copied code, not a dependency. Take the **form** and the accessibility contract. Never
take the values — a shadcn component writes its colours and radii into Tailwind classes, which is
UMB-COL-002 and UMB-PRO-003 by construction.

## The five systematic corrections

They apply to every component. Apply them before reading any entry below.

| | shadcn ships | Umbral applies | Rule |
|---|---|---|---|
| 1 | `rounded-md`, `rounded-xl`, `rounded-full` | 2px radius ceiling; a pill is banned outright | UMB-LAY-001 |
| 2 | `shadow-xs`, `shadow-sm` | No shadows; 1px rules carry the structure | UMB-LAY-002 |
| 3 | Control heights `h-7` to `h-10` | 44px touch target minimum | UMB-A11Y-006 |
| 4 | Tailwind palette and its own variables | Every colour from the tokens | UMB-COL-002 |
| 5 | `font-semibold` headings | Space Grotesk 500; 600 is for small labels only | UMB-TYP-001 |

No default shadcn control height reaches 44px. The touch target may exceed the visible border, so
the fix does not force a fatter control.

## Overlays

`dialog`, `alert-dialog`, `sheet`, `drawer`, `popover` and `command` share one contract
(UMB-A11Y-008): focus enters on open, is trapped while open, Escape closes, and focus returns to
the control that opened it. Radix supplies this in React. It has to be written by hand elsewhere.

## Reject (3)

| Component | Instead |
|---|---|
| `switch` | `rounded-full` es una píldora. Usa el control segmentado o una casilla. |
| `chart` | Umbral grafica con `@umbralmx/umbral-plot`. Doce reglas UMB-CHT lo gobiernan. |
| `carousel` | Esconde contenido detrás de movimiento. Pon las piezas una junto a otra. |

## Adapt (20)

| Component | The specific change |
|---|---|
| `navigation-menu` | Una portada no lleva barra de navegación. Ver `14-superficies/landing.md`. |
| `scroll-area` | Prefiere el scroll nativo. Una barra propia rompe el comportamiento del sistema. |
| `tabs` | Toma la forma del control segmentado (UMB-LAY-008), no la pestaña con relleno. |
| `card` | Radio y sombra fuera. Una **lista** no se hace con tarjetas (UMB-LAY-007). Ver OQ-010. |
| `hover-card` | El hover no existe en táctil. El mismo contenido abre con foco. |
| `tooltip` | Nunca es el único portador de un significado (UMB-A11Y-005). Abre con foco. |
| `empty` | Declara **cuál** vacío es: sin registro, suprimido o cero medido (UMB-COL-010, UMB-NUM-006). |
| `button` | Rectángulo de 1px sin relleno para el secundario (UMB-LAY-008). Radio, sombra y altura fuera. |
| `toggle` | El estado activo mueve borde y texto a `signal` (UMB-LAY-008). |
| `input` | Radio, sombra y altura fuera. El borde es de 1px en `border`. |
| `slider` | Lleva su valor en cifra, en mono. El pulgar alcanza 44px. |
| `alert` | La severidad se nombra con palabras. `alert` solo marca advertencia (UMB-COL-004). |
| `badge` | `rounded-full` fuera. Rectángulo de 1px en mono minúsculas. |
| `progress` | Lleva su porcentaje en cifra. El símbolo va pegado al número (UMB-NUM-004). |
| `skeleton` | Respeta `prefers-reduced-motion` (UMB-A11Y-007). No imita la forma del dato que falta. |
| `spinner` | Respeta `prefers-reduced-motion`. |
| `sonner` | Confirma una acción. Nunca lleva un hallazgo ni una cifra. Ver OQ-011. |
| `toast` | Igual que `sonner`. |
| `avatar` | Nunca para una persona de un conjunto de datos (UMB-MET-004). Equipo y autoría, sí. |
| `typography` | Umbral tiene su propia escala. Ver [03 · Tipografía](03-tipografia.md). |

## Adopt (37)

Form is fine. Apply the five corrections and nothing else.

| Component | Note |
|---|---|
| `accordion` | Patrón de divulgación. El encabezado es un `button`, no un `div`. |
| `breadcrumb` | El elemento actual lleva `aria-current="page"`. |
| `collapsible` | — |
| `menubar` | — |
| `pagination` | Los números van en mono (UMB-TYP-004). |
| `resizable` | El separador alcanza 44px de área táctil. |
| `separator` | Es la regla de 1px. El componente más umbral del catálogo. |
| `sidebar` | — |
| `direction` | Utilidad de dirección. Ver también `lang` (UMB-A11Y-001). |
| `item` | Es la fila separada por regla de 1px. La forma que UMB-LAY-007 pide. |
| `aspect-ratio` | Utilidad de layout, sin superficie visual. |
| `sheet` | Capa superpuesta: UMB-A11Y-008. |
| `drawer` | Capa superpuesta: UMB-A11Y-008. |
| `dialog` | Capa superpuesta: UMB-A11Y-008. |
| `alert-dialog` | Capa superpuesta. La acción destructiva se nombra en el botón, no solo en color. |
| `popover` | Capa superpuesta: UMB-A11Y-008. |
| `button-group` | — |
| `toggle-group` | Es el control segmentado. Forma canónica de UMB-LAY-008. |
| `checkbox` | Área táctil de 44px. El radio baja a 0. |
| `radio-group` | Área táctil de 44px. |
| `input-group` | — |
| `input-otp` | Las casillas van en mono (UMB-TYP-004). |
| `native-select` | Preferido sobre `select`. El control nativo ya trae su accesibilidad. |
| `select` | Úsalo solo cuando `native-select` no alcance. |
| `combobox` | — |
| `command` | Capa superpuesta: UMB-A11Y-008. |
| `context-menu` | Toda acción del menú tiene otra ruta. El clic derecho no se descubre solo. |
| `dropdown-menu` | Capa superpuesta: UMB-A11Y-008. |
| `textarea` | El ancho se acota con la medida de UMB-LAY-003. |
| `label` | Todo campo lleva etiqueta visible. El `placeholder` no es una etiqueta. |
| `field` | — |
| `form` | El error se nombra con palabras, no solo con color (UMB-A11Y-005). |
| `calendar` | Las fechas van en ISO dentro del dato (UMB-NUM-003). |
| `date-picker` | Composición de `calendar` y `popover`. |
| `kbd` | Mono, por definición. |
| `table` | Ya especificado en [04 · Layout](04-layout.md) § Tablas de datos. |
| `data-table` | Composición sobre `table`. Las cifras en mono, alineadas a la derecha. |

## Out of scope (6)

`attachment` · `bubble` · `message` · `message-scroller` · `questionnaire` · `marker`

The catalogue's chat pieces. Umbral does not publish a conversational product.

## Open

OQ-011 asks what a transient message may carry. OQ-012 asks how a disabled control meets the 4.5:1
floor, which UMB-COL-005 states without an exception.
