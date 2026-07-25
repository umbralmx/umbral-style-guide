# `guide/`

The style guide itself — the part a human reads. **Spanish first**; English only where it earns its
place.

## The chapters

| | |
|---|---|
| `00-principios.md` | The five principles and how the normative chain works |
| `01-marca.md` | Logo, isotype geometry, clear space, misuse |
| `02-color.md` | The two modes, tokens, the generated contrast matrix, ramps |
| `03-tipografia.md` | Families, the 500 weight, the scale, self-hosting |
| `04-layout.md` | Spacing, measure, flat surfaces, no shadows |
| `05-voz.md` | Voice, headline construction, hedging |
| `06-numeros.md` | Numbers, dates, units, rates — **new in 1.1** |
| `07-vocabulario-visual.md` | Chart chooser: intent → chart type — **new in 1.1** |
| `08-anatomia-grafica.md` | The title/subtitle/source frame every chart carries |
| `09-incertidumbre.md` | Bands, dashed futures, the `hoy` rule |
| `10-mapas.md` | Choropleths, CVEGEO keys, rates vs counts, small-n — **new in 1.1** |
| `11-accesibilidad.md` | Contrast, `lang`, chart alternatives, keyboard |
| `12-datos-procedencia.md` | `SOURCE.md`, snapshots, licences, reproducibility |
| `13-interpretabilidad.md` | Causal vs descriptive language, dignity |
| `14-superficies/` | One guide per surface: web, Streamlit, Quarto, notebook, social, slides, GitHub, email |
| `15-terminologia.md` | Bilingual controlled vocabulary — **new in 1.1**, and the most credibility-relevant page |

`CHECKLIST.md` and `_includes/` are **generated**. Don't edit them.

## The rule chapters don't restate rules

A chapter never writes a rule in its own words. It *includes* the generated callout:

```markdown
{{< include _includes/rules/UMB-COL-004.md >}}
```

That's what makes UMB-PRO-002 mechanical — prose cannot drift from the norm, because the normative
text is generated from `rules/rules.yaml` at build time. `tools/verify_guide.py` fails if a chapter
states a rule's text without including its callout, or if a rule names a chapter that doesn't
include it.

Prose around the callouts is explanation: it orients, it doesn't oblige.

## Editing

1. Change the chapter, and the rule in `rules/rules.yaml` if the norm itself is changing (UMB-PRO-005).
2. `npm run build && python3 tools/verify_guide.py`
