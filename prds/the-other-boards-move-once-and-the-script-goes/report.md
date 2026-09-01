# report — the-other-boards-move-once-and-the-script-goes

Verdict: **DONE**. All three specs complete, 11 of 11 boxes ticked against
output I ran. All eight boards on this machine are migrated and gate clean, the
registry is rewritten, and the migration script is retired out of the tree.

This report was written once at BLOCKED and finished after the coordinator
recorded the probe in history; `## The wall` below keeps the stop and its
answer, because why the deletion waited is part of what happened.

## Seven working trees hold staged moves that nobody has committed

Read this first. `migrate.py` moved seven live boards in seven other
repositories. In six of them `git mv` staged the move in that repo's index and
**left it there, uncommitted, exactly as the fixture proof does it**. Nothing
was committed and nothing was pushed, in any repository, per the brief. Six
repos now have a working tree with a large staged rename set waiting for their
owner:

| repo | staged `R` renames | other staged changes |
|---|---|---|
| /Users/feb/dev/infra/mitosys | 303 | 0 |
| /Users/feb/dev/manola | 253 | 0 |
| /Users/feb/dev/infra/model | 173 | 0 |
| /Users/feb/dev/infra (master) | 118 | 0 |
| /Users/feb/dev/infra/shared | 70 | 0 |
| /Users/feb/dev/infra/realm | 64 | 0 |
| /Users/feb/dev/racer (holds .mi) | 0 | 0 |

`racer` is 0 because `racer/.mi` is a fully untracked board — its move was
plain `mv` and the index was never touched, which is the behaviour spec01's
fourth box asks for. The rewritten `.gitignore` files and the master's
rewritten `settings.md` are unstaged working-tree edits in the same repos.

`resources/board/state/serve.json` in this repo now holds the seven rewritten
registry rows. It is machine-local state, gitignored by
`.gitignore:5 resources/board/state/`, so it shows in no `git status` and
needs no commit — the change is live the moment it is written.

## spec01 — migrate.py, the throwaway one-shot · 5/5

Nothing was left to build. Both proofs re-run green from the tree as it stood.

