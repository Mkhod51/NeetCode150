#!/usr/bin/env python3
"""Scaffold a new solution file from the template.

Usage:
  python scripts/new_problem.py <category> <leetcode-number> <slug>

Example:
  python scripts/new_problem.py arrays-hashing 1 two-sum
    -> creates arrays-hashing/0001-two-sum.py

Copies templates/problem-template.py into the category folder as
{NNNN}-{slug}.py, pre-filling only the Problem / Link / Category / Difficulty
fields (difficulty and title are read from the README checklist). It never
writes solution code or approach hints, and refuses to overwrite an existing
file. Standard library only.
"""
import argparse
import re

from lib import docmeta as meta
from lib import neetcode150 as nc

TEMPLATE = "templates/problem-template.py"

# Matches a README checklist line:
#   - [ ] 0001 Two Sum (Easy) — arrays-hashing/0001-two-sum.py
_CHECKLIST = re.compile(
    r"^- \[.\] (?P<num>\d{4}) (?P<title>.+) \((?P<diff>Easy|Medium|Hard)\) — (?P<path>\S+)\s*$")


def lookup_from_readme(number):
    """Return (title, difficulty) for a zero-padded number from the README.

    Returns (None, None) if the number is not in the checklist.
    """
    readme = meta.repo_root() / "README.md"
    if not readme.is_file():
        return None, None
    for line in readme.read_text(encoding="utf-8").splitlines():
        m = _CHECKLIST.match(line)
        if m and m.group("num") == number:
            return m.group("title"), m.group("diff")
    return None, None


def title_from_slug(slug):
    return slug.replace("-", " ").title()


def time_limit_note(difficulty):
    if difficulty == "Easy":
        return "Time limit: 25 minutes (Easy)."
    if difficulty in ("Medium", "Hard"):
        return "Time limit: 40 minutes ({}).".format(difficulty)
    return "Time limit: 25 min for Easy, 40 min for Medium/Hard."


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Scaffold a new solution file from the template.")
    parser.add_argument("category", help="category folder, e.g. arrays-hashing")
    parser.add_argument("number", help="LeetCode problem number, e.g. 1")
    parser.add_argument("slug", help="LeetCode slug, e.g. two-sum")
    args = parser.parse_args(argv)

    valid = [folder for folder, _ in nc.CATEGORY_ORDER]
    if args.category not in valid:
        parser.error("unknown category '{}'. Valid: {}".format(
            args.category, ", ".join(valid)))

    try:
        number = "{:04d}".format(int(args.number))
    except ValueError:
        parser.error("number must be an integer, got '{}'".format(args.number))

    slug = args.slug.strip().lower()
    filename = "{}-{}.py".format(number, slug)
    target = meta.repo_root() / args.category / filename
    if target.exists():
        parser.error("refusing to overwrite existing file: {}".format(
            target.relative_to(meta.repo_root())))

    title, difficulty = lookup_from_readme(number)
    if title is None:
        title = title_from_slug(slug)
        print("note: {} not found in README checklist; "
              "using derived title and leaving Difficulty as TODO.".format(number))
    if difficulty is None:
        difficulty = "TODO"

    template_text = (meta.repo_root() / TEMPLATE).read_text(encoding="utf-8")
    filled = (template_text
              .replace("{NUMBER} {TITLE}", "{} {}".format(number, title))
              .replace("{LEETCODE_URL}", "https://leetcode.com/problems/{}/".format(slug))
              .replace("{CATEGORY}", nc.display_name(args.category))
              .replace("{DIFFICULTY}", difficulty))

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(filled, encoding="utf-8")

    rel = target.relative_to(meta.repo_root())
    print("Created {}".format(rel))
    print(time_limit_note(difficulty))
    print("Read the problem on LeetCode yourself, then solve it by hand. "
          "Ask for a hint (/hint) only if you get stuck.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
