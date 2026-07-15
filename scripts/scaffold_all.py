#!/usr/bin/env python3
"""Create a scaffold file for every NeetCode 150 problem at once.

Saves you from typing a category, number and slug for each problem. It copies
the template into each topic folder with the Problem / Link / Category /
Difficulty fields pre-filled from the canonical list (lib/neetcode150.py), so
you just open a file by name and solve it. No solution code is written.

Existing files are never overwritten, so it is safe to re-run: it only fills in
the ones that are missing. Standard library only.

Usage:
  python3 scripts/scaffold_all.py            # create every missing scaffold
  python3 scripts/scaffold_all.py --dry-run  # list what would be created
"""
import argparse

from lib import docmeta as meta
from lib import neetcode150 as nc

import new_problem


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Scaffold a file for every NeetCode 150 problem (skips existing).")
    parser.add_argument("--dry-run", action="store_true",
                        help="show what would be created without writing anything")
    args = parser.parse_args(argv)

    created = 0
    skipped = 0
    for p in nc.problems():
        target = meta.repo_root() / p["category"] / p["filename"]
        if target.exists():
            skipped += 1
            continue
        rel = target.relative_to(meta.repo_root())
        if args.dry_run:
            print("would create {}".format(rel))
            created += 1
            continue
        number = "{:04d}".format(p["number"])
        content = new_problem.render_template(
            number, p["title"], p["slug"], p["category"], p["difficulty"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        created += 1

    verb = "would create" if args.dry_run else "created"
    print("\n{} {} file(s), skipped {} that already existed.".format(
        verb, created, skipped))
    if not args.dry_run and created:
        print("Open any file by name and solve it, then run /done on it. "
              "Empty scaffolds stay uncommitted until you finish them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
