---
state: done
origin: requested
priority: 0
complexity: 29
blast-radius: high
workflow: probe-then-spec
actual: 13.49h
commit: dca5ce2 f74bdfb
---

# the-largest-module-is-cut-by-responsibility — resources/board/plan.py` is several modules beside each other, each named for one thing it is responsible for and none over 700 lines, with every command, caller and harness unchanged from the outside

resources/board/plan.py` is several modules beside each other, each named for one thing it is responsible for and none over 700 lines, with every command, caller and harness unchanged from the outside

## Report

spec01: exit 0
resources/board/boards.py 471
resources/board/prdfile.py 537
resources/board/repos.py 134
resources/board/registry.py 260
resources/board/silence.py 163
resources/board/needs.py 140
resources/board/vision.py 215
resources/board/schedule.py 519
resources/board/mapfile.py 488
resources/board/plan.py 644
bash: .pearde/prds/resources-are-organised-by-responsibility/the-largest-module-is-cut-by-responsibility/probe/verify.sh: No such file or directory

spec02: exit 0
index.py check: 1 line(s), exit 1

spec03: exit 0
the-board-runs-itself/one-command: 0 FAIL (was 1), 0 traceback (was 0), harness exit 0
the-tool-keeps-its-word/one-predicate-for-dispatchable: 0 FAIL (was 29), 0 traceback (was 1), harness exit 0
complexity-is-guarded-like-priority: 0 FAIL (was 0), 0 traceback (was 0), harness exit 0
scan-parses-the-board-once-and-caches-it-by-mtime: 0 FAIL (was 0), 0 traceback (was 0), harness exit 0
