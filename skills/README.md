# `skills/`

Agent skills — what Claude loads when it works in an Umbral repo.

| | |
|---|---|
| `umbral-brand/` | The brand and data-visualization system, packaged for an agent |

## Installing it

**In another repo (Claude Code):**

```bash
mkdir -p .claude/skills
cp -r path/to/umbral-style-guide/skills/umbral-brand .claude/skills/
```

**Globally, for every project:**

```bash
cp -r skills/umbral-brand ~/.claude/skills/
```

**On claude.ai:** upload the packaged `.skill` file attached to each GitHub release.

## If you already have a v1.0 skill installed

Replace it. The v1.0 skill bundles the old token values — including `caption` at 2.37:1 and `muted`
at 4.25:1, both of which fail WCAG AA — and the old logo SVGs with the wrong bar ratios. An
installed copy keeps handing those out no matter what the repo says.

```bash
rm -rf ~/.claude/skills/umbral-brand
cp -r skills/umbral-brand ~/.claude/skills/
```

## Why the references are generated

`SKILL.md` is authored — it is instructions. Everything it cites lives in `references/` and
`assets/`, which are **generated from the normative layer** by `build/skill.mjs`.

That is the whole point. A skill that restates token values in prose is a second place those values
live, and it will drift — which is exactly what the v1.0 skill did.
