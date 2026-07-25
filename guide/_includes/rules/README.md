# `guide/_includes/rules/`

**Generated. Do not edit.** One callout per rule, built from `rules/rules.yaml` by
`build/rules.mjs`. This whole folder is deleted and rewritten on every build.

Chapters include a callout rather than restating the rule:

```markdown
{{< include _includes/rules/UMB-COL-004.md >}}
```

That is what makes UMB-PRO-002 mechanical — the normative text on a guide page is generated, so
prose cannot drift from the norm. `tools/verify_guide.py` fails if a chapter states a rule's text
without including its callout.

Currently 69 rules: 58 `error`, 10 `warning`,
1 `info`. The full index is `guide/_includes/rule-index.md`.
