"""Verify the two packages against the normative layer.

The packages are the fourth and fifth place token values could live. This is what
stops them becoming a second v1.0 skill — which shipped frozen copies of the old
tokens and handed out failing contrast for a year because nothing compared them.

Checks:
  * every vendored file is byte-identical to what the build produced;
  * no module writes a colour, font or size as a literal;
  * the generated JS token module agrees with tokens.json value for value;
  * both packages import, and their guardrails actually fire.

Run: python3 tools/verify_packages.py    (exit 1 on any failure)
"""
from __future__ import annotations

import filecmp
import json
import pathlib
import re
import subprocess
import sys

VIZ = pathlib.Path("packages/umbral-viz")
PLOT = pathlib.Path("packages/umbral-plot")
DATA = VIZ / "umbral_viz/_data"

failures: list[str] = []
count = 0


def check(ok: bool, msg: str) -> None:
    global count
    count += 1
    if not ok:
        failures.append(msg)


if not DATA.exists():
    sys.exit("packages/ not built — run `npm run build:packages` first")

tokens = json.loads(pathlib.Path("tokens/build/tokens.json").read_text())
rules = json.loads(pathlib.Path("rules/rules.json").read_text())

# ── 1. vendored data is byte-identical ────────────────────────────────────
VENDORED = [
    ("tokens/build/tokens.json", "tokens.json"),
    ("tokens/build/contrast.json", "contrast.json"),
    ("tokens/build/umbral-laboratorio.mplstyle", "umbral-laboratorio.mplstyle"),
    ("tokens/build/umbral-instrumento.mplstyle", "umbral-instrumento.mplstyle"),
    ("tokens/build/plotly-umbral-laboratorio.json", "plotly-umbral-laboratorio.json"),
    ("tokens/build/plotly-umbral-instrumento.json", "plotly-umbral-instrumento.json"),
    ("tokens/build/streamlit-config.toml", "streamlit-config.toml"),
    ("rules/rules.json", "rules.json"),
]
for src, name in VENDORED:
    dst = DATA / name
    check(dst.exists(), f"umbral-viz is missing vendored {name}")
    if dst.exists():
        check(filecmp.cmp(src, dst, shallow=False),
              f"{name} differs from {src} — run `npm run build:packages`")

check(filecmp.cmp("tokens/build/tokens.css", PLOT / "dist/umbral.css", shallow=False),
      "umbral-plot/dist/umbral.css differs from tokens/build/tokens.css")

for _mode in ("laboratorio", "instrumento"):
    _css = f"observable-framework-{_mode}.css"
    check(filecmp.cmp(f"tokens/build/{_css}", PLOT / "dist" / _css, shallow=False),
          f"umbral-plot/dist/{_css} differs from tokens/build/{_css}")

# ── 2. no module writes a value as a literal ──────────────────────────────
live_hex = {v.lower() for m in tokens["mode"].values()
            for v in m.values() if isinstance(v, str) and v.startswith("#")}
families = {tokens["font"][k] for k in ("display", "body", "mono")}

for py in sorted((VIZ / "umbral_viz").glob("*.py")):
    text = py.read_text()
    for hexv in set(re.findall(r"#[0-9a-fA-F]{6}\b", text)):
        check(False, f"{py}: contains the literal {hexv} — read it from tokens")
    for fam in families:
        # naming a family in a docstring is fine; assigning it is not
        for m in re.finditer(rf"=\s*[\"']{re.escape(fam)}[\"']", text):
            check(False, f"{py}:{text[:m.start()].count(chr(10)) + 1}: "
                         f"assigns the literal {fam!r} — use tokens.font()")

for js in sorted((PLOT / "src").glob("*.js")):
    if js.name == "tokens.js":
        continue                      # generated; it IS the values
    text = js.read_text()
    for hexv in set(re.findall(r"#[0-9a-fA-F]{6}\b", text)):
        check(False, f"{js}: contains the literal {hexv} — import it from tokens.js")

# ── 3. the generated JS module agrees with tokens.json ────────────────────
js_src = (PLOT / "src/tokens.js").read_text()
check("GENERATED from tokens/build/tokens.json" in js_src,
      "umbral-plot/src/tokens.js has no generated-file header")
for mode, vals in tokens["mode"].items():
    for name, v in vals.items():
        if isinstance(v, str):
            check(f'"{v}"' in js_src,
                  f"tokens.js is missing {mode}/{name} = {v}")
check(f'"{rules["version"]}"' in js_src,
      "tokens.js is not pinned to the current design-system version")

