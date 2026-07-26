# `docs/adr/`

Architecture Decision Records — decisions that are expensive to reverse, with the reasoning that
produced them and the alternatives that were rejected.

| | | Status |
|---|---|---|
| [0001](0001-token-architecture.md) | Token architecture | accepted |
| 0002 | Site generator (Quarto or Astro) | *Phase 7* |
| [0003](0003-downstream-consumption.md) | How downstream repos consume the system | accepted |

An ADR is written when the decision is made, not afterwards, and it isn't edited once accepted — if
a decision changes, a new ADR supersedes it.

Smaller decisions about the *design system* (as opposed to its architecture) go in
[`audit/open-questions.md`](../../audit/open-questions.md) instead. The line: an ADR is about how
the repo is built, an open question is about what the brand says.
