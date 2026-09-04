# `docs/adr/`

Architecture Decision Records — decisions that are expensive to reverse, with the reasoning that
produced them and the alternatives that were rejected.

| | | Status |
|---|---|---|
| [0001](0001-token-architecture.md) | Token architecture | accepted |
| [0002](0002-site-generator.md) | Site generator | accepted |
| [0003](0003-downstream-consumption.md) | How downstream repos consume the system | accepted |
| [0004](0004-dashboard-surface.md) | Observable Framework as the dashboard surface | accepted |

An ADR is written when the decision is made, not afterwards. It is not edited once accepted. If a
decision changes, a new ADR supersedes it.

Smaller decisions about the *design system*, rather than its architecture, go in
[`audit/open-questions.md`](../../audit/open-questions.md) instead. The line is simple. An ADR is
about how the repo is built. An open question is about what the brand says.
