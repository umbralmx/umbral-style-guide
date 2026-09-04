# ADR-0004 — Observable Framework replaces Streamlit as the dashboard surface

- **Status:** accepted
- **Date:** 2026-09-03
- **Phase:** 9
- **Supersedes:** Streamlit, which was never a recorded decision

## Context

Two Umbral products are live dashboards. `desaparecidosmx` and `pautamx` both run on Streamlit.

Streamlit arrived with v1.0. No ADR records the choice. The lab inherited it rather than decided
it.

The Phase 0 audit measured what the inheritance costs. Three findings stand out.

`primaryColor` paints every widget accent at once. Streamlit exposes no setting that restricts it.
OQ-002 therefore scoped UMB-COL-004 to the data layer.

Streamlit hardcodes `lang="en"` and does not expose it. OQ-004 accepted a JavaScript shim as the
fix.

`pautamx` still renders Source Sans. The v1.0 brand book set `font = "sans serif"`, which is a
valid Streamlit value naming Streamlit's own face.

Each finding is a limit of the platform. None is a design decision. The design system has spent a
year absorbing constraints it did not choose.

Observable Framework is a static site generator for data apps. Pages are Markdown. Data loaders run
at build time. Charts are Observable Plot.

## Decision

**Observable Framework becomes the dashboard surface.** The rule set registers it as `framework`.
It inherits the `web` rules, not the `streamlit` ones.

Three things settled it.

**1. The chart layer already exists.** `packages/umbral-plot` targets Observable Plot. Framework
renders Observable Plot natively. The theme, the `Frame`, the ramps and the uncertainty helpers
transfer unchanged. The most expensive half of the system needs no work at all.

**2. Framework returns the CSS control that Streamlit withheld.** The `streamlit` rule set is a
strict subset of `web`. Three rules were excused: UMB-LAY-003, UMB-LAY-009 and UMB-LAY-010. All
three apply again. The guide stops making exceptions for a platform.

**3. A dashboard becomes reproducible.** Framework builds static pages from data loaders. The
loader *is* the rebuild command. UMB-DAT-003 becomes checkable on a dashboard for the first time.

### What the decision adds to the normative layer

Framework's defaults are not neutral. Nine of them collide with the guide.
`guide/14-superficies/framework.md` lists all nine beside their fixes.

Two collisions changed the rules rather than the chapter.

`theme: "dashboard"` resolves to `air` and `near-midnight`. Framework wraps each import in a
`prefers-color-scheme` query. The reader's operating system then picks the mode. Umbral picks the
mode by medium. No rule said so, because no platform had ever offered to decide it for us.
**UMB-COL-011** now says it.

`abstract-light.css` derives `muted`, `faint`, `fainter` and `faintest` with `color-mix()`. Those
derived values never reach `tokens/build/contrast.json`. The contrast gate cannot measure a colour
it never sees. UMB-COL-002 forbids a hand-written hex, and a formula is not a hex.
**UMB-COL-012** closes the gap.

Both rules ship at `warning`. That follows the precedent set by UMB-LAY-006 through UMB-LAY-010.

## Consequences

**Good**

- One generated stylesheet carries the whole surface. `tokens/build/observable-framework.css`
  declares the nine `--theme-*` properties and the three font stacks for both modes. A dashboard
  sets `style:` and inherits every token value.
- The dashboards join the reproducibility chain. A data loader reads `SOURCE.md`-documented raw
  data and writes the file the page loads. `npm run build` rebuilds the figure from raw.
- The `signal` carve-out narrows. Under Framework we control which chrome takes the accent, so
  UMB-COL-004 can bind more of the page than it could under Streamlit.
- The `lang` defect becomes visible. Framework emits `<html>` with no `lang` attribute at all.
  UMB-A11Y-001 told authors not to leave the framework's `lang="en"`. That sentence assumed an
  attribute exists. The rule now covers the absent case, which is the worse one.

**Costs**

- Two products need porting. That work lives in their repos, not here.
- Streamlit does not vanish on the day of the decision. The `streamlit` surface stays in the rule
  set until both products migrate. Two dashboard surfaces coexist for one release cycle at least.
- Every dashboard repo gains a Node toolchain. Streamlit needed only Python.
- The execution model changes. Streamlit re-runs Python for each interaction. Framework precomputes
  at build time and filters on the client. `desaparecidosmx` holds 351,057 records, so its
  filtering needs DuckDB or a narrower extract. This is the real engineering cost of the move.

## Alternatives considered

**Stay on Streamlit.** Zero migration cost. Rejected because three audit findings are Streamlit
limits, and no amount of care inside Streamlit fixes any of them.

**Quarto dashboards.** Quarto is already a dependency, and `format: dashboard` exists. Rejected on
interactivity. Client-side filtering needs Shiny or OJS. Shiny adds a server the lab does not want
to run. OJS means Observable Plot inside Quarto, which is Framework with weaker data loaders.
Quarto's dashboard layout is also card-first, so it collides with UMB-LAY-007 exactly as Framework
does, while giving back less CSS control.

**Astro, or a hand-rolled site.** Total control over every default listed above. Rejected because
the lab would then own the dashboard layer itself. Framework's nine bad defaults are cheaper to
override than a dashboard framework is to maintain.
