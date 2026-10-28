"""Convert the scraped source documents in `data/documents` from HTML to Typst.

The two sources have unrelated markup, so each gets its own block-level reader
over a shared inline renderer:

- `elimination.html`: OCR'd article. Numbered all-caps paragraphs are section
  headings, `<sup>n</sup>` markers point into a trailing "Notes" section (turned
  into `#footnote`s), numbered blockquotes are lists, and the symbolic-logic
  formulas in the table become math.
- `what is metaphysics.html`: calibre epub pages concatenated together. The
  cover becomes document metadata and `#title`, the TOC page `#outline`, bold
  paragraphs subheadings, and the all-caps `h5` callouts block quotes.

Usage: `python3 scripts/html_to_typst.py data/documents/elimination.html [...]`
(needs `bs4`, which is not a project dependency),
writing `<name>.typ` next to each input.
"""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

# Chars with markup meaning anywhere in a line.
ESCAPE = re.compile(r"([\\#*_$@<>\[\]~`])")
# Bare whitespace only: `\s` would also eat no-break spaces.
SPACES = re.compile(r"[ \t\r\n\f]+")
# "4. THE SIGNIFICANCE OF A SENTENCE"
SECTION = re.compile(r"^(\d+)\. ([A-Z][A-Z ,\-]+)$")
# "1. ...", "(1.) ..."
ITEM = re.compile(r"^(\()?\d+\.\)? ")
# "Ou(?)", "?(r)", "∼(∃x).Ou(x)"
FORMULA = re.compile(r"^[∼(∃x).]*(\?|[A-Z][a-z]?)\([a-z?]+\)$")


class Inline:
    """Renders a run of inline HTML nodes as Typst markup.

    Text is flattened into `(text, flags)` runs first, so formatting split over
    adjacent tags (`<b>a</b><span> </span><b>b</b>`) merges into one `*a b*`.
    """

    def __init__(self, footnote=lambda node: ""):
        self.footnote = footnote

    def render(self, nodes) -> str:
        runs = [r for n in nodes for r in self.runs(n, frozenset())]
        runs = [(SPACES.sub(" ", t) if not raw else t, f, raw) for t, f, raw in runs]
        runs = self.settle_whitespace(runs)
        groups = []
        for text, flags, raw in runs:
            piece = text if raw else escape(text)
            if groups and groups[-1][1] == flags:
                groups[-1][0] += piece
            else:
                groups.append([piece, flags])
        return SPACES.sub(" ", wrap_groups(groups)).strip()

    def runs(self, node, flags):
        """Yields `(text, flags, raw)`; `raw` text is already markup."""
        if isinstance(node, Comment):
            return
        if isinstance(node, NavigableString):
            yield str(node), flags, False
            return
        classes = set(node.get("class", []))
        if node.name == "br":
            yield " \\ ", flags, True
        elif node.name == "sup":
            yield self.footnote(node), flags, True
        elif node.name == "a" and node.get("href", "").startswith("http"):
            body = Inline(self.footnote).render(node.children)
            yield f'#link("{node["href"]}")[{body}]', flags, True
        else:
            if node.name in ("b", "strong") or "calibre5" in classes:
                flags |= {"b"}
            if node.name in ("i", "em") or "calibre6" in classes:
                flags |= {"i"}
            for child in node.children:
                yield from self.runs(child, flags)

    @staticmethod
    def settle_whitespace(runs):
        """Whitespace-only runs take the formatting shared by both neighbours."""
        solid = [i for i, (t, _, raw) in enumerate(runs) if raw or t.strip()]
        out = []
        for i, (text, flags, raw) in enumerate(runs):
            if not raw and not text.strip():
                prev = next((runs[j][1] for j in reversed(solid) if j < i), frozenset())
                nxt = next((runs[j][1] for j in solid if j > i), frozenset())
                flags = prev & nxt
            out.append((text, flags, raw))
        return out


