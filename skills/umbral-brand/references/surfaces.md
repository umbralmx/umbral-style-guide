<!-- references/surfaces.md — GENERATED from the normative layer of
     umbralmx/umbral-style-guide v1.5.0. Do not edit; regenerate. -->

# Surfaces

| Surface | Mode | The thing that bites |
|---|---|---|
| Web | laboratorio | Self-host fonts; never a CDN |
| Observable Framework | instrumento | `style`, never `theme`; `<html>` ships with no `lang` at all |
| Streamlit | instrumento | `primaryColor` hits every widget; `lang="en"` is hardcoded (superseded) |
| Quarto | laboratorio | Use the generated `_brand.yml`; `fig-alt` carries the finding |
| Notebook | laboratorio | Use the generated `.mplstyle`; the v1.0 one failed contrast |
| Social | instrumento | The card travels without its page — the source line is mandatory |
| Slides | laboratorio | Nothing below 24px, ever |
| GitHub | — | No emoji, no decorative badges, both licence files |
| Email | laboratorio | No CSS variables; inline values copied from the build |

## Observable Framework — the dashboard surface

Framework replaced Streamlit as the dashboard surface in 1.4 (ADR-0004). It is the `web` surface,
not a reduced one: UMB-LAY-003, UMB-LAY-009 and UMB-LAY-010 all apply again.

```js
// observablehq.config.js
export default {
  style: "observable-framework-instrumento.css",   // copied from assets/
  globalStylesheets: [],                            // its default is Google Fonts
  head: '<script>document.documentElement.lang="es"</script>',
};
```

```bash
cp assets/observable-framework-instrumento.css src/
```

**Ship `style`, never `theme`.** Framework's own themes derive muted, faint, fainter and faintest
with `color-mix()` from one foreground. A derived colour never reaches `contrast.json`, so the
gate cannot measure it (UMB-COL-012). The generated stylesheet declares all nine `--theme-*`
properties from the tokens instead.

**One file per mode.** `theme: "dashboard"` resolves to `air` and `near-midnight` under
`prefers-color-scheme`, which hands the mode to the reader's operating system. The medium sets the
mode (UMB-COL-011). Two stylesheets ship; import exactly one.

**`<html>` has no `lang` attribute at all.** Not a wrong value — an absent one, which is the worse
case of UMB-A11Y-001. Framework does not expose the tag, so the shim goes in `head`.

**Charts need no new work.** Framework renders Observable Plot natively, so `@umbralmx/umbral-plot`
applies unchanged: `theme()`, `Frame`, `band()`, `label()`.

**Cards.** Framework's dashboard vocabulary is `.card` inside `.grid`. The generated stylesheet
fixes the 12px radius. It does not make a card the right container for a *list* — that stays rows
separated by 1px rules (UMB-LAY-007).

## Streamlit — the two traps

Streamlit is superseded but still live in `desaparecidosmx` and `pautamx` until both migrate.

**1. The config keys.** v1.0's brand book rendered them as `sc-camel-primary-color`, a PDF-export
artifact. It also set `font = "sans serif"`, which is a *valid* Streamlit value meaning Streamlit's
own Source Sans. Copy the generated file instead:

```bash
cp assets/streamlit-config.toml .streamlit/config.toml
```

**2. `lang="en"`.** Streamlit hardcodes it. One call, at the top of the app:

```python
import streamlit.components.v1 as components
components.html("<script>window.parent.document.documentElement.lang='es';</script>", height=0)
```

**On `signal` in Streamlit:** `primaryColor` is applied to sliders, chips, tabs, links and focus
rings simultaneously. No configuration restricts it to one element. So UMB-COL-004 is scoped to the
data layer — in a dashboard it means *one series in signal per chart*. Widget chrome is exempt.

## Rule counts by surface

| Surface | Rules |
|---|---|
| `web` | 74 |
| `framework` | 74 |
| `quarto` | 73 |
| `streamlit` | 71 |
| `slides` | 63 |
| `notebook` | 61 |
| `social` | 58 |
| `print` | 54 |
| `email` | 31 |
| `github` | 20 |
| `repo` | 14 |
