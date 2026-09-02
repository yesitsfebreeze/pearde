---
complexity: 5
footprint:
  - references/parts/guard.md
  - references/install.md
  - .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh
---

# spec03 — the manual says it, and the sibling harness counts four

Two claims about the block `pearde guard on` writes are copied in three
places. All three now say four hooks, and
`@references/install.md`'s *"which every session start does"* — the sentence
this PRD exists to make true — names what does it.

**The two doc edits stand already**, uncommitted in the tree:

| file | change |
|---|---|
| `@references/parts/guard.md` | "the three hook entries below" → four; the `SessionStart` block added to the JSON it shows; a `**The SessionStart entry brings the board up.**` paragraph with the measured costs and a three-row table saying why no `matcher`, why `>/dev/null 2>&1`, why `\|\| true`; the note `doctor` prints when it is absent |
| `@references/install.md` | the `pearde guard on` bullet names the `SessionStart` hook; the view bullet's *"which every session start does"* now ends *"from the `SessionStart` hook `pearde guard on` writes"* |

**The harness edit is not built** and is the one thing here that reaches
outside this PRD. `@.pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh`
counts the lines `guard on` and `guard off` print. It counted three hooks;
there are four. Five literal numbers, and nothing else in that file:

| line | check | `3`/`4` → |
|---|---|---|
| 38 | `A four + lines` | `5` — the env cap plus four hooks |
| 65 | `A three - lines` | `4` |
| 94 | `B four + lines` | `5` |
| 104 | `B three - lines` | `4` |
| 119 | `C three + lines — the cap was set` | `4` |

Rename each check's text to the number it now asserts. Line 119's rename lands
on `C four + lines — the cap was set`, which is **correct**: section C starts
from a settings file whose cap is already `4000`, so the cap adds no `+` line
and the four hooks are all of them. The stale-label box below was originally
aimed at the bare needle `four + lines`, which that correct new label also
matches; it is aimed at the five stale labels by name instead. The rule it
asserts — no check still says three hooks — did not move.

The other 73 checks in
that file are green under the four-hook block and stay untouched — the
byte-identical round trip, the foreign-hook preservation and the key ordering
all held through the probe pass. **The orchestrator sequences this**: the file
belongs to another PRD, and nothing else in this spec does.

## Acceptance

- [x] `@references/parts/guard.md` shows a `SessionStart` entry in the JSON block it says `guard on` writes, and states that the entry carries no `matcher`
- [x] `@references/parts/guard.md` gives a reason for `>/dev/null 2>&1` and for `|| true` separately
- [x] `@references/install.md`'s *"which every session start does"* names the hook that does it
- [x] `grep -c 'three - lines\|three + lines\|A four + lines\|B four + lines' .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh` returns `0` — no stale three-hook label survives
- [x] `guard-on-is-one-command`'s harness reads `78 checks · 78 pass · 0 fail`
- [x] Section H of this PRD's probe harness is green
- [x] `python3 resources/index.py check` exits 0

## Verify and Proof

```sh
bash .pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh
bash .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh
python3 resources/index.py check
```
