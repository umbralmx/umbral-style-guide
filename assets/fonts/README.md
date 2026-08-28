# `assets/fonts/`

Self-hosted font subsets (UMB-TYP-005). `fonts.css` is **generated** by `build/fonts.mjs`; the
`.woff2` files and the OFL licences are vendored.

| | Weights | Files |
|---|---|---|
| Space Grotesk | 500–600 | variable — one file per subset |
| IBM Plex Sans | 400–600 | variable — one file per subset |
| IBM Plex Mono | 400, 500 | static — one file per weight per subset |

8 files, ~142KB, subset to `latin` + `latin-ext`. `latin-ext` is the one carrying Spanish
diacritics beyond Latin-1, so it is not optional here.

## Why self-host

A public-interest data product has to work offline and inside government networks. A CDN also leaks
every reader's IP to a third party.

The v1.0 engineering doc asked for self-hosting in prose. It shipped a Google Fonts `<link>` in the
code block of the same section. The main site copied the code block, and `umbral-lint` still flags
it.

## Variable vs static

Space Grotesk and IBM Plex Sans are variable fonts. They carry an `fvar` axis, so **one file
legitimately serves every weight in its range**. `fonts.css` declares a weight range instead of
discrete weights.

IBM Plex Mono is still distributed as static instances, so it gets one file per weight.

Worth knowing, because three same-sized files for 400/500/600 looks like a packaging bug and is not.

## Licences

Both families are SIL OFL. `OFL-IBM-Plex.txt` and `OFL-Space-Grotesk.txt` ship alongside, as the
licence requires — `build/fonts.mjs` fails the build if either is missing.

## A limitation

matplotlib cannot read `.woff2`. It needs TTF or OTF. Notebooks fall back to a default face unless
the families are installed system-wide.

A proper fix means vendoring TTFs too, which roughly doubles the asset weight. Flagged, not done.
