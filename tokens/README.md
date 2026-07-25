# `tokens/`

Every colour, font and spacing value in the system.

| | |
|---|---|
| `src/` | **Authored.** W3C DTCG format. The only place a value is written. |
| `build/` | **Generated.** Eleven targets, committed so downstream repos can fetch a raw URL. |

```bash
npm run build:tokens        # generates build/ and runs the contrast gate
python3 tools/verify_tokens.py
```

The build **fails** if a token misses the contrast threshold for its declared role — text needs
4.5:1, data marks need 3:1, and chart furniture (gridlines, borders) is exempt by explicit
per-token declaration. See [ADR-0001](../docs/adr/0001-token-architecture.md) and OQ-001.

Details on how values are derived and how to change one: [`src/README.md`](src/README.md).
