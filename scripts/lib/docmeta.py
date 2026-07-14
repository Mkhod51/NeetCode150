"""Docstring parsing and solution-file running for the tooling scripts.

Not a solution file and not scanned as one. Parses the metadata docstring at
the top of a solution file and runs solution files as subprocesses. Contains
no algorithmic content.
"""
import ast
import datetime
import pathlib
import re
import subprocess
import sys

# Trailing template annotation like "2        (must end up as an integer 0-3)".
# Real values never contain two-or-more spaces immediately before a "(", so this
# only strips the alignment notes the template ships with — not titles such as
# "Pow(x, n)" or a hand-written "O(n)" complexity.
_ANNOTATION = re.compile(r"\s{2,}\(.*\)\s*$")

# Canonical docstring field labels, in the order the template lists them.
FIELDS = [
    "Problem",
    "Link",
    "Category",
    "Difficulty",
    "Pattern",
    "Key insight",
    "Where I got stuck",
    "Hints used",
    "Time complexity",
    "Space complexity",
    "Date solved",
    "Revisit",
]

# Fields new_problem.py pre-fills; the rest stay "TODO" until the human solves.
PREFILLED_FIELDS = ["Problem", "Link", "Category", "Difficulty"]

TODO = "TODO"


def repo_root():
    """Repo root is two levels up from this file (scripts/lib/ -> repo)."""
    return pathlib.Path(__file__).resolve().parents[2]


def read_docstring(path):
    """Return the module-level docstring of a Python file, or '' if none."""
    src = pathlib.Path(path).read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return ""
    return ast.get_docstring(tree) or ""


def parse_fields(path):
    """Parse 'Label: value' lines from a file's module docstring.

    Returns {label: value} for every recognised label present. Values keep
    any trailing inline note (e.g. the '(must end up ...)' hints) stripped off
    only of surrounding whitespace.
    """
    doc = read_docstring(path)
    found = {}
    for raw in doc.splitlines():
        line = raw.strip()
        for field in FIELDS:
            prefix = field + ":"
            if line.startswith(prefix):
                value = line[len(prefix):]
                value = _ANNOTATION.sub("", value).strip()
                found[field] = value
                break
    return found


def missing_or_todo(fields):
    """Return the list of canonical fields that are absent or still 'TODO'."""
    bad = []
    for field in FIELDS:
        value = fields.get(field)
        if value is None or value == "" or TODO in value:
            bad.append(field)
    return bad


def is_solved(path):
    """A file is 'solved' when no field is missing/TODO and it runs clean."""
    fields = parse_fields(path)
    if missing_or_todo(fields):
        return False
    code, _ = run_file(path)
    return code == 0


def run_file(path, timeout=60):
    """Run a solution file as a subprocess from the repo root.

    Returns (exit_code, combined_stdout_stderr). A timeout or crash yields a
    non-zero code so callers can treat it as a failure.
    """
    path = pathlib.Path(path).resolve()
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(repo_root()),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return 1, "TIMEOUT: file did not finish within {}s".format(timeout)
    return proc.returncode, proc.stdout + proc.stderr


def parse_date(value):
    """Parse a YYYY-MM-DD string into a date, or return None if invalid."""
    try:
        return datetime.datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None
