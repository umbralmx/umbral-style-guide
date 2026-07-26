# ADR-0002 — Site generator

- **Status:** accepted
- **Date:** 2026-07-26
- **Phase:** 7

## Context

KICKOFF §8 asks for Quarto "if it can carry the interaction we need … otherwise Astro", and requires
the site be a **demonstration** of the system rather than a description: every swatch, specimen,
ratio and example chart generated from `tokens/build/`, with at least one page rendering a real
chart from a real Umbral dataset with a live mode toggle.

The guide is 23 Markdown chapters that already use Quarto include shortcodes, and Jay works in
Quarto daily.

## Decision

**Quarto**, with the site generated into `site/` by `build/site.mjs`.

The site directory is **generated, not authored**. `build/site.mjs` copies `guide/*.md` to
`site/guide/*.qmd`, copies the rule callouts, and generates `_quarto.yml`, `styles.css`, the demo
pages and the index. `guide/` stays the single source for prose.

Three things settled it:

1. **The includes already work.** Guide chapters carry `{{< include _includes/rules/UMB-*.md >}}`,
   which is Quarto's own shortcode. Astro would have needed a second mechanism for the same job,
   and the whole point of those includes is that prose cannot drift from `rules.yaml`.
2. **The site can be its own reproducibility demo.** `build/site.mjs` rebuilds the demo dataset
   from `site/data/raw/` on every build, so the chart on the site satisfies UMB-DAT-003 the same
   way a published figure must.
3. **No JS framework is needed for the interaction we actually want.** The mode toggle is a button
   that flips `data-mode` and redraws an SVG from `tokens.json`. That is ~40 lines of vanilla
   module script. Astro's advantage — component islands — buys nothing here.

## Consequences

**Good**

- One toolchain for the guide, the site, and Jay's own reports.
- `theme: none` plus the generated `styles.css` means the site is styled *only* by the tokens.
  There is no Bootstrap to fight and no hand-written colour anywhere in `site/`.
- The demo pages are generated, so a token change re-renders the swatches, the contrast matrix and
  the correct-vs-incorrect gallery without anyone touching them.

**Costs**

- Quarto is a system dependency for building the site, on top of Node and Python. It is not needed
  to consume the design system — only to publish the guide.
- `site/` is generated *and* committed output, like `tokens/build/`. CI rebuilds and diffs it.
- Quarto's include filter renumbers lines, so Pandoc emits a spurious "Div … unclosed" warning on
  chapters with many rule callouts. The rendered HTML is correct — verified by checking that each
  callout div opens, contains its do/don't table, and closes. Recorded here so nobody chases it.

**Two things Quarto made us fix, which are wins**

- Rule callouts originally used raw `<div>` wrapping a Markdown table. Pandoc mis-nests that, and
  it silently dropped a table. They now use fenced-div syntax (`::: {.u-rule …}`), which is
  unambiguous.
- Constraining `main` alone left the measure unbounded, so the guide's own site violated
  UMB-LAY-003. The generated CSS now constrains Quarto's content column, with wide elements
  opting back out.

## Alternatives considered

**Astro.** Better for a genuinely interactive chart chooser, and a nicer component model. Rejected
because it adds a second templating system for content that is already Markdown with Quarto
shortcodes, and because the interaction we need is one toggle.

**Publishing `guide/` directly with GitHub's Markdown rendering.** Zero build. Rejected: it cannot
generate swatches from tokens, so the guide would describe the system instead of demonstrating it —
which is the failure mode the whole repo exists to correct.
