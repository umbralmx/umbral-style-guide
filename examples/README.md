# `examples/`

Working examples that open without a build step. Each one loads `tokens/build/` directly, so a
token change re-renders it. Nothing here writes a colour, a size or a space.

| | |
|---|---|
| `componentes.html` | The ten components from `packages/umbral-plot/src/components.css`, in both modes |

Open `componentes.html` in a browser. There is no server and no bundler.

`umbral-lint` runs over this folder like any other, and CLAUDE.md's definition of done requires an
example here for any change that adds a form. An example that cannot be opened is not an example.
