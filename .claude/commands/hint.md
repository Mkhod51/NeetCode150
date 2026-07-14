---
description: Give the next graduated hint for a problem (never the solution)
argument-hint: <file>
allowed-tools: Bash, Read
---
Constraint (CLAUDE.md): hints are graduated and you NEVER skip levels, NEVER
write or fix solution code, and NEVER state the algorithm/approach outright.

Target file: `$ARGUMENTS`

Graduated hint levels (give exactly ONE level per invocation, the next one up):
- **Hint 1** — a clarifying question that nudges their thinking (e.g. "what does
  brute force cost here?", "what are you scanning more than once?").
- **Hint 2** — point to the relevant line, input property, or general concept
  (name a *concept*, not the algorithm — e.g. "think about what you can
  precompute", not "use a prefix sum").
- **Hint 3** — describe the idea in words only. Still no code, no pseudocode.

Steps:
1. Read the file and any docstring notes to understand where they are.
2. Figure out which hint level was already reached earlier in this session for
   THIS problem (start at Hint 1 if none). Never skip a level.
3. Give only that one hint.
4. Tell them which level you just gave, and remind them to record it in the
   docstring **Hints used** field (it must end up an integer 0-3).
5. If they're still stuck after Hint 3, keep asking Socratic questions — do not
   hand them the solution.
