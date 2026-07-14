---
description: Finalize a solved problem — fill notes, validate, commit
argument-hint: <file>
allowed-tools: Bash, Read, Edit
---
Constraint (CLAUDE.md): you are only recording the human's own work — never
write, complete, or improve their solution code here.

Target file: `$ARGUMENTS`

Steps:
1. Read the file's docstring. For EACH field still set to `TODO`, ask the human
   for the value, one at a time, and record their answer (do not invent values):
   Pattern, Key insight, Where I got stuck, Hints used (integer 0-3),
   Time complexity, Space complexity, Revisit (yes/no).
2. Set **Date solved** to today's date in `YYYY-MM-DD` format.
3. Remove the `(must end up ...)` alignment notes if the human left them.
4. Validate with the honesty gate:

   `python3 scripts/check_file.py $ARGUMENTS`

   If it fails, fix the offending docstring field (ask the human) and re-run.
   Do not touch their solution code.
5. Regenerate progress: `python3 scripts/progress.py`
6. Stage and commit just this file plus the README:

   `git add $ARGUMENTS README.md && git commit -m "{NNNN} {Title}"`

   where {NNNN} is the zero-padded number and {Title} is the problem title from
   the docstring. The pre-commit hook re-runs the honesty gate as a backstop.
