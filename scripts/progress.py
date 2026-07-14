#!/usr/bin/env python3
"""Regenerate the README PROGRESS and REVISIT QUEUE sections.

Scans every category folder, decides which problems are solved, and rewrites
the two machine-owned regions of the README (between the BEGIN/END markers),
leaving all other prose untouched. Also prints a terminal summary.

A problem counts as SOLVED when its file exists, has no remaining "TODO"
docstring fields, and runs (as a subprocess) with exit code 0.

Revisit due date = Date solved + 3 days when Hints used > 0 or Revisit is yes,
otherwise Date solved + 14 days. The queue shows entries due today or earlier,
oldest first.

This script never writes solution code. Standard library only.

Usage:
  python scripts/progress.py            # regenerate README + print summary
  python scripts/progress.py --check    # verify README is in sync; do not write
"""
import argparse
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import neetcode150 as nc  # noqa: E402
import _docmeta as meta  # noqa: E402

PROGRESS_BEGIN = "<!-- PROGRESS:BEGIN -->"
PROGRESS_END = "<!-- PROGRESS:END -->"
REVISIT_BEGIN = "<!-- REVISIT:BEGIN -->"
REVISIT_END = "<!-- REVISIT:END -->"

BAR_WIDTH = 10


def progress_bar(solved, total):
    filled = int(round((solved / total) * BAR_WIDTH)) if total else 0
    filled = max(0, min(BAR_WIDTH, filled))
    return "█" * filled + "-" * (BAR_WIDTH - filled)


def canonical_filenames():
    """Set of '{folder}/{filename}' strings for the canonical 150."""
    return {"{}/{}".format(p["category"], p["filename"]) for p in nc.problems()}


def extra_files(folder):
    """Return non-canonical *.py files present in a category folder, sorted."""
    root = meta.repo_root() / folder
    if not root.is_dir():
        return []
    canon = {p["filename"] for p in nc.problems() if p["category"] == folder}
    extras = [f for f in root.glob("*.py") if f.name not in canon]
    return sorted(extras, key=lambda f: f.name)


def _extra_meta(path):
    """Derive (number, title, difficulty) for a non-canonical file."""
    fields = meta.parse_fields(path)
    stem = path.stem  # e.g. 9999-test-problem
    number = stem.split("-", 1)[0]
    problem = fields.get("Problem", "")
    title = problem
    if problem[:len(number)] == number:
        title = problem[len(number):].strip()
    if not title or meta.TODO in title:
        title = stem.split("-", 1)[-1].replace("-", " ").title()
    difficulty = fields.get("Difficulty", "") or "?"
    if meta.TODO in difficulty:
        difficulty = "?"
    return number, title, difficulty


def gather():
    """Build the per-category view used for rendering and the summary.

    Returns a list of dicts: {folder, name, rows, solved, total}
    where each row is {mark, number, title, difficulty, path, solved}.
    """
    categories = []
    for folder, name, items in nc.problems_by_category():
        rows = []
        for p in items:
            path = meta.repo_root() / p["category"] / p["filename"]
            solved = path.is_file() and meta.is_solved(path)
            rows.append({
                "mark": "x" if solved else " ",
                "number": "{:04d}".format(p["number"]),
                "title": p["title"],
                "difficulty": p["difficulty"],
                "path": "{}/{}".format(p["category"], p["filename"]),
                "solved": solved,
            })
        for f in extra_files(folder):
            solved = meta.is_solved(f)
            number, title, difficulty = _extra_meta(f)
            rows.append({
                "mark": "x" if solved else " ",
                "number": number,
                "title": title,
                "difficulty": difficulty,
                "path": "{}/{}".format(folder, f.name),
                "solved": solved,
            })
        solved_count = sum(1 for r in rows if r["solved"])
        categories.append({
            "folder": folder,
            "name": name,
            "rows": rows,
            "solved": solved_count,
            "total": len(rows),
        })
    return categories


