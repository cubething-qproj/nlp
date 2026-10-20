from dataclasses import replace
from pathlib import Path

from hypothesis import given, strategies as st

from notelab.data import Annotation, DataSet, Target, Text, covered_length

FIXTURE = Path(__file__).parents[1] / "data" / "fixture"

ranges = st.lists(st.tuples(st.integers(0, 30), st.integers(1, 10)).map(lambda r: (r[0], r[0] + r[1])), max_size=6)


def text_with(*annotations: Annotation) -> Text:
    return Text("t", "t.txt", "x" * 40, annotations)


def tag(id_: str, concepts: str, *spans: tuple[int, int], layer: str | None = None) -> Annotation:
    targets = tuple(Target("t.txt", lo, hi) for lo, hi in spans)
    return Annotation(id_, layer, frozenset(concepts.split()), targets)


@given(ranges)
def test_covered_length_is_size_of_union(rs):
    assert covered_length(rs) == len({i for lo, hi in rs for i in range(lo, hi)})


def test_concepts_at_scores_share_of_highlight_covered():
    text = text_with(tag("a", "x", (0, 10)), tag("b", "x y", (5, 15), (30, 40)))
    assert text.concepts_at(10, 20) == {"x": 0.5, "y": 0.5}
    # Overlapping ranges of one concept count once.
    assert text.concepts_at(0, 20) == {"x": 0.75, "y": 0.5}
    assert text.concepts_at(15, 30) == {}
    assert text.concepts_at(5, 5) == {}


def test_concepts_at_filters_by_layer():
    text = text_with(tag("a", "x", (0, 10), layer="term"), tag("b", "y", (0, 10), layer="argument"))
    assert text.concepts_at(0, 10, layer="term") == {"x": 1.0}
    assert text.concepts_at(0, 10) == {"x": 1.0, "y": 1.0}


def test_annotation_accepts_single_objects_or_arrays():
    position = {"type": "TextPositionSelector", "start": 1, "end": 4}
    one = Annotation.from_json({
        "id": "a", "body": {"purpose": "tagging", "value": "x"},
        "target": {"source": "t.txt", "selector": position},
    })
    many = Annotation.from_json({
        "id": "a", "body": [{"purpose": "tagging", "value": "x"}, {"purpose": "commenting", "value": "hm"}],
        "target": [{"source": "t.txt", "selector": [position]}],
    })
    assert one == many == Annotation("a", None, frozenset({"x"}), (Target("t.txt", 1, 4),))


def test_target_checks_quote_against_text():
    plain = "abcdefgh"
    assert Target("t", 2, 5, "cde", "ab", "fg").problems(plain) == []
    assert len(Target("t", 3, 6, "cde", "ab", "fg").problems(plain)) == 3
    assert len(Target("t", 6, 9).problems(plain)) == 1
    # Context running off either end of the text is a mismatch, not a crash.
    assert len(Target("t", 1, 3, prefix="xa", suffix=None).problems(plain)) == 1
    assert len(Target("t", 6, 8, suffix="hx").problems(plain)) == 1


def test_text_offsets_are_byte_exact(tmp_path):
    (tmp_path / "t.txt").write_bytes("a\r\nb".encode())
    assert Text.load(tmp_path / "t.txt").plain == "a\r\nb"


def test_fixture_is_valid():
    assert DataSet.load(FIXTURE).problems() == []


def test_problems_catch_bad_annotations_and_notes():
    data = DataSet.load(FIXTURE)
    text = data.texts["ferry"]
    annotation = replace(text.annotations[0], concepts=frozenset({"nope"}))
    note = data.notes[0]
    bad_note = replace(note, span=(note.span[0] + 1, note.span[1] + 1), gold=replace(note.gold, stance="maybe"))
    bad = replace(
        data,
        texts={"ferry": replace(text, annotations=(annotation, *text.annotations[1:]))},
        notes=(bad_note, *data.notes[1:]),
    )
    problems = bad.problems()
    assert len(problems) == 3
    assert sum(p.startswith(f"note {note.id}:") for p in problems) == 2
