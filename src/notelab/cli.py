"""Command line entry point: `uv run notelab --help`."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from .data import DataSet


def main() -> None:
    parser = argparse.ArgumentParser(prog="notelab")
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="validate a data set and summarize it")
    check.add_argument("root", type=Path, help="data set directory, e.g. data/fixture")

    args = parser.parse_args()
    match args.command:
        case "check":
            data = DataSet.load(args.root)
            splits = Counter(n.split for n in data.notes)
            layers = Counter(a.layer for t in data.texts.values() for a in t.annotations)
            print(f"{len(data.texts)} texts, {len(data.concepts)} concepts")
            print(f"{layers.total()} annotations: " + ", ".join(f"{l} {k}" for l, k in sorted(layers.items(), key=str)))
            print(f"{len(data.notes)} notes: " + ", ".join(f"{s} {k}" for s, k in sorted(splits.items())))
            problems = data.problems()
            for problem in problems:
                print(problem)
            if problems:
                sys.exit(f"{len(problems)} problems")
