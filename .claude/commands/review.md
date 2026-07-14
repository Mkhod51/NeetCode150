---
description: Review a solved file with edge-case tests and Socratic questions
argument-hint: <file>
allowed-tools: Bash, Read, Edit
---
Constraint (CLAUDE.md): point at bugs with Socratic QUESTIONS, never
corrections; never write or fix the human's solution code. Only name a bug
directly after two rounds of hints on the same issue.

Target file: `$ARGUMENTS`

Steps:
1. Read the file. Check the **Time complexity** and **Space complexity** claims
   in the docstring against the code the human actually wrote. If a claim looks
   wrong, ask a question that leads them to re-examine it — don't just correct
   it.
2. Add **exactly 3 edge-case asserts** to the `if __name__ == "__main__":`
   block (e.g. empty input, single element, duplicates/negatives, max bounds).
   Edit ONLY the test block — never the `Solution` class or their algorithm.
3. Run the file: `python3 $ARGUMENTS`
4. Report the outcome:
   - If asserts pass, say so and note the complexity discussion.
   - If an assert fails, present the failing case as a QUESTION ("what happens
     when the input is empty?"), not a fix. Give a second Socratic nudge if
     needed. Only after two rounds may you name the bug directly.
5. Never edit their solution to make tests pass.
