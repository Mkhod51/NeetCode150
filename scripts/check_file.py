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


def check(path):
    """Return a list of human-readable failure strings (empty == pass)."""
    failures = []
    fields = meta.parse_fields(path)

    for field in meta.FIELDS:
        value = fields.get(field)
        if value is None:
            failures.append("missing docstring field: '{}'".format(field))
        elif value == "" or meta.TODO in value:
            failures.append("field '{}' is still TODO/empty".format(field))

    hints = fields.get("Hints used", "")
    if hints and meta.TODO not in hints:
        try:
            n = int(hints)
            if not 0 <= n <= 3:
                failures.append("'Hints used' must be 0-3, got {!r}".format(hints))
        except ValueError:
            failures.append("'Hints used' must be an integer 0-3, got {!r}".format(hints))

    date_val = fields.get("Date solved", "")
    if date_val and meta.TODO not in date_val:
        if meta.parse_date(date_val) is None:
            failures.append("'Date solved' must be YYYY-MM-DD, got {!r}".format(date_val))

    revisit = fields.get("Revisit", "")
    if revisit and meta.TODO not in revisit:
        if revisit.strip().lower() not in ("yes", "no"):
            failures.append("'Revisit' must be 'yes' or 'no', got {!r}".format(revisit))

    code, output = meta.run_file(path)
    if code != 0:
        detail = output.strip() or "(no output)"
        failures.append("file did not run clean (exit {}):\n    {}".format(
            code, detail.replace("\n", "\n    ")))

    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate a single solution file (the honesty gate).")
    parser.add_argument("path", help="path to the solution .py file")
    args = parser.parse_args(argv)

    path = pathlib.Path(args.path)
    if not path.is_file():
        print("error: no such file: {}".format(args.path), file=sys.stderr)
        return 2

    failures = check(path)
    if failures:
        print("FAIL: {}".format(path))
        for f in failures:
            print("  - {}".format(f))
        return 1
    print("PASS: {}".format(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
