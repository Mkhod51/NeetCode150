---
description: Analyse a solved problem's running time and compare it to the optimal
argument-hint: <file>
allowed-tools: Bash, Read, Edit
---
Constraint (CLAUDE.md): only analyse a problem the human has ALREADY solved.
Explaining the complexity of code they have written is allowed. Never reveal
the optimal complexity, the approach or any code for a problem that is not yet
solved, and never write or improve their solution.

Target file: `$ARGUMENTS`

Steps:

1. Check the problem is solved: run `python3 scripts/check_file.py $ARGUMENTS`.
   - If it FAILS (TODO fields, or the file does not run), STOP. Tell the human
     this command only analyses solved problems, and that revealing the optimal
     now would spoil the exercise. Offer `/hint` instead. Do not state the
     optimal complexity or the approach.

2. Measure the real running time (this benchmarks THEIR code, which is allowed):
   - If the file has no `bench()` function, add a small one at the bottom using
     `helpers.complexity` (pick a generator that matches the method's inputs,
     e.g. `random_ints`, `sorted_ints`, `random_string`; return a tuple from
     `make_input` for multi-argument methods). This is measurement code, not
     solution logic.
   - Run `python3 scripts/benchmark.py $ARGUMENTS` and read the table and the
     estimated growth.

3. Read the human's stated **Time complexity** and **Space complexity** from the
   docstring. Note if the measured growth disagrees with what they wrote (for
   example they wrote O(n) but it scales like O(n^2)), and ask them about it.

4. Compare against the optimal. Because the problem is solved, you may state the
   optimal time and space complexity for it and say whether they matched.
   - If they matched the optimal: say so plainly and stop.
   - If their solution is slower than optimal: name the gap in complexity terms
     only (for example "yours is O(n^2) time, the optimal is O(n)"). Explain in
     one or two sentences, in words, what is costing the extra time. Do NOT
     write or describe the full better algorithm outright. Offer a choice:
     a graduated `/hint` toward the faster idea, or set the docstring
     **Revisit** field to `yes` so they redo it later. Then run
     `python3 scripts/progress.py` if you changed the field.

Never edit their `Solution` code. You are analysing and comparing, not fixing.
