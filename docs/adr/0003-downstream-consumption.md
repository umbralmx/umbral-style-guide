# ADR-0003 — How downstream repos consume the system

- **Status:** accepted
- **Date:** 2026-07-26
- **Phase:** 4
- **Supersedes:** copy-paste, which is what v1.0 actually did

## Context

Four Umbral products consume the design system. In v1.0 they consumed it by **copying files**:
`tokens.css` was duplicated into each repo, and the chart themes were pasted out of a PDF and a
markdown file.

The Phase 0 audit measured what that produced. The two static products happened to hold identical
copies of `tokens.css` — but only because nobody had edited either since. Meanwhile the *sources*
had already diverged: the brand book and `umbral-engineering.md` disagreed about the third series
colour, and the mplstyle in the engineering doc used a token at 2.37:1 for axis labels.

There is a second, less obvious consumer: **an agent**. Claude Code working in
`desaparecidosmx` needs the same values, and a v1.0 skill was already installed globally at
`~/.claude/skills/umbral-brand/` carrying its own frozen copy of the old tokens. It had been
handing out failing colours for as long as it had existed.

So the question is not just "how does a repo get a hex" but "how does anything — human, build tool,
or agent — get a value, and how does it find out when that value changes".

## Decision

**Three consumption paths, all pinned to a version tag, none of them requiring a build step.**

### 1. Machines — raw URLs at a tag

```
https://raw.githubusercontent.com/umbralmx/umbral-style-guide/v1.1.0/tokens/build/tokens.css
```

`tokens/build/` is generated *and committed* precisely so this works. A notebook, a Quarto document
or a `<link>` tag can fetch a value without Node, npm, or a build.

**Always a tag, never `main`.** A token value change is a major version bump because it re-renders
every product; consuming `main` would let that land unannounced.

### 2. Agents — the skill

`skills/umbral-brand/` copied into `.claude/skills/`, or the packaged `.skill` uploaded to
claude.ai. `SKILL.md` is authored instructions; everything it cites lives in `references/` and
`assets/`, which are **generated** by `build/skill.mjs` and verified byte-identical to the build by
`tools/verify_skill.py`.

That verification is the whole point of the decision. A skill that restates values in prose is a
second place they live. `verify_skill.py` fails if any hex in `SKILL.md` is not a current token
value, if a cited rule ID does not exist, or if a pinned asset differs from what the build produced.

### 3. Humans — `dist/CLAUDE.snippet.md`

~40 generated lines to paste into a downstream repo's `CLAUDE.md`: the pinned tag, the raw URLs,
the two modes, and the rules broken most often. It is regenerated on every version bump, so the
pinned tag inside it cannot go stale silently.

## Consequences

**Good**

- No downstream repo needs a build toolchain to get a correct value.
- Pinning is the default and unpinning is the deliberate act, rather than the reverse.
- An agent working in any Umbral repo gets the same values as CI, and CI proves it.
- The skill can no longer drift, which is the specific failure being corrected.

**Costs**

- `tokens/build/`, `rules/rules.json`, the skill's `references/` and `assets/`, and
  `dist/CLAUDE.snippet.md` are all generated *and* committed. That is a lot of generated output in
  version control, and every one of them can go stale. CI rebuilds and diffs all of it.
- Downstream repos must be told to bump. There is no push mechanism; the release notes and
  `CHANGELOG.md` are the mechanism.
- A globally-installed skill at `~/.claude/skills/` is outside this repo's control. Someone with a
  v1.0 copy installed keeps getting v1.0 values until they replace it — which is exactly the state
  Jay's machine was in when Phase 4 started.

**Deferred to Phase 6**

Python and JS packages (`umbral-viz`, `umbral-plot`) on PyPI and npm. Those give a fourth path with
real dependency resolution, which is strictly better than raw URLs for code — but worse for a
notebook that needs one hex, so raw URLs stay.

## Alternatives considered

**A git submodule.** Correct dependency semantics and no duplication. Rejected because submodules
are hostile to the actual contributors here — analysts working in notebooks and Streamlit apps —
and because a submodule still needs a build step to produce `tokens.css`.

**Publish only to npm/PyPI, no raw URLs.** Cleaner, and it is what Phase 6 adds. Rejected as the
*only* path because a Quarto document or a static site should not need a package manager to get a
colour.

**Generate on install rather than committing `build/`.** Avoids stale committed output. Rejected:
it forces Node into every consumer, including R and Quarto users who have no reason to have it.
