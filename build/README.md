# `build/`

The generators. Node, run via `npm run build`.

| | Reads | Writes |
|---|---|---|
| `index.mjs` | `tokens/src/*.tokens.json` | `tokens/build/*` — eleven targets + the contrast matrix |
| `rules.mjs` | `rules/rules.yaml` | `rules/rules.json`, `guide/CHECKLIST.md`, `guide/_includes/rules/` |
| `guide.mjs` | the two above | `guide/_includes/*.md` — the data-driven partials |
| `lib/color.mjs` | — | OKLab/OKLCH maths, WCAG contrast, dichromacy simulation |

## What the build enforces

**`index.mjs`** runs the contrast gate and exits non-zero if a token misses the threshold for its
declared role. It also expands the ramp *specs* in `ramp.tokens.json` into concrete steps in OKLCH —
ramps are authored as derivations, not as frozen hex lists.

**`rules.mjs`** validates `rules.yaml` against its JSON Schema, then checks the things a schema
can't: unique IDs, unique check ids, an ID prefix matching the category, live `see_also` references,
and `evidence` on every rule newer than 1.0.

## Why the colour maths exists twice

`lib/color.mjs` computes contrast here; `tools/verify_tokens.py` re-derives the same numbers in
Python from the generated files, and CI runs both.

That's deliberate duplication, which is normally a smell. It's justified because the defect this
system was built to correct was an unverified accessibility claim that survived a year unchallenged.
A mistake now has to be made twice, in two languages, to reach the published system.
