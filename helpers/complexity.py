"""Empirically measure how a function's running time grows with input size.

This is a testing utility, not a solution. It runs code YOU wrote on inputs of
increasing size, times it and estimates the growth (linear, quadratic, and so
on) from the timings. It reveals nothing about any problem's approach; it only
measures the code you already have.

Standard library only. Typical use, after you have solved a problem, inside a
``bench()`` function in your solution file::

    def bench():
        from helpers.complexity import report, random_ints
        report(lambda nums: Solution().your_method(nums), random_ints)

Then run:  python3 scripts/benchmark.py <your-file.py>

``make_input(n)`` returns the argument(s) for one call. Return a tuple for a
multi-argument method, e.g. ``lambda n: (random_ints(n), n // 2)``.
"""
import gc
import math
import random
import time

DEFAULT_SIZES = (250, 500, 1000, 2000, 4000, 8000, 16000)

# Upper edge of each log-log slope bucket, with a human-readable label. A slope
# near p means the time grows like n**p, so p ~= 1 is linear, p ~= 2 quadratic.
_BUCKETS = [
    (0.40, "roughly constant or logarithmic  (~O(1) or O(log n))"),
    (0.85, "sublinear  (~O(sqrt n))"),
    (1.35, "roughly linear  (~O(n) or O(n log n))"),
    (2.35, "roughly quadratic  (~O(n^2))"),
    (3.35, "roughly cubic  (~O(n^3))"),
]
_SUPER = "super-polynomial  (worse than O(n^3), possibly exponential)"


# ---- ready-made input generators ----

def random_ints(n, lo=-10**6, hi=10**6):
    """A list of n random integers."""
    return [random.randint(lo, hi) for _ in range(n)]


def sorted_ints(n):
    """A sorted list of n random integers."""
    return sorted(random_ints(n))


def random_string(n, alphabet="abcdefghijklmnopqrstuvwxyz"):
    """A random string of length n."""
    return "".join(random.choice(alphabet) for _ in range(n))


# ---- measurement ----

def _as_args(value):
    return value if isinstance(value, tuple) else (value,)


def measure(func, make_input, sizes=DEFAULT_SIZES, repeats=3, max_seconds=2.0):
    """Time ``func`` on inputs from ``make_input`` across ``sizes``.

    Returns a list of (n, best_seconds). Building the input is not counted, only
    the call. Stops early once a single call exceeds ``max_seconds`` so a slow
    solution cannot hang the benchmark.
    """
    results = []
    for n in sizes:
        best = math.inf
        for _ in range(repeats):
            args = _as_args(make_input(n))
            gc.disable()
            start = time.perf_counter()
            func(*args)
            elapsed = time.perf_counter() - start
            gc.enable()
            best = min(best, elapsed)
        results.append((n, best))
        if best > max_seconds:
            break
    return results


def _linear_fit(xs, ys):
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if denom == 0:
        return 0.0
    return (n * sxy - sx * sy) / denom


def classify(results):
    """Estimate the growth order from (n, time) points.

    Fits the slope of log(time) against log(n); that slope approximates the
    exponent p in time ~ n**p. Returns {"slope": float|None, "label": str}.
    """
    points = [(n, t) for n, t in results if t > 0 and n > 0]
    if len(points) < 2:
        return {"slope": None,
                "label": "not enough timing data to classify (try larger sizes)"}
    xs = [math.log(n) for n, _ in points]
    ys = [math.log(t) for _, t in points]
    slope = _linear_fit(xs, ys)
    for upper, label in _BUCKETS:
        if slope < upper:
            return {"slope": slope, "label": label}
    return {"slope": slope, "label": _SUPER}


def report(func, make_input, sizes=DEFAULT_SIZES, repeats=3, label=""):
    """Measure, print a table plus the estimated growth, and return the classify dict."""
    results = measure(func, make_input, sizes=sizes, repeats=repeats)
    heading = "Measured running time" + (" for " + label if label else "")
    print(heading)
    print("  {:>10}  {:>12}  {:>8}".format("n", "seconds", "x prev"))
    previous = None
    for n, seconds in results:
        if previous is None or previous == 0:
            factor = "-"
        else:
            factor = "{:.1f}x".format(seconds / previous)
        print("  {:>10}  {:>12.6f}  {:>8}".format(n, seconds, factor))
        previous = seconds
    verdict = classify(results)
    if verdict["slope"] is None:
        print(verdict["label"])
    else:
        print("Empirical growth: {}  (log-log slope ~= {:.2f})".format(
            verdict["label"], verdict["slope"]))
    return verdict


if __name__ == "__main__":
    # Self-test: a linear loop should classify below the quadratic threshold, a
    # nested loop above it.
    def linear(xs):
        total = 0
        for x in xs:
            total += x
        return total

    def quadratic(xs):
        count = 0
        for a in xs:
            for b in xs:
                if a == b:
                    count += 1
        return count

    lin = classify(measure(linear, random_ints, sizes=(2000, 4000, 8000, 16000)))
    quad = classify(measure(quadratic, random_ints, sizes=(100, 200, 400, 800)))
    print("linear ->", lin)
    print("quadratic ->", quad)
    assert lin["slope"] is not None and lin["slope"] < 1.35, lin
    assert quad["slope"] is not None and quad["slope"] >= 1.35, quad
    print("helpers.complexity self-test passed.")
