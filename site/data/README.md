# `site/data/`

Data for the site's demonstration chart.

| | |
|---|---|
| `raw/` | **Immutable, as downloaded**, with its `SOURCE.md` (UMB-DAT-001) |
| `sesiones-por-anio.csv` | **Generated** by `build/site.mjs` from `raw/` on every build |

That split is the point. The published figure rebuilds from raw with one command, which is the
criterion the guide sets for anything it publishes (UMB-DAT-003). A figure that could not be rebuilt
would not ship, including on the site that teaches the rule.

The dataset is [Actas Abiertas — Cabildo de Colima](https://umbralmx.github.io/cabildo-libre/), a
real Umbral product. It has four known gaps: 27 missing agenda listings, one undated session, dead
PDF links from 2013–2014, and two partial years. All four are declared in `raw/SOURCE.md` and
surfaced in the chart's subtitle, not smoothed away.
