---
complexity: 14
footprint:
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
---

# spec02 — the README harness judges the README, against a control run

Four assertions in the README harness were readings of the machine rather
than of the code: two pinned counts of a tree several sessions write, one
pinned row total, and two comparisons of whole `doctor` reports taken at
different moments. This unit replaces each with a relation or a control pair,
so the harness goes red when the README or the code moved and at no other
time.

## What stands from the probe

The rewrite is in the tree, uncommitted, and green — `75 checks · 75 pass · 0
fail` in `verify.sh`, `41 checks · 41 pass · 0 fail` in `quickstart.sh`, on a
working tree that three sessions are writing and in which `index` is
genuinely broken.

| was | is |
|---|---|
| `verify.sh` F: `ls references/skills/*.md` = `16` | a dry `install` run builds one folder per `references/skills/*.md` — the relation install states in its own help — and the dry run builds nothing |
| `quickstart.sh` 1: `16` folders, `80` links | folders = skill files, links = folders x 5 |
| `quickstart.sh` 2: init's report closes green | rows broken with **no board on disk** are the checkout's and are named in a note; rows broken only with the board are init's, and that is what is asserted |
| `quickstart.sh` 6: the whole report at 19 rows | a floor of 15 rows plus two rows named, so an extractor reading nothing still fails and a new `doctor` row does not |
| `quickstart.sh` 6: diff of two whole reports | three reports — real HOME, scrubbed HOME, real HOME again. A row that moves with the home held constant is the machine: named in a note, not judged. A row that moves only across the home boundary must reproduce on a second pair before it is a red |

`quickstart.sh` 5 also stopped reading the first URL `view` prints: when the
service is not already up, `view` prints `serve: started on http://…:PORT`
first, and whether the service happens to be up is machine state. It now
matches the `/board/` URL.

**The measurements that justify it.** On 2026-09-02, at HEAD,
`references/skills/` held **15** files while the harness asserted 16 — it was
green only because a neighbouring session had an uncommitted sixteenth file
in the working tree. And
`.pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/flake-doctor.sh`
stops the view service between the two `doctor` runs, which is what a
neighbour's `serve.py stop` does, and the old comparison printed `< view ok /
> view off` and went red with the README, `doctor.sh` and the board all
correct.

**The flip.** Two probes, both on the same HEAD:

- `probe/steady-doctor.sh` runs the old comparison and the new one side by
  side under that same injection: old `rows differing: 2 -> RED`, new
  `moved with the home held constant, so not judged: view` and `-> green`.
- `probe/flip-readme.sh` builds four trees from `git archive HEAD` and
  compares each variant's failures against the baseline's, since the live
  tree moves under the run:

| tree | injected | added failures |
|---|---|---|
| `good` | nothing | baseline |
| `skill` | a seventeenth file under `references/skills/` | none — the old harness went red here |
| `home` | `doctor`'s `memos` row taught to read `$HOME` | `6 no row but vault reads the home` |
| `board` | the example board `init` copies carries a memo `doctor` rejects | `2 the board init wrote breaks no doctor row` |

## What is left

Run the three commands below. The harness is green on a churning tree; if it
is not, read which check failed — every one of them now names either the
README, `init`, or `doctor`, and none of them names the machine.

## Acceptance

- [x] `bash .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh` ends `0 fail` and exits 0
- [x] neither harness file pins a count of the tree or of the report — no bare `"16"`, `"80"` or `"19"` right-hand side survives in either
- [x] `bash .pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/steady-doctor.sh` exits 0: the old comparison red and the new one green under one injection
- [x] `bash .pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/flip-readme.sh` exits 0 and ends `FLIP:` — a seventeenth skill file adds no failure, a home-dependent row and a badly written board each add theirs
- [x] a `doctor` row that is broken before any board exists is reported as a note and does not fail a check — the note line `broken before any board existed` appears when the checkout has one, and the run still ends `0 fail`

## Verify and Proof

```sh
V=.pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
Q=.pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
OUT="$(bash "$V")"
printf '%s\n' "$OUT"
bash .pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/steady-doctor.sh
bash .pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/flip-readme.sh
PINNED="$( { cat "$V" "$Q" | grep -cE '"(16|80|19)"$' || true; } )"
[ "$PINNED" = 0 ] && [ -n "$(printf '%s\n' "$OUT" | grep ' 0 fail$')" ]
```
