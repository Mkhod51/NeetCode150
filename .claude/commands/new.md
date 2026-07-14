---
description: Scaffold a new NeetCode problem file and start the timer
argument-hint: <category> <number> <slug>
allowed-tools: Bash(python3 scripts/new_problem.py:*)
---
Constraint (CLAUDE.md): scaffold only — never reveal the pattern, approach, data
structure, or any hint about how to solve it.

Do exactly this:

1. Run the scaffolder:

   `python3 scripts/new_problem.py $ARGUMENTS`

2. Confirm the created file path back to the human (from the script output).
3. Tell them their time limit: **25 min for Easy, 40 min for Medium/Hard**
   (use whatever the script reported).
4. Remind them to open the problem on LeetCode and solve it by hand.
5. Say NOTHING about the solution — no pattern name, no algorithm, no
   "you'll want a hash map", nothing. If they want help, they run `/hint`.
