# /// script
# requires-python = ">=3.12"
# dependencies = ["beautifulsoup4", "charset-normalizer"]
# ///
"""Convert downloaded web pages and texts to UTF-8 in place, before importing them into Label Studio.

Label Studio reads every file as UTF-8 and fails on anything else ("invalid
continuation byte"). Files that already decode as UTF-8 are left alone. For
the rest the encoding is taken from a BOM, then the page's own `<meta
charset>`, then a statistical guess (`UnicodeDammit` with charset-normalizer).
The original bytes are kept next to the file as `<name>.orig`.

    uv run scripts/to_utf8.py data/documents            # a directory, recursively
    uv run scripts/to_utf8.py page.html notes.txt       # or single files
    uv run scripts/to_utf8.py --dry-run data/documents  # report only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bs4 import UnicodeDammit

SUFFIXES = {".html", ".htm", ".txt"}
# Browsers (WHATWG) decode these labels as windows-1252, and real pages rely on it.
ALIASES = {"iso-8859-1": "windows-1252", "latin-1": "windows-1252", "ascii": "windows-1252"}
META_CHARSET = re.compile(rb"""(<meta[^>]+charset=["']?)[\w-]+""", re.I)


def convert(path: Path, dry_run: bool) -> bool:
    """Rewrite `path` as UTF-8 if it isn't already; False if its encoding couldn't be detected."""
    raw = path.read_bytes()
    try:
        raw.decode("utf-8")
        return True
    except UnicodeDecodeError:
        pass

    html = path.suffix.lower() in {".html", ".htm"}
    detected = UnicodeDammit(raw, is_html=html).original_encoding
    if detected is None:
        print(f"SKIP  {path}: could not detect encoding", file=sys.stderr)
        return False
    encoding = ALIASES.get(detected.lower(), detected)

    text = raw.decode(encoding, errors="replace")
    undecodable = text.count("�")
    print(f"{'WOULD' if dry_run else 'OK   '} {path}: {encoding} -> utf-8"
          + (f" ({undecodable} undecodable chars, check by eye)" if undecodable else ""))
    if not dry_run:
        out = text.encode("utf-8")
        if html:
            out = META_CHARSET.sub(rb"\1utf-8", out)
        path.with_name(path.name + ".orig").write_bytes(raw)
        path.write_bytes(out)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", type=Path, help="files or directories")
    parser.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    args = parser.parse_args()

    files = [f for p in args.paths for f in (sorted(p.rglob("*")) if p.is_dir() else [p])]
    results = [convert(f, args.dry_run) for f in files if f.is_file() and f.suffix.lower() in SUFFIXES]
    if not all(results):
        sys.exit(f"{results.count(False)} files left unconverted")


if __name__ == "__main__":
    main()
