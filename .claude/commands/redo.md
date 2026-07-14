---
description: Redo the oldest problem due in the revisit queue, from scratch
allowed-tools: Bash, Read, Edit
---
Constraint (CLAUDE.md): describe ONLY the problem statement — no approach, no
pattern, no hint about the original solution. Never write solution code.

Steps:
1. Run `python3 scripts/progress.py` and read the **Revisit queue**. Pick the
   single oldest entry (top of the queue). If the queue is empty, say so and stop.
2. Tell the human which problem it is and restate ONLY the problem statement in
   your own words (inputs, outputs, constraints). Do NOT mention the pattern,
   the approach, or anything from their original file.
3. Have them solve it fresh — from a blank file — at:
   `redo/{NNNN}-{slug}-redo-{YYYYMMDD}.py`
   (scaffold it with `python3 scripts/new_problem.py`-style header if helpful,
   but the human writes all the code). redo/ is excluded from the honesty hook.
4. When they're done, `diff` the redo file against the original
   `{category}/{NNNN}-{slug}.py` and discuss what changed — faster? cleaner?
   different bug? Ask questions; don't rewrite their code.
5. If the redo was clean (they solved it comfortably, no hints), update the
   ORIGINAL file's docstring: set **Revisit** to `no` and **Date solved** to
   today (`YYYY-MM-DD`), then run `python3 scripts/progress.py`.
