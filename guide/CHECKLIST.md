<!-- GENERATED from rules/rules.yaml. Do not edit. -->

# Checklist de entrega

Umbral v1.1.0

Esta hoja **no** repite las 41 reglas que CI ya comprueba sola — si alguna falla, el
release se bloquea sin que nadie tenga que acordarse. Aquí están las que exigen
criterio humano, que son las que se pierden.

Antes de publicar, verificar estas **17**:

### Marca

- [ ] **UMB-BRD-001** — El wordmark es «umbral_» en minúsculas, Space Grotesk 500, con el guión bajo en signal
- [ ] **UMB-BRD-004** — El logo no se distorsiona, contornea, sombrea ni recolorea fuera de los tokens

### Color

- [ ] **UMB-COL-009** — Las dos rampas secuenciales no codifican dos variables en la misma figura
- [ ] **UMB-COL-010** — Dato faltante, dato suprimido y cero se distinguen visualmente entre sí

### Gráficas

- [ ] **UMB-CHT-009** — Cualquier truncamiento del eje se anota en la propia gráfica
- [ ] **UMB-CHT-011** — Toda proyección o estimación muestra su incertidumbre
- [ ] **UMB-CHT-012** — Toda tasa declara su denominador y su n

### Voz

- [ ] **UMB-VOZ-001** — Español primero; el inglés se añade donde lo gane el público

### Números y unidades

- [ ] **UMB-NUM-005** — La precisión declarada no excede la del dato

### Datos y procedencia

- [ ] **UMB-DAT-003** — Toda figura publicada se reconstruye desde el dato crudo con un solo comando
- [ ] **UMB-DAT-005** — Los datos faltantes o subreportados se declaran; no se omiten ni se imputan en silencio

### Accesibilidad

- [ ] **UMB-A11Y-005** — El significado nunca se codifica solo con color

### Método

- [ ] **UMB-MET-002** — El titular se sostiene con los datos que la gráfica muestra
- [ ] **UMB-MET-003** — No se comparan conteos crudos entre poblaciones de distinto tamaño
- [ ] **UMB-MET-004** — Los temas sensibles se tratan con dignidad: se cuenta a las personas, no se les hace espectáculo

### Proceso

- [ ] **UMB-PRO-004** — Cambiar el valor de un token es un cambio MAYOR de versión
- [ ] **UMB-PRO-005** — El capítulo de la guía y la entrada de la regla se actualizan juntos

---

## Lo que comprueba la máquina

```
npm run build      # tokens + reglas; falla si un token no alcanza su umbral
npm run verify     # re-deriva contraste y reglas de forma independiente
umbral-lint .      # las comprobaciones automáticas sobre este repo
```

41 reglas `error` automáticas · 10 advertencias · 1 de guía. Todas en `rules/rules.yaml`.

`■ error` bloquea el release · `▲ advertencia` se reporta y se justifica · `· guía` orienta.
