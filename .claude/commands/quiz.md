---
description: 5 pattern-recognition questions from problems you've solved
argument-hint: "[category]"
allowed-tools: Bash, Read
---
Constraint (CLAUDE.md): draw questions ONLY from already-solved problems;
quizzing on solved patterns is allowed. Never reveal anything about an unsolved
problem.

Optional category filter: `$ARGUMENTS` (a category folder name, or empty for all).

Steps:
1. Determine which problems are solved: run `python3 scripts/progress.py` and
   use the checked `[x]` items (optionally filtered to the `$ARGUMENTS`
   category). If there aren't enough solved problems yet, say so and quiz on
   what's available.
2. Read the docstrings (Pattern, Key insight) of those solved files for material.
3. Ask **5** short pattern-recognition questions, ONE at a time. Examples:
   "Which pattern solves 'find if any value repeats'?", "You see a sorted array
   and need a pair summing to target — what technique?", "Given this key insight,
   which problem was it?".
4. After the human attempts each question, reveal the answer, then move to the
   next. Do not dump all answers at once.
5. Keep it to solved material only — this is recall practice, not new teaching.
