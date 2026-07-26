# `site/data/raw/`

**Immutable.** As downloaded, never edited. Every directory under a `data/raw/` carries a
`SOURCE.md` with origin, accessor, download date, licence and known caveats (UMB-DAT-001) — see
[`SOURCE.md`](SOURCE.md).

| | |
|---|---|
| `cabildo-actas.csv` | 7,019 agenda points, Ayuntamiento de Colima, 2012–2026, snapshot `cabildo-2026-07` |

Processed output goes to `../sesiones-por-anio.csv`, regenerated from this file by
`build/site.mjs`. Nothing downstream reads this file directly.
