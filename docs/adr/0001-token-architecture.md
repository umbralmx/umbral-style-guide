# ADR-0001 — Token architecture

- **Status:** accepted
- **Date:** 2026-07-25
- **Phase:** 1
- **Supersedes:** the `assets/tokens.css` + `assets/tokens.json` pair shipped in v1.0

## Context

v1.0 kept colour in two hand-maintained files, `tokens.css` and `tokens.json`, and expected every
other artifact to copy values out of them. The Phase 0 audit measured what that produced:

- The brand book documented **7 of the 11** colour tokens. `caption` — the worst-failing token and
  the most-used small-text colour across all four products — appeared in neither document.
- The mplstyle in `umbral-engineering.md` and the Plotly snippet in the brand book **disagreed about
  the third series colour**, and the version that won in Python tooling used a token at 2.37:1.
- `umbral-engineering.md` asserted both modes met WCAG AA. Four token pairs did not, and three more
  failed that the kickoff had not identified.

None of these were implementation mistakes. They were the predictable result of a value being
stated in more than one place with nothing checking that the statements agreed.

We need a token layer that (a) makes a value impossible to state twice, (b) reaches eleven
heterogeneous targets including matplotlib, R and Quarto, and (c) fails CI rather than review when
a colour stops meeting its accessibility obligation.

## Decision

**Author W3C DTCG token files in `tokens/src/`; generate everything else into `tokens/build/`; gate
on a generated contrast matrix; verify the generator with an independent implementation.**

Four parts:

### 1. DTCG source, primitives → semantic

`tokens/src/` holds the only authored values. Primitives (`color.teal.600`) carry raw hex plus the
OKLCH coordinates they were derived at; semantic tokens (`semantic.laboratorio.signal`) are
references, never literals. `verify_tokens.py` fails if any hex is authored twice, which is what
mechanically prevents the v1.0 failure mode.

### 2. Style Dictionary v4 as the transformer

Chosen per KICKOFF §9. It parses DTCG natively, resolves references, and its custom-format API
carries the eleven targets. Node is required by Phase 6 (`umbral-plot`) and Phase 7 (the site)
regardless, so this adds no new toolchain.

### 3. `contrastRole` on every token, and a role-aware gate

Recorded in full as OQ-001. A literal "fail any pair below threshold" gate fails permanently and
correctly on gridlines, which are meant to sit below the data — so it would have been switched off
within a week, taking the real checks with it. Instead every token declares one of:

| Role | Gate |
|---|---|
| `text` | 4.5:1 against both `base` and `panel` |
| `mark` | 3:1 against both |
| `furniture` | exempt, with a written `exemptRationale` |
| `surface` | measured against, not measured |

The exemption is authored per token and never inherited, so a new token cannot acquire it silently.

### 4. Two independent implementations of the colour maths

`build/lib/color.mjs` computes contrast and expands ramps in JS. `tools/verify_tokens.py`
re-derives the same numbers in Python **from the generated files** and fails on disagreement. Both
run in CI.

This is deliberate duplication, which is normally a smell. It is justified here because the whole
system's credibility rests on these numbers being right, and the failure being corrected is
precisely a case of an unverified claim ("both modes meet AA") going unchallenged for a year. A
mistake now has to be made twice, in two languages, to reach the published system.

## Consequences

**Good**

- A colour cannot be stated twice; CI proves it.
- The four v1.0 contrast failures, plus three more found in Phase 0, are fixed at the token layer —
  no product markup changes to adopt them.
- `caption` and `muted` are documented, having been absent from the brand book entirely.
- Ramps are authored as *derivation specs*, not frozen hex lists, so they can be re-derived if a
  background changes rather than being untouchable.
- The `signal` / `signal-text` split resolves a genuine role conflict: `signal` clears the 3:1 a
  mark needs but not the 4.5:1 text needs, and the brand mandates direct series labels — which makes
  series colours into small text.

**Costs**

- `tokens/build/` is generated *and* committed. Downstream repos can fetch a raw URL without a build
  step, but a stale commit is now possible; CI rebuilds and diffs to catch it.
- Two toolchains (Node + Python) are needed to validate a change, though only Node to build.
- The colour maths exists twice and both copies must be maintained together.

**Deferred**

- `signal-text` in `modo instrumento` aliases `signal`, because dark-mode `signal` already clears
  4.5:1. If dark `base` ever lightens, that alias must be re-derived, not assumed.
- The sequential ramps anchored on `signal` and `model` are indistinguishable under tritanopia
  (OQ-005). They ship with a binding rule against using both in one figure rather than a technical
  fix, because no technical fix exists at these two hues.

## Alternatives considered

**A single Python build, no Node.** Would have put the colour maths in one language and removed a
toolchain from the normative path. Rejected because KICKOFF §9 specifies Style Dictionary, Node is
required by later phases anyway, and the cross-language check turns the duplication into a feature.

**Generate `tokens/build/` at install time instead of committing it.** Cleaner, but it forces every
downstream repo — including notebooks and Quarto documents — to run a Node build to get a hex.
Rejected as hostile to the actual consumers.

**Keep one `signal` token and relax the text requirement to 3:1.** Rejected: it would have meant
asserting that 4.22:1 body text is acceptable for a public-interest lab, which is the exact claim
Phase 0 disproved.
