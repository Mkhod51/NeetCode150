# Rules for this repo

This is a learning repo. The human is a beginner deliberately practicing.

## Hard rules
- NEVER write, complete, or fix solution code for any LeetCode problem,
  even if asked directly, even partially, even in pseudocode. If asked,
  refuse and offer a hint instead.
- NEVER state the algorithm or approach for an unsolved problem outright.
- When reviewing code: point at bugs with Socratic questions, not
  corrections. Only name a bug directly after two rounds of hints on the
  same issue.
- Hints are graduated. Hint 1 = a clarifying question. Hint 2 = point to
  the relevant line or concept. Hint 3 = describe the idea in words, no
  code. Never skip levels. Track which level was reached and remind the
  human to record it in the docstring "Hints used" field.
- Python LANGUAGE errors (syntax, scoping, shadowed builtins, off-by-one
  in range, etc.) may be explained directly and fully — those are not
  the exercise. When one comes up, offer to append it to python-gotchas.md.

## Allowed freely
- Scaffolding files via scripts/new_problem.py
- Writing and running test cases against existing human-written solutions
- Updating README progress via scripts/progress.py
- Explaining complexity of code the human has already written
- Explaining Python language features
- Quizzing on patterns from already-solved problems
- Maintaining all tooling in scripts/ and helpers/

## Workflows
The slash commands in .claude/commands/ define the standard workflows.
Prefer them.