class Elimination:
    """Reader for the OCR'd Carnap article; see the module docs."""

    def __init__(self, soup: BeautifulSoup):
        nodes = list(soup.contents)
        start = next(i for i, n in enumerate(nodes) if is_tag(n, "center") and n.get_text(strip=True) == "Notes")
        self.body, notes = nodes[:start], [n for n in nodes[start + 1 :] if is_tag(n, "p") and n.get_text(strip=True)]
        self.notes = {}
        for p in notes:
            text = Inline().render(p.children)
            number, rest = re.match(r"^(\d+)\. (.*)$", text).groups()
            self.notes[number] = rest
        self.inline = Inline(lambda sup: f"#footnote[{self.notes[sup.get_text(strip=True)]}]")
        self.dropped = []

    def convert(self) -> str:
        head = ['#set document(title: [{title}], author: "{author}")', "#set smartquote(enabled: false)", '#set heading(numbering: "1.")', ""]
        out, loose, items = [], [], []

        def flush():
            if loose:
                if text := self.inline.render(loose):
                    out.append(line_start(text))
                loose.clear()
            if items:
                out.append("\n".join(f"+ {i}" for i in items))
                items.clear()

        titled = False
        for node in self.body:
            if isinstance(node, NavigableString) or node.name in ("i", "b", "sup"):
                if str(node).strip() == ">":
                    self.dropped.append("stray `>` before the table")
                    continue
                loose.append(node)
                continue
            flush()
            text = node.get_text(" ", strip=True)
            if node.name == "hr" or not text:
                continue
            if node.name == "center" and not titled:
                titled = True
                title, author = self.title(node, head, out)
            elif node.name == "center":
                out.append(f"#heading(numbering: none)[{self.inline.render(node.children)}]")
            elif node.name == "p" and (m := SECTION.match(text)):
                out.append(f"= {m.group(2)}")
            elif node.name == "p" and ITEM.match(text):
                items.append(ITEM.sub("", self.inline.render(node.children)))
            elif node.name == "p":
                out.append(line_start(self.inline.render(node.children)))
            elif node.name == "blockquote":
                out.append(self.blockquote(node))
            elif node.name == "table":
                out.append(self.table(node))
            else:
                raise ValueError(f"unhandled <{node.name}>")
        flush()
        head[0] = head[0].format(title=title, author=author)
        return "\n".join(head) + "\n" + "\n\n".join(out) + "\n"

    def title(self, center: Tag, head: list, out: list):
        """`<p>TITLE<br/>by<br/>AUTHOR</p><p>(TRANSLATED BY ...)</p>`."""
        byline, translator = center.find_all("p")
        title, by, author = [SPACES.sub(" ", s).strip() for s in byline.stripped_strings]
        out.append("#title()")
        # Plain paragraphs, not `#align`: HTML export drops aligned content.
        out += [f"{by} \\ {escape(author)}", escape(translator.get_text(strip=True))]
        return escape(title), author.title()

    def blockquote(self, quote: Tag) -> str:
        """Splits on `<p>`, the first item being the loose text before them."""
        parts, current = [], []
        for child in quote.children:
            if is_tag(child, "p"):
                parts.append(current)
                parts.append(list(child.children))
                current = []
            else:
                current.append(child)
        parts.append(current)
        parts = [t for t in (self.inline.render(p) for p in parts) if t]
        if all(ITEM.match(p) for p in parts):
            numbering = "(1.)" if parts[0].startswith("(") else "1."
            body = "\n".join(f"  + {ITEM.sub('', p)}" for p in parts)
            return f'#quote(block: true)[\n  #set enum(numbering: "{numbering}")\n{body}\n]'
        return "#quote(block: true)[\n  " + "\n\n  ".join(map(line_start, parts)) + "\n]"

    def table(self, table: Tag) -> str:
        rows = table.find_all("tr")
        cells = [[self.cell(td) for td in row.find_all("td")] for row in rows]
        header = "".join(f"[{c}]" for c in cells[0])
        body = "\n".join("  " + ", ".join(f"[{c}]" for c in row) + "," for row in cells[1:])
        return f"#table(\n  columns: {len(cells[0])},\n  table.header{header},\n{body}\n)"

    def cell(self, td: Tag) -> str:
        """Lines split on `<br>`/`<p>`; lines that are formulas become math."""
        paras, current = [], []
        for child in td.children:
            if is_tag(child, "p"):
                paras += [current, list(child.children)]
                current = []
            else:
                current.append(child)
        paras.append(current)
        rendered = []
        for nodes in paras:
            lines = [l.strip() for l in self.inline.render(nodes).split(" \\ ")]
            lines = [math(l) if FORMULA.match(unescape(l)) else line_start(l) for l in lines if l]
            if lines:
                rendered.append(" \\ ".join(lines))
        return "\n\n".join(rendered)


