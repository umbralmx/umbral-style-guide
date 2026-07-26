# `site/data/`

Data for the site's demonstration chart.

| | |
|---|---|
| `raw/` | **Immutable, as downloaded**, with its `SOURCE.md` (UMB-DAT-001) |
| `sesiones-por-anio.csv` | **Generated** by `build/site.mjs` from `raw/` on every build |

That split is the point: the published figure rebuilds from raw with one command, which is the
criterion the guide sets for anything it publishes (UMB-DAT-003). If it could not be rebuilt, it
would not ship — including on the site that teaches the rule.

The dataset is [Actas Abiertas — Cabildo de Colima](https://umbralmx.github.io/cabildo-libre/),
a real Umbral product. Its known gaps — 27 missing agenda listings, one undated session, dead PDF
links from 2013–2014, and two partial years — are declared in `raw/SOURCE.md` and surfaced in the
chart's subtitle rather than smoothed away.
