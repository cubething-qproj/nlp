# note-lab

Statistical test lab for Quell's reading notes. The player highlights passages
in in-world texts and writes free-text notes; the game needs concept ids out of
both, to gate canned NPC dialogue. Interpreters are prototyped and measured
here, at tiers 0–2 of the "System One" research (authored annotations, embedding
similarity, schema-driven encoders). Only a chosen one is ported to Rust.

```sh
uv sync
uv run pytest
uv run notelab check data/fixture       # validate a data set; lists every problem, exits 1 if any
```

## Data (`data/`)

Real texts are excerpts from books and are **never committed**: everything in
`data/` is gitignored except `data/fixture/`, a tiny made-up set for tests and
smoke runs. A data set is a directory:

| path            | contents                                                                 |
| --------------- | ------------------------------------------------------------------------ |
| `texts/*.txt`   | Source texts, plain, exactly as the player reads them.                   |
| `texts/*.json`  | Optional annotations for the same-named text (see below).                |
| `concepts.toml` | Concept ids with label and description; the closed stance and slot sets. |
| `notes.jsonl`   | One note per line: text, highlighted span, gold labels, `dev`/`holdout`. |

All offsets are `[start, end)` in Unicode code points over the text file; a
Rust port must convert from byte offsets.

Downloaded pages come in all sorts of encodings, and Label Studio only reads
UTF-8. Run `uv run scripts/to_utf8.py data/documents` before importing: it
detects each file's encoding, rewrites it as UTF-8, and keeps the original as
`<name>.orig` (`--dry-run` to only report).

**Annotations** are a [W3C Web Annotation](https://www.w3.org/TR/annotation-model/)
`AnnotationPage`, so they can overlap and stack freely. We read a subset:

- `id`, and `layer`: our extension, naming what kind of structure the
  annotation is (free-form for now).
- `body`: one `TextualBody` with `"purpose": "tagging"` per concept id in
  `value`. Bodies with other purposes are ignored.
- `target`: one per range, each with `source` (the text's file name) and a
  `TextPositionSelector`. An optional `TextQuoteSelector` (`exact`, plus
  `prefix`/`suffix`) is checked against the text, so offsets that drift after
  a text edit fail loudly.

W3C allows a single object anywhere we show an array. Relations between
annotations (W3C `linking` annotations) aren't read yet.

**Notes:** `span` is the player's highlight; the optional `highlight` quotes
it and is checked like `exact` above. Gold `concepts` are everything the note
plus its highlight should resolve to. Thresholds and few-shot prototypes are
fitted on `dev` only; `holdout` is for reporting.

## Experiments

Same conventions as hex-lab: every experiment gets a tagged commit
(`exp/NN-name`), a summary in `experiments/NN-name.md`, and figures under
`.docs/designs/quell-reading-notes/experiments/NN-name/`. Arms are never
deleted from the registry, so any tag reruns. Exemplars first; statistics on
request.