class Metaphysics:
    """Reader for the calibre Heidegger epub dump; see the module docs."""

    def __init__(self, raw: str):
        self.pages = [BeautifulSoup(p, "html.parser") for p in raw.split("</html>") if "<body" in p]
        self.inline = Inline()
        self.merged = []

    def convert(self) -> str:
        head, out = ["#set smartquote(enabled: false)", "#set par(first-line-indent: 1.6em)", ""], []
        for page in self.pages:
            body = page.body
            if body.find("h1", class_="heading"):
                title = body.h1.get_text(strip=True)
                author = body.h3.get_text(strip=True)
                publisher = body.find("p", class_="front-matter-imprint").get_text(strip=True)
                head.insert(0, f'#set document(title: [{escape(title)}], author: "{author}")')
                out += ["#title()", escape(author), escape(publisher)]
            elif body.get("id") == "inline-toc":
                out.append(f"#outline(title: [{escape(body.h2.get_text(strip=True))}], depth: 1)")
            else:
                self.blocks(body, out)
        return "\n".join(head) + "\n" + "\n\n".join(out) + "\n"

    def blocks(self, node: Tag, out: list):
        for child in node.children:
            if not isinstance(child, Tag):
                continue
            classes = set(child.get("class", []))
            text = child.get_text(strip=True)
            if child.name == "div" and "heading-section-break" not in classes:
                self.blocks(child, out)
            elif not text or child.name == "div":
                continue
            elif child.name == "h1":
                out.append(f"= {self.inline.render(child.children)}")
            elif child.name == "h5":
                out.append(f"#quote(block: true)[{self.inline.render(child.children)}]")
            elif child.name == "p" and ("font-weight-bold" in classes or all_caps_bold(child)):
                out.append(f"== {self.inline.render(child.children)}")
            elif child.name == "p" and "font-weight-bold1" in classes:
                out.append(f"*{self.inline.render(child.children)}*")
            elif child.name == "p":
                para = self.inline.render(child.children)
                # Epub page breaks split sentences across two <p>s.
                if out and text[0].islower() and not re.search(r"[.?!:;”\"’)]$", out[-1]):
                    self.merged.append(f"…{out[-1][-30:]} | {para[:30]}…")
                    out[-1] += " " + para
                else:
                    out.append(line_start(para))
            else:
                raise ValueError(f"unhandled <{child.name}>")


def all_caps_bold(p: Tag) -> bool:
    """Some subheadings are plain paragraphs with every word bolded."""
    words = [s for s in p.find_all(string=True) if s.strip()]
    return p.get_text().isupper() and all(s.find_parent("b") for s in words)


def is_tag(node, name: str) -> bool:
    return isinstance(node, Tag) and node.name == name


def escape(text: str) -> str:
    """Escapes markup chars, plus the sequences Typst would turn into
    typography: `--` dashes, `...` ellipses, `-1` minus signs, `//` comments."""
    text = ESCAPE.sub(r"\\\1", text)
    text = re.sub(r"(?<=-)-|-(?=\d)", r"\\-", text)
    text = re.sub(r"(?<=\.\.)\.", r"\\.", text)
    return re.sub(r"(?<=/)/", r"\\/", text)


def unescape(markup: str) -> str:
    return re.sub(r"\\(.)", r"\1", markup)


def line_start(markup: str) -> str:
    """Escapes what Typst reads as list/heading syntax at the start of a line."""
    if m := re.match(r"^(\d+)\.", markup):
        return m.group(1) + "\\." + markup[m.end() :]
    if re.match(r"^([=+\-]|/ )", markup):
        return "\\" + markup
    return markup


def math(markup: str) -> str:
    """`∼(∃x).Ou(x)` → `$∼(∃x)."Ou"(x)$`: multi-letter names and predicates
    are upright text, single-letter variables stay italic."""
    formula = unescape(markup)
    formula = re.sub(r"[A-Za-z]{2,}|[A-Z](?=\()", lambda m: f'"{m.group()}"', formula)
    return f"${formula}$"


def wrap_groups(groups) -> str:
    """Emits `[markup, flags]` groups, wrapping formatted ones in `*`/`_`, or
    in `#strong[]`/`#emph[]` when a delimiter would touch a word character."""
    out = ""
    for i, (markup, flags) in enumerate(groups):
        if not flags or not markup.strip():
            out += markup
            continue
        lead = markup[: len(markup) - len(markup.lstrip())]
        trail = markup[len(markup.rstrip()) :]
        body = markup.strip()
        after = trail or (groups[i + 1][0][:1] if i + 1 < len(groups) else "")
        before = lead or out[-1:]
        if (before and before[-1].isalnum()) or (after and after[0].isalnum()):
            for flag, fn in (("i", "emph"), ("b", "strong")):
                if flag in flags:
                    body = f"#{fn}[{body}]"
            if after[:1] in ("(", "[", ".", ";"):
                body += ";"
        else:
            for flag, delim in (("i", "_"), ("b", "*")):
                if flag in flags:
                    body = f"{delim}{body}{delim}"
        out += lead + body + trail
    return out


def convert(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if "calibre" in raw:
        reader = Metaphysics(raw)
        typ = reader.convert()
        for m in reader.merged:
            print(f"  merged split paragraph: {m}")
    else:
        reader = Elimination(BeautifulSoup(raw, "html.parser"))
        typ = reader.convert()
        for d in reader.dropped:
            print(f"  dropped {d}")
    return typ


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        src = Path(arg)
        print(src)
        src.with_suffix(".typ").write_text(convert(src), encoding="utf-8")
