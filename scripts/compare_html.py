"""Compare an original HTML document with its Typst round trip.

Prints the element counts on both sides, then a word-level diff of the
visible body text, so dropped, moved, or mangled text shows up regardless of
how the markup changed.

Usage: `python3 scripts/compare_html.py original.html roundtrip.html`
"""

import difflib
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

TAGS = ["h1", "h2", "h3", "h5", "p", "blockquote", "ol", "li", "table", "td", "th", "i", "em", "b", "strong", "sup", "a", "math", "br"]


def load(path: str) -> BeautifulSoup:
    soup = BeautifulSoup(Path(path).read_text(encoding="utf-8"), "html.parser")
    for tag in soup.find_all(["head", "style", "title"]):
        tag.decompose()
    return soup


def words(soup: BeautifulSoup) -> list[str]:
    return soup.get_text(" ").split()


def show(words_: list[str], i: int, j: int) -> str:
    text = " ".join(words_[i:j])
    return text if len(text) < 160 else text[:75] + " … " + text[-75:]


if __name__ == "__main__":
    a, b = load(sys.argv[1]), load(sys.argv[2])
    ca, cb = Counter(t.name for t in a.find_all(True)), Counter(t.name for t in b.find_all(True))
    print("elements  original  roundtrip")
    for tag in TAGS:
        if ca[tag] or cb[tag]:
            print(f"{tag:<9} {ca[tag]:>8}  {cb[tag]:>9}")
    wa, wb = words(a), words(b)
    matcher = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    print(f"\nwords: {len(wa)} original, {len(wb)} roundtrip, similarity {matcher.ratio():.4f}\n")
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op != "equal":
            print(f"{op:>7} @{i1}: - {show(wa, i1, i2)!r}\n{'':>9}+ {show(wb, j1, j2)!r}")
