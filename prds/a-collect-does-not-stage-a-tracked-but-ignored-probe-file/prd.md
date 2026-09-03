---
state: done
origin: requested
priority: 85
complexity: 6
blast-radius:
actual: 0.08h
---

# A collect does not stage a tracked-but-ignored probe file

<The request, for an analyst who knows the codebase but not this conversation:
what exists at the end and why, what must not change, pointers to files and
prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
2337:            git_out(root, "add", "-f", "--", *p["add"])
dirty_paths() sees it: 'tracked'
no `-f`: collect.git_out(..., "add", ...) raised: git add failed in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/repro-tracked-ignored-0kl5gu17: The following paths are ignored by one of your .gitignore files:
prds/foo/probe
hint: Use -f if you really want to add them.
hint: Disable this message with "git config set advice.addIgnoredFile false"
staged after the fixed call (`-f`): True
PASS: `git_out(root, "add", "-f", "--", *p["add"])` — collect.py:2337 — stages the tracked-but-ignored probe file that the unpatched call refused