def render_progress(categories):
    lines = [PROGRESS_BEGIN, ""]
    for cat in categories:
        bar = progress_bar(cat["solved"], cat["total"])
        lines.append("### {}  [{}] {}/{}".format(
            cat["name"], bar, cat["solved"], cat["total"]))
        for r in cat["rows"]:
            lines.append("- [{}] {} {} ({}) — {}".format(
                r["mark"], r["number"], r["title"], r["difficulty"], r["path"]))
        lines.append("")
    lines.append(PROGRESS_END)
    return "\n".join(lines)


def revisit_entries(categories, today=None):
    """Return solved entries whose revisit due date is today or earlier."""
    today = today or datetime.date.today()
    entries = []
    for cat in categories:
        for r in cat["rows"]:
            if not r["solved"]:
                continue
            path = meta.repo_root() / r["path"]
            fields = meta.parse_fields(path)
            solved_date = meta.parse_date(fields.get("Date solved", ""))
            if solved_date is None:
                continue
            try:
                hints = int(fields.get("Hints used", "0"))
            except ValueError:
                hints = 0
            revisit_yes = fields.get("Revisit", "").strip().lower() == "yes"
            span = 3 if (hints > 0 or revisit_yes) else 14
            due = solved_date + datetime.timedelta(days=span)
            if due <= today:
                entries.append({
                    "due": due,
                    "solved_date": solved_date,
                    "number": r["number"],
                    "title": r["title"],
                    "path": r["path"],
                })
    entries.sort(key=lambda e: (e["due"], e["number"]))
    return entries


def render_revisit(categories, today=None):
    entries = revisit_entries(categories, today=today)
    lines = [REVISIT_BEGIN, ""]
    if not entries:
        lines.append("_Nothing due for revisit. Keep going!_")
    else:
        for e in entries:
            lines.append("- {} {} — {} (due {}, solved {})".format(
                e["number"], e["title"], e["path"],
                e["due"].isoformat(), e["solved_date"].isoformat()))
    lines.append("")
    lines.append(REVISIT_END)
    return "\n".join(lines)


def replace_region(text, begin, end, new_block):
    start = text.find(begin)
    stop = text.find(end)
    if start == -1 or stop == -1 or stop < start:
        raise SystemExit(
            "README is missing the {}/{} markers.".format(begin, end))
    return text[:start] + new_block + text[stop + len(end):]


def build_readme(readme_text, categories, today=None):
    updated = replace_region(
        readme_text, PROGRESS_BEGIN, PROGRESS_END, render_progress(categories))
    updated = replace_region(
        updated, REVISIT_BEGIN, REVISIT_END, render_revisit(categories, today))
    return updated


def print_summary(categories, today=None):
    total_solved = sum(c["solved"] for c in categories)
    grand_total = sum(c["total"] for c in categories)
    print("Progress summary")
    print("================")
    for cat in categories:
        print("  {:<26} {}/{}".format(cat["name"], cat["solved"], cat["total"]))
    print("  {:<26} {}/{}".format("TOTAL", total_solved, grand_total))
    entries = revisit_entries(categories, today=today)
    print()
    if not entries:
        print("Revisit queue: empty.")
    else:
        print("Revisit queue ({} due):".format(len(entries)))
        for e in entries:
            print("  {} {} (due {})".format(e["number"], e["title"], e["due"].isoformat()))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Regenerate the README PROGRESS and REVISIT QUEUE sections.")
    parser.add_argument(
        "--check", action="store_true",
        help="verify the README is in sync without writing; exit nonzero if stale")
    args = parser.parse_args(argv)

    readme_path = meta.repo_root() / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8")
    categories = gather()
    updated = build_readme(readme_text, categories)

    if args.check:
        if updated != readme_text:
            print("README is OUT OF SYNC. Run: python scripts/progress.py",
                  file=sys.stderr)
            return 1
        print("README PROGRESS/REVISIT sections are in sync.")
        return 0

    readme_path.write_text(updated, encoding="utf-8")
    print_summary(categories)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
