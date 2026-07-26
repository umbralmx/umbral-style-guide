# `assets/`

Binary and near-binary brand assets. Distinct from `_inbox/`, which holds the superseded v1.0
material.

| | |
|---|---|
| `logo/` | **Generated** by `build/logo.mjs` from one parametric spec |
| `fonts/` | Self-hosted Space Grotesk and IBM Plex subsets, with their OFL licences *(pending)* |
| `templates/` | Social 1080², slide 1920×1080, chart frame *(pending)* |

## Fonts are not here yet

`UMB-TYP-005` requires the three families to be self-hosted and subset to `latin` + `latin-ext`,
and the audit confirmed `umbralmx.github.io` still loads them from Google's CDN. Vendoring the
`.woff2` files is outstanding — tracked for the release phase, since it means committing binaries
and their licence files.

Until then, `cabildo-libre/assets/fonts.css` is the working reference implementation: correctly
subset, with `unicode-range`, and self-hosted.
