"""Internal shared library for the tooling scripts.

The entry-point scripts in scripts/ import this as ``from lib import ...``,
which resolves because Python puts a script's own directory (scripts/) on
sys.path when run as ``python3 scripts/<name>.py`` from the repo root.

Holds problem metadata and docstring parsing — never solution code.
"""
