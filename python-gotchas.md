# Python gotchas

A running reference of Python *language* traps (not algorithm notes). These are
fair game to explain fully — they're not the exercise. Add more with `/gotcha`.

---

**`enumerate` yields `(index, value)`, in that order.**
Easy to swap them by accident.
```python
for i, x in enumerate(nums):   # right: index first, value second
    ...
for x, i in enumerate(nums):   # wrong: x is the index, i is the value
    ...
```

**Don't shadow builtins (`dict`, `list`, `set`, `str`, `sum`, `id`, ...).**
Naming a variable `list` or `dict` rebinds the type, and later calls blow up
with confusing errors like `'type' object does not support item assignment` or
`'list' object is not callable`.
```python
dict = {}          # wrong: now `dict(...)` is broken for the rest of the scope
counts = {}         # right
```

**`{}` is an empty dict, not an empty set.** Use `set()` for an empty set.
```python
seen = {}          # this is a dict
seen = set()       # this is a set
seen = {1, 2, 3}   # non-empty set literal is fine
```

**A name assigned anywhere in a function is local to the WHOLE function.**
Even if you read it before that assignment, Python treats it as local, giving
`UnboundLocalError`. To rebind a variable from an outer scope, declare
`nonlocal` (enclosing function) or `global` (module level).
```python
count = 0
def bump():
    count += 1          # UnboundLocalError: `count` is local because it's assigned here
def bump_ok():
    global count
    count += 1          # right
```

**`range(n)` excludes `n`.** It goes `0 .. n-1`. `range(a, b)` is `a .. b-1`.
```python
list(range(3))      # [0, 1, 2]  — not [0, 1, 2, 3]
```

**`dict[int, int]`-style annotations need Python 3.9+.**
On older versions (or to be safe), add `from __future__ import annotations` at
the top of the file, or use `typing.Dict[int, int]`.
```python
from __future__ import annotations   # lets you write dict[int, int] on 3.7/3.8
def f(counts: dict[int, int]) -> None: ...
```

**Membership: `set`/`dict` lookup is O(1) average; `list`/`str` scan is O(n).**
`x in a_set` is fast; `x in a_list` walks the whole list. Converting a list to a
set before repeated membership tests is often the whole trick to a speedup.
```python
if x in big_list:   # O(n) each time
    ...
lookup = set(big_list)
if x in lookup:     # O(1) average
    ...
```