# ── 4. both packages import, and their guardrails fire ────────────────────
py_probe = r"""
import sys, json
sys.path.insert(0, "packages/umbral-viz")
import umbral_viz as uv
out = {"version": uv.__version__, "signal": uv.color("signal"),
       "series": uv.series(n=3), "ramp": len(uv.ramp("diverging"))}
try:
    uv.Frame(title="una afirmacion completa aqui", subtitle="x", source="")
    out["no_source"] = "DID NOT RAISE"
except uv.MissingSource:
    out["no_source"] = "raises"
try:
    uv.series(n=7); out["too_many"] = "DID NOT RAISE"
except ValueError:
    out["too_many"] = "raises"
try:
    uv.tokens.tokens("oscuro"); out["bad_mode"] = "DID NOT RAISE"
except uv.tokens.UnknownMode:
    out["bad_mode"] = "raises"
print(json.dumps(out))
"""
res = subprocess.run([sys.executable, "-c", py_probe], capture_output=True, text=True)
check(res.returncode == 0, f"umbral-viz failed to import: {res.stderr.strip()[:300]}")
if res.returncode == 0:
    got = json.loads(res.stdout)
    check(got["version"] == rules["version"], "umbral-viz version disagrees with the rule set")
    check(got["signal"] == tokens["mode"]["laboratorio"]["signal"],
          "umbral-viz returns the wrong signal value")
    check(got["series"] == tokens["mode"]["laboratorio"]["series"][:3],
          "umbral-viz series order disagrees with the tokens")
    check(got["ramp"] == len(tokens["ramp"]["laboratorio"]["diverging"]),
          "umbral-viz diverging ramp length disagrees")
    for k in ("no_source", "too_many", "bad_mode"):
        check(got[k] == "raises", f"umbral-viz guardrail {k} did not fire")

js_probe = """
import('./packages/umbral-plot/src/index.js').then((m) => {
  const out = { version: m.version, signal: m.tokens.tokensFor().signal,
                series: m.categorical(3), ramp: m.diverging().length,
                label: m.label('signal').fill,
                bandOpacity: m.band().fillOpacity };
  try { new m.Frame({ title: 'una afirmacion completa aqui', subtitle: 'x', source: '' });
        out.no_source = 'DID NOT THROW'; }
  catch (e) { out.no_source = e.rule || 'throws'; }
  try { m.categorical(7); out.too_many = 'DID NOT THROW'; }
  catch { out.too_many = 'throws'; }
  console.log(JSON.stringify(out));
});
"""
res = subprocess.run(["node", "-e", js_probe], capture_output=True, text=True)
check(res.returncode == 0, f"umbral-plot failed to import: {res.stderr.strip()[:300]}")
if res.returncode == 0:
    got = json.loads(res.stdout)
    lab = tokens["mode"]["laboratorio"]
    check(got["version"] == rules["version"], "umbral-plot version disagrees with the rule set")
    check(got["signal"] == lab["signal"], "umbral-plot returns the wrong signal value")
    check(got["series"] == lab["series"][:3], "umbral-plot series order disagrees")
    check(got["ramp"] == len(tokens["ramp"]["laboratorio"]["diverging"]),
          "umbral-plot diverging ramp length disagrees")
    check(got["label"] == lab["signal-text"],
          "umbral-plot direct labels must use signal-text, not signal — "
          "a series label is small text and needs 4.5:1")
    check(got["bandOpacity"] == tokens["uncertaintyBandOpacity"],
          "umbral-plot band opacity disagrees with the token")
    check(got["no_source"] == "UMB-CHT-003", "umbral-plot Frame accepted a chart with no source")
    check(got["too_many"] == "throws", "umbral-plot allowed more than 5 series")

# ── 5. doctests run (they must be run as a package, not standalone) ───────
doc_probe = r"""
import doctest, sys
sys.path.insert(0, "packages/umbral-viz")
import umbral_viz.tokens, umbral_viz.chart, umbral_viz.themes
fails = 0
for mod in (umbral_viz.tokens, umbral_viz.chart, umbral_viz.themes):
    fails += doctest.testmod(mod, verbose=False).failed
print(fails)
"""
res = subprocess.run([sys.executable, "-c", doc_probe], capture_output=True, text=True)
check(res.returncode == 0 and res.stdout.strip() == "0",
      f"umbral-viz doctests failed: {res.stdout.strip()} {res.stderr.strip()[:200]}")

# ── 6. manifests are pinned to the design-system version ──────────────────
pyproject = (VIZ / "pyproject.toml").read_text()
check(f'version = "{rules["version"]}"' in pyproject,
      f"umbral-viz pyproject.toml is not at {rules['version']}")
pkg = json.loads((PLOT / "package.json").read_text())
check(pkg["version"] == rules["version"],
      f"umbral-plot package.json is at {pkg['version']}, not {rules['version']}")
check("_data/*" in pyproject, "umbral-viz does not ship its _data/ as package data")

print(f"verify_packages: {count} checks, {len(failures)} failed")
print(f"  {len(VENDORED) + 1} vendored files byte-identical · both packages import · "
      f"pinned to v{rules['version']}")
if failures:
    for f in failures:
        print(f"  FAIL  {f}")
    sys.exit(1)
print("packages agree with the normative layer")
