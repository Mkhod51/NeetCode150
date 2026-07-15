#!/usr/bin/env python3
"""Scaffold a new solution file from the template.

Usage:
  python scripts/new_problem.py <category> <leetcode-number> <slug>

Example:
  python scripts/new_problem.py arrays-hashing 1 two-sum
    -> creates arrays-hashing/0001-two-sum.py

Copies templates/problem-template.py into the category folder as
{NNNN}-{slug}.py, pre-filling only the Problem / Link / Category / Difficulty
fields (title and difficulty come from the canonical list in
lib/neetcode150.py). It never writes solution code or approach hints, and
refuses to overwrite an existing file. Standard library only.
"""
import argparse

from lib import docmeta as meta
from lib import neetcode150 as nc

TEMPLATE = "templates/problem-template.py"


def lookup_canonical(number):
    """Return (title, difficulty) for a LeetCode number from the canonical list.

    Returns (None, None) if the number is not one of the NeetCode 150.
    """
    for p in nc.problems():
        if p["number"] == number:
            return p["title"], p["difficulty"]
    return None, None


def render_template(number, title, slug, category_folder, difficulty):
    """Return the filled template text for one problem (writes nothing).

    ``number`` is the zero-padded string, e.g. "0271". Only the four
    pre-fill fields are set; the rest stay TODO. No solution code.
    """
    template_text = (meta.repo_root() / TEMPLATE).read_text(encoding="utf-8")
    return (template_text
            .replace("{NUMBER} {TITLE}", "{} {}".format(number, title))
            .replace("{LEETCODE_URL}", "https://leetcode.com/problems/{}/".format(slug))
            .replace("{CATEGORY}", nc.display_name(category_folder))
            .replace("{DIFFICULTY}", difficulty))


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
        number_int = int(args.number)
    except ValueError:
        parser.error("number must be an integer, got '{}'".format(args.number))
    number = "{:04d}".format(number_int)

    slug = args.slug.strip().lower()
    filename = "{}-{}.py".format(number, slug)
    target = meta.repo_root() / args.category / filename
    if target.exists():
        parser.error("refusing to overwrite existing file: {}".format(
            target.relative_to(meta.repo_root())))

    title, difficulty = lookup_canonical(number_int)
    if title is None:
        title = title_from_slug(slug)
        print("note: {} is not in the canonical NeetCode 150 list; "
              "using derived title and leaving Difficulty as TODO.".format(number))
    if difficulty is None:
        difficulty = "TODO"

    filled = render_template(number, title, slug, args.category, difficulty)

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
