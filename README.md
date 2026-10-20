# note-lab

Statistical test lab for Quell's reading notes. The player highlights passages
in in-world texts and writes free-text notes; the game needs concept ids out of
both, to gate canned NPC dialogue. Interpreters are prototyped and measured
here, at tiers 0–2 of the "System One" research (span tags, embedding
similarity, schema-driven encoders). Only a chosen one is ported to Rust.

```sh
uv sync
uv run pytest
```

## Data (`data/`)

Real texts are excerpts from books and are **never committed**: everything in
`data/` is gitignored except `data/fixture/`, a tiny made-up set for tests and
smoke runs. A data set is a directory:

| path            | contents                                                                    |
| --------------- | --------------------------------------------------------------------------- |
| `texts/*.txt`   | Source texts, marked up with span tags: `[clue id=river_ford]…[/clue]`.     |
| `concepts.toml` | Concept ids with label and description; the closed stance and slot sets.    |
| `notes.jsonl`   | One note per line: text, highlighted span, gold labels, `dev`/`holdout`.    |

A note's `span` is `[start, end)` in Unicode code points over the text as the
player sees it (tags stripped); a Rust port must convert from byte offsets.
The optional `highlight` quotes that span for readability and is checked
against it, so a text edit that shifts offsets fails loudly. Gold `concepts`
are everything the note plus its highlight should resolve to. Thresholds and
few-shot prototypes are fitted on `dev` only; `holdout` is for reporting.

## Experiments

Same conventions as hex-lab: every experiment gets a tagged commit
(`exp/NN-name`), a summary in `experiments/NN-name.md`, and figures under
`.docs/designs/quell-reading-notes/experiments/NN-name/`. Arms are never
deleted from the registry, so any tag reruns. Exemplars first; statistics on
request.
