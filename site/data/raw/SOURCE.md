# Actas de cabildo — Ayuntamiento de Colima

- **Origen:** https://www.colima.gob.mx/portal2016/actas-de-cabildo/
- **Vía:** https://umbralmx.github.io/cabildo-libre/actas.csv — proyecto Umbral, estructura CC BY 4.0
- **Institución:** Ayuntamiento de Colima
- **Descargado por:** equipo umbral-style-guide
- **Fecha de descarga:** 2026-07-26
- **Snapshot:** `cabildo-2026-07`
- **Licencia:** contenido del Ayuntamiento de Colima; la estructura y extracción, CC BY 4.0
- **Método:** el índice HTML oficial publica el órden del día de cada sesión como texto; un script
  de `cabildo-libre` lo convierte en registros estructurados.

## Qué contiene

7,019 puntos de órden del día, uno por renglón, de 2012 a 2026.
Columnas: `id_sesion, fecha, no_acta, periodo, punto_n, punto_numeral, punto_texto, pdf_url`.

## Limitaciones conocidas

Declaradas, no imputadas (UMB-DAT-005):

- **27 sesiones** cuyo órden del día no aparece en el índice oficial.
- **Una sesión sin fecha publicada**, excluida de cualquier serie temporal.
- **Enlaces PDF de 2013–2014** que el servidor del ayuntamiento ya no resuelve.
- **2012 y 2026 son años parciales.** El índice empieza a mitad de 2012 y 2026 no ha terminado.
  Cualquier gráfica anual tiene que marcarlos como provisionales, o la caída en los extremos se
  lee como un desplome real.

## Para qué se usa aquí

Solo para la página de demostración `site/demo/grafica.qmd`, que reconstruye
`site/data/sesiones-por-anio.csv` desde este archivo en cada build (UMB-DAT-003).
No es un producto de datos de Umbral: es el dato real más cercano y públicamente descargable con el
que demostrar el sistema.