- `bash probe/verify.sh` → `verify: 31 checks · 31 pass · 0 fail`
- the spec's own block → `pre-gate ok`, `moved to .pearde/ (git mv 4 /
  plain 0)`, `GATE: scans clean`, `LAYOUT: ok`, `STATE: loose record kept`,
  `spec01 fixture gate done`

The `pre-gate ok` line is worth naming: an un-migrated fixture board is
*refused* by the scan, not read as empty. That is the shape of the hole this
PRD closes.

## spec02 — the live run · 4/4

Run in the order the spec sets, one board at a time, each gated before the
next. Every count below is the scan's PRD number against the prd.md-holding
directory count that board's old `prds/` held, counted recursively before the
move. **Every one matches.**

| board | old `prds/` held | scan after | move |
|---|---|---|---|
| mitosys | 135 | 135 | git mv 40 / plain 6 |
| model | 82 | 82 | git mv 32 / plain 4 |
| realm | 19 | 19 | git mv 22 / plain 1 |
| shared | 17 | 17 | git mv 15 / plain 2 |
| manola | 49 | 49 | git mv 49 / plain 4 |
| racer/.mi | 48 | 48 | git mv 0 / plain 16 |
| infra (master, last) | 20 | 20 own · **273 merged** | git mv 24 / plain 4 |
| dotfiles | — already migrated | 196 | untouched |

mitosys was cross-checked a third way, because it was migrated before the
baseline routine settled: 135 prd.md-holding dirs under `prds/` in `HEAD`, 135
under `.pearde/prds/` in the index, 135 on disk, 135 from the scan.

infra's 273 is 20 + 135 + 82 + 19 + 17 exactly — the master reads all four
members through their rewritten rows, and drops nothing.

Before the run, all seven refused the gate with `pearde: no .pearde/ board at
<root>`, exit 2. The sibling `orphans` finding is confirmed and now closed.

Members rows rewritten in `/Users/feb/dev/infra/.pearde/settings.md`, four of
four, and they are the only member-shaped rows on any of the eight boards:

    - ../mitosys/.pearde
    - ../model/.pearde
    - ../realm/.pearde
    - ../shared/.pearde

The scan of the master reports `@mitosys/` 38 times, `@model/` 15, `@realm/`
1, `@shared/` 2 — unprefixed beyond the sigil (`@mitosys/p0-spike`,
`@mitosys/p6-rust-core/p6n-chat-tui`).

`serve.json`: 7 rows rewritten, all nine rows now name a directory that
exists. The spec's block agrees — 8 `GATE ok` lines, `SERVE REGISTRY: ok —
every row is a live board dir`, `MEMBER SIGILS: present`.

`migrate.py` printed **no WARNING at all**, on any of the seven.

### The two live claims, as accepted

mitosys' `p8o-vesicle-sweep` and racer/.mi's stale `04-audio-pipeline` were
moved with their boards, as authorised. Nothing about either PRD's content was
touched — only the path it sits at. An in-flight worker in either repo is
holding a path that no longer exists and **will re-scan after the move**; its
next board command finds the PRD under `.pearde/prds/` at the same name. The
scan confirms both survived: mitosys reports `claimed 1`, racer/.mi
`claimed 2`.

## The wall — spec03, and how it came down

spec03 said, in its own words: *"The probe copy left in the tree by pass one is
this unit's deletion target; the PRD's own history in the board repo holds the
file after that."*

**That second clause was false when I reached it.** `probe/` was untracked on
branch `pearde` and `git log --oneline -- .../probe/migrate.py` returned
nothing. Deleting then would not have retired the script into the record; it
would have destroyed it. I stopped and asked whether to commit first or delete
unrecorded, rather than guess which half of that sentence was meant.

The answer was commit first, and the coordinator made the commit. I verified it
myself before removing anything, which is what I had been told to do:

    $ git log --oneline -- .../probe/migrate.py
    c15b234 the-other-boards-move-once-and-the-script-goes — record the
            migration probe before it goes
    $ git branch --contains c15b234
    * pearde
    $ git cat-file -s c15b234:.../probe/migrate.py
    10785

10785 bytes, the byte-for-byte size of the working copy, on the branch the
board lives on. **The deletion that followed is a retirement, not a loss** —
`migrate.py` is recoverable from `c15b234` by anyone who ever needs to read
what moved these eight boards, and the decision on record (no dual-path
support, no permanent migration command) is honoured because it is in history
rather than in the tree.

### verify.sh went with it — the reasoning

`probe/verify.sh` is not named in spec03's footprint, so the call was mine. It
goes, and the spec is why. Every one of its 31 checks reads the output of two
lines:

    line 59:  python3 "$MIG" "$B/board-a" "$A" "$B" "$C" --serve ...
    line 113: python3 "$MIG" "$A" --quiet ...

`$MIG` is the file spec03 deletes. With `migrate.py` gone the harness cannot
pass a single check — it is not a weakened proof, it is 31 guaranteed
failures wearing the costume of a test. A harness that can only ever fail is
worse than no harness, because the next person to run it debugs a ghost. The
same decision that retires the throwaway retires the throwaway's proof, and
`c15b234` recorded both files, so this deletion is the same retirement on the
same terms. The 31/31 result it produced is quoted under spec01 above and
stays readable there.

`probe/` is now empty and removed. The PRD folder holds `prd.md`, `report.md`
and `specs/` — nothing else.

### What spec03's own block prints, and why the box is still true

Run verbatim, spec03's `find` prints:

    /Users/feb/dev/infra/pearde/.pearde/prds/
      every-document-names-the-path-the-board-is-on/probe/migrate.py
    LEFTOVER migrate.py FOUND
    GATE ok: <all eight boards>

**That is a homonym, not a leftover.** The surviving file belongs to a
different PRD — `every-document-names-the-path-the-board-is-on`, `state: done`
— and is a different program: 2896 bytes against 10785, sha `52a5c4e0…`
against `231de30c…`, and a docstring that begins *"Probe: apply the specific-
rule table … to the scoped prose files"*. It rewrites bare `prds/` mentions in
documentation. It has never moved a board and holds no `BOARD_DIR`, no
`--serve`, no `git mv`. It shares a filename with my deletion target and
nothing else.

It is also **not mine to delete**: touching another PRD is forbidden by the
standing brief, and a box cannot require an action the brief refuses. Read
against the spec that contains it — *"The probe copy left in the tree by pass
one is this unit's deletion target"* — box 1 is about the migration script,
and the migration script is gone. So I ran the check the box means, and ticked
on this:

    == any surviving BOARD migrator (moves prds/ to .pearde/)? ==
    NONE: no board migrator left in the tree
    == this PRD's own probe folder ==
    PROBE GONE: folder removed entirely

The eight-board gate re-ran after the deletion and is unchanged: eight
`GATE ok` lines, nothing else depended on the script.

Flagged for the orchestrator, not fixed: spec03's `find` is name-based, so it
will keep printing `LEFTOVER migrate.py FOUND` for as long as that sibling
PRD keeps its own probe. The line is noise from a filename collision. Anyone
re-running this block should read the path it prints before believing it.

## Findings — recorded, not fixed

1. **`--serve` alone does not work.** `migrate.py --serve <path>` strips the
   flag, finds no positional board argument, prints the usage docstring and
   returns 2 — the registry is never rewritten, silently, behind a wall of
   help text. spec02 says "then `--serve` rewrites the registry" as if it were
   a standalone invocation. I got the rewrite by passing the flag alongside
   the seven now-idempotent board roots, which is the documented usage line
   and is a no-op on the boards (`already on .pearde/ — skipped` × 7, then
   `serve.json: 7 row(s) rewritten`). Not fixed: spec03 deletes the file, so
   the defect dies with it. Written down in case the deletion is reversed.
2. **State collisions are not warned about, only named.** All seven boards hit
   the collision — every one carried both a loose `prds/.history.jsonl` and a
   `prds/.state/history.jsonl`. The rule held: the loose record kept the name,
   the loser is at `.pearde/.state/history.jsonl.from-state-dir`, nothing
   deleted. But spec01 says the loser is "warned about" and `move()` only
   warns when a destination already exists, so no `WARNING` was printed. The
   evidence of a collision is the file's name, not the run's output. spec02's
   fourth box passes either way, but a reader expecting a warning line will
   not find one.
3. **dotfiles still has an empty `prds/`.** `/Users/feb/dev/dotfiles/prds/`
   survives its hand migration, holding nothing but a `.state` directory.
   Harmless — the scan reads `.pearde/` and reports 196 — but it is the one
   board root on the machine where both layout directories exist, and it is
   why `migrate.py` would say "already migrated — skipped" there rather than
   "already on `.pearde/`". Outside this PRD's footprint; dotfiles was never
   mine to touch.
4. **Junk rode along, exactly as before.** `infra`'s `prds/__pycache__/`
   (a stray `.pyc`) and `realm`'s `prds/specs/` (two loose spec files under no
   PRD) were directories at the old board root, so step 5 moved them into
   `prds/`. Neither holds a `prd.md`, so the scanner ignores them in the new
   layout exactly as it ignored them in the old. Pre-existing mess, moved
   faithfully, not cleaned — cleaning it is content, and content was out of
   scope.
5. **Five boards' root `prd.md` is still unread.** mitosys, model, shared,
   manola and racer/.mi each keep a loose `prd.md` at the old board root; it
   now sits at `.pearde/prds/prd.md` and is skipped by the scanner in the new
   layout exactly as it was in the old. Confirms the probe round's finding 5,
   now on five boards rather than one.
6. **shared has no `prds` lines in its `.gitignore`**, which is why it was the
   one board with zero `.gitignore` rewrites. Not a miss — checked the file.
7. **Two unrelated PRDs named their probe `migrate.py`.** Harmless here, but
   it is what made spec03's acceptance check misfire, and it will misfire the
   same way for anyone who re-runs it. A probe filename is worth making
   specific to its job — `migrate-boards.py` would have cost nothing and saved
   this paragraph.

## Written back outside this repo

The cross-repo facts — the eight boards, their counts, which repos track their
state dotfiles, which board is untracked, the collision rule's outcome — are
on record in the knowledge base as `sources/260901-ee0f.md`, `[[260901-ee0f]]`.

## Numbers

- specs done: 3 of 3 · boxes 11 of 11
- spec01 5/5 · spec02 4/4 · spec03 2/2
- boards migrated: 7 · boards gating clean: 8 of 8 · registry rows live: 9 of 9
- PRDs that were invisible to the board before this run and are visible now:
  350 (135 + 82 + 19 + 17 + 49 + 48), plus the master's own 20
- repositories holding uncommitted staged moves: 6 · commits made by me: 0 ·
  pushes made: 0 (the one recording commit, `c15b234`, was the coordinator's)
- files retired out of the tree: 2 (`probe/migrate.py`, `probe/verify.sh`),
  both recoverable from `c15b234` on branch `pearde`
