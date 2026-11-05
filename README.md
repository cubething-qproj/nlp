# nlp lab

Model experiments for Quell's debate system: can a small local model turn
natural language into argument maps the xAIF editor (`../xAIF`) accepts?

The first experiment is the direct-model spike: a CPU-bound model writes a
compact notation under a grammar, a deterministic expander turns it into
xAIF, and the editor's own rules check it. See the spike record in the wiki
(`debate-spike`).

The earlier reading-notes lab (note-lab: concept tagging for player notes,
Python) is archived at the tag `note-lab-final`.

## Layout

| path         | contents                                                         |
| ------------ | ---------------------------------------------------------------- |
| `data/`      | Library and corpus excerpts from published books. Never committed. |
| `inception/` | INCEpTION layer schemas (see the `inception-api` skill).         |
| `scripts/`   | Data-preparation scripts, including `pta_schema.py`.             |
| `models/`    | GGUF weights. Never committed.                                   |
| `results/`   | Experiment outputs; they quote the corpus. Never committed.      |

Gold argument maps live in `../xAIF/examples/`, where the editor opens them.

## Experiments

Every experiment gets a tagged commit (`exp/NN-name`) and a summary in
`experiments/NN-name.md`. Exemplars come before statistics.
