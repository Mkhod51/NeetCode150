#!/usr/bin/env python3
"""Install the tracked pre-commit hook into .git/hooks.

Symlinks hooks/pre-commit to .git/hooks/pre-commit (falling back to a copy if
the platform can't symlink) and makes it executable. Safe to re-run. Standard
library only.

Usage:
  python scripts/install_hooks.py
"""
import argparse
import os
import pathlib
import shutil
import stat
import sys

EXEC_BITS = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH


def make_executable(path):
    path = pathlib.Path(path)
    path.chmod(path.stat().st_mode | EXEC_BITS)


def main(argv=None):
    argparse.ArgumentParser(
        description="Install the pre-commit hook into .git/hooks.").parse_args(argv)

    root = pathlib.Path(__file__).resolve().parents[1]
    src = root / "hooks" / "pre-commit"
    git_dir = root / ".git"

    if not src.is_file():
        print("error: {} not found".format(src), file=sys.stderr)
        return 1
    if not git_dir.is_dir():
        print("error: {} is not a git repository".format(root), file=sys.stderr)
        return 1

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    dest = hooks_dir / "pre-commit"

    if dest.exists() or dest.is_symlink():
        dest.unlink()

    # Make the tracked source executable; git follows the symlink to it.
    make_executable(src)

    rel = os.path.relpath(src, hooks_dir)
    try:
        dest.symlink_to(rel)
        how = "symlink -> {}".format(rel)
    except (OSError, NotImplementedError):
        shutil.copyfile(src, dest)
        make_executable(dest)
        how = "copy"

    print("Installed .git/hooks/pre-commit ({}).".format(how))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
