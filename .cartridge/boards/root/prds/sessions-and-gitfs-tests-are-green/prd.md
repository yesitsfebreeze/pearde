---
state: "specced"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- "sessions.ctg"
- "gitfs.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
---

# Sessions and gitfs tests are green

## Outcome

The two owners with the most red tests (2026-09-14: sessions 8, gitfs 6) pass repeatably.

## Acceptance

- [x] `just test sessions` and `just test gitfs` exit 0 on three consecutive runs; the count observed at the start is in Result.

## Result

2026-09-15, pass 3 (cartridge-ctg-22). Landed as sessions.ctg `b896162` and
gitfs.ctg `f837c81`.

Start count: the 2026-09-14 red (sessions 8, gitfs 6) did not reproduce at
sessions `207f47e` / gitfs `cb638a5` with the unowned 07:13-07:41 attempt in the
trees: sessions 92/92, gitfs 48/48. The attempt was the fix, and no live
session claimed it. It was kept except one part: it gave gitfs's production
`Capture` two fields (`kept`, `kept_bytes`) only so tests could shrink the caps;
those are gone and the provenance tests reach the real `record::batch()` (1024)
and `record::batch_bytes()` (16 MiB) caps. Docs that named 8 MiB for settings
defaulting to 256 MiB, and mailbox credential variables outside the
`SESSIONS_MAILBOX_*` grant, were corrected in the same commits.

Independent verifier, 11:24:51-11:28:43 CEST, cwd `/Users/feb/dev/cartridge`,
at sessions `207f47e` + diff sha256 `e8d83853…`, gitfs `cb638a5` + diff sha256
`4b96f25e…` (unchanged before and after; the commits above are that diff plus
the doc lines):

```
just test sessions  run 1  exit 0  test result: ok. 92 passed; 0 failed   (25.6s)
just test sessions  run 2  exit 0  test result: ok. 92 passed; 0 failed   (29.5s)
just test sessions  run 3  exit 0  test result: ok. 92 passed; 0 failed   (25.0s)
just test gitfs     run 1  exit 0  test result: ok. 48 passed; 0 failed   (35.2s)
just test gitfs     run 2  exit 0  test result: ok. 48 passed; 0 failed   (36.4s)
just test gitfs     run 3  exit 0  test result: ok. 48 passed; 0 failed   (40.0s)
just check sessions        exit 0  check sessions pass
just check gitfs           exit 0  check gitfs pass
grep -n 'kept' gitfs.ctg/src/provenance.rs   (no output)
```
