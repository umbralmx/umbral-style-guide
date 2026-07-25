# `audit/scripts/`

The measurement scripts behind the Phase 0 audit. Kept so every number in
`2026-07-conformance.md` can be re-derived rather than trusted.

| | |
|---|---|
| `contrast.py` | WCAG contrast matrix for the v1.0 tokens, by role |
| `derive.py` | Finds AA-clearing variants in OKLCH, holding hue fixed |
| `cvd.py` | Dichromacy simulation and OKLab separation between series |
| `pdftext.py` | Reads the brand book PDF by decoding its subset-font ToUnicode CMaps |

```bash
python3 audit/scripts/contrast.py
```

Two notes:

**These hold v1.0 values, deliberately.** They're a historical record of what was measured in July
2026. The live system's numbers come from `tokens/build/contrast.json`, and `cvd.py` is also called
by the CI check for series separability.

**`pdftext.py` exists because poppler wasn't installed.** It decodes the PDF's own font mappings to
recover text. Useful again if another v1.0 artefact turns up as a PDF.
