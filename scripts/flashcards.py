#!/usr/bin/env python3
"""Export solved problems as an Anki-importable CSV (front,back).

Front = the problem plus "Which pattern?"; back = the pattern and key insight.
Only problems that pass the solved check (no TODO fields, runs clean) are
included. Standard library only.

Usage:
  python scripts/flashcards.py            # writes flashcards.csv
  python scripts/flashcards.py --out cards.csv
  python scripts/flashcards.py --out -    # write CSV to stdout
"""
import argparse
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import neetcode150 as nc  # noqa: E402
import _docmeta as meta  # noqa: E402


def solved_cards():
    """Yield (front, back) tuples for every solved problem, in README order."""
    for p in nc.problems():
        path = meta.repo_root() / p["category"] / p["filename"]
        if not path.is_file() or not meta.is_solved(path):
            continue
        fields = meta.parse_fields(path)
        problem = fields.get("Problem", p["title"])
        pattern = fields.get("Pattern", "")
        insight = fields.get("Key insight", "")
        front = "{}\n\nWhich pattern applies, and why?".format(problem)
        back = "Pattern: {}\nKey insight: {}".format(pattern, insight)
        yield front, back


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Export solved problems as an Anki-importable CSV (front,back).")
    parser.add_argument(
        "--out", default="flashcards.csv",
        help="output CSV path, or '-' for stdout (default: flashcards.csv)")
    args = parser.parse_args(argv)

    cards = list(solved_cards())

    if args.out == "-":
        writer = csv.writer(sys.stdout)
        writer.writerow(["front", "back"])
        writer.writerows(cards)
        return 0

    out_path = pathlib.Path(args.out)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["front", "back"])
        writer.writerows(cards)
    print("Wrote {} card(s) to {}".format(len(cards), out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
