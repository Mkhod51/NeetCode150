#!/usr/bin/env python3
"""Benchmark a solution file's running time across growing input sizes.

Imports the file and calls its ``bench()`` function, which you write using
helpers.complexity (see that module's docstring). This measures YOUR code and
reveals nothing about any problem's approach, so it is safe to run any time you
have a working solution.

Usage:
  python3 scripts/benchmark.py <path-to-solution.py>

If the file has no bench() yet, this prints a template to copy in.
"""
import argparse
import importlib.util
import pathlib
import sys

EXAMPLE = '''\
def bench():
    # measures YOUR solution; run: python3 scripts/benchmark.py <this file>
    from helpers.complexity import report, random_ints
    report(lambda nums: Solution().your_method(nums), random_ints)
'''


def load_solution_module(path):
    """Import a solution file by path (handles names starting with digits)."""
    path = pathlib.Path(path).resolve()
    spec = importlib.util.spec_from_file_location("solution_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Benchmark a solution file's running time across input sizes.")
    parser.add_argument("path", help="path to the solution .py file")
    args = parser.parse_args(argv)

    path = pathlib.Path(args.path)
    if not path.is_file():
        print("error: no such file: {}".format(args.path), file=sys.stderr)
        return 2

    module = load_solution_module(path)
    if not hasattr(module, "bench") or not callable(module.bench):
        print("{} has no bench() function yet.".format(path))
        print("Add one to the file (adjust the method name and input), then re-run:\n")
        print(EXAMPLE)
        return 1

    module.bench()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
