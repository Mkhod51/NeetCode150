#!/usr/bin/env python3
"""Validate a single solution file — the honesty gate.

Usage:
  python scripts/check_file.py <path>

Checks that every docstring field is present and no longer "TODO", that
"Hints used" is an integer 0-3, "Date solved" is a valid YYYY-MM-DD date,
"Revisit" is yes/no, and that the file runs (asserts pass) with exit code 0.
Exits 0 when everything passes, non-zero with a list of failures otherwise.
This script never inspects or writes solution logic. Standard library only.
"""
import argparse
import pathlib
import sys

from lib import docmeta as meta


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate a single solution file (the honesty gate).")
    parser.add_argument("path", help="path to the solution .py file")
    args = parser.parse_args(argv)

    path = pathlib.Path(args.path)
    if not path.is_file():
        print("error: no such file: {}".format(args.path), file=sys.stderr)
        return 2

    failures = meta.validate(path)
    if failures:
        print("FAIL: {}".format(path))
        for f in failures:
            print("  - {}".format(f))
        return 1
    print("PASS: {}".format(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
