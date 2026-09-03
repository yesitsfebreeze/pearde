# Install check

A present but broken install looks exactly like an absent one. `doctor.sh`
tells the two apart. Run doctor on the first run, on `doctor`, and
whenever a part is silent when a part should not be.

```sh
bash @resources/doctor.sh [board]         # report; exit 1 when a part is broken
bash @resources/doctor.sh --fix [board]   # report, then repair
bash @resources/doctor.sh --harnesses [board]   # …and run the board's harnesses
```

One part per line, each `ok`, `off`, or `broken`. A broken part carries the
command that repairs it. `members` reports only on a master board, and `index`
never reads `off` — the map is either right or wrong.

| part         | `off`                                  | `broken`                                                        |
|--------------|----------------------------------------|------------------------------------------------------------------|
| `skills`     | —                                      | a skill file with no `name:`, no `description:`, or a `name:` that disagrees with its file name |
| `index`      | —                                      | @references/files.md and the tree disagree, or an `@@` keyword is undefined in @index.md |
| `claims`     | —                                      | a document names a command, a settings or frontmatter key, or a memo that does not exist |
| `statusline` | —                                      | @resources/statusline.sh renders nothing for this board                       |
| `board`      | no board                               | off the contract path, or no `language`                          |
| `members`    | not a master board — no `members:`     | an entry that is not a board on disk, or an empty list           |
| `origin`     | no PRDs to read                        | a `derived` PRD with no `from:`, or the @references/parts/derived.md tripwire live |
| `memos`      | no `memos/`                            | a memo fails the check in `@references/memo.md`                   |
| `workflows`  | no `workflows/`                        | a file fails the check in `@references/workflow.md`               |
| `grammar`    | no grammar file on the board           | a term defined twice, a row that is neither two columns nor three, or a frontmatter key nobody declared |
| `health`     | no `health/` on the board              | a note with a key nobody declared or for a file no longer tracked, a ranking that disagrees with its notes, or a knob that cannot be read |
| `questions`  | no PRDs to read                        | a pass the user cannot act on — the four shapes are below        |
| `view`       | the service is not running             | the service runs and this board is not registered                |
| `plan`       | no plan on record yet                  | —                                                                |
| `harnesses`  | `harnesses:` is not `on` and `--harnesses` was not passed, or the board has no `verify.sh` | a harness exits non-zero — named, with its first `FAIL` line |

## No agent is named, so the check holds for any reader

**No agent is named in `doctor.sh`, and none is looked for.** Where a skill
folder goes and where a status line is configured are the reader's setup, not
this repo's — @references/install.md is that step, written to be worked out
rather than executed. Doctor checks only what holds regardless of who is
reading: the skill files parse, the map matches the tree, the status line
renders, the board is on its contract.

## `skills` is about frontmatter, not placement

A skill is found by its `name:` and fires on its `description:`. Frontmatter
failing to parse is a skill that silently never fires, which reads exactly like
a model choosing not to use the skill. A `name:` disagreeing with the file name
installs one skill under another's name.

## `statusline` answers the half that is ours

A line wired to a script rendering nothing and a line not wired at all look
identical in a terminal. Doctor runs the script against this board and says
which of the two is on screen.

## `index` checks both halves of the map

`@resources/index.py check` reads the scopes in @index.md and the manifest in
@references/files.md: a file on disk with no row, a row naming no file, a scope
naming no file, an `@@` keyword nobody defined. Not `--fix`-able — which row a
new file belongs in is a judgement.

## `claims` checks that what a document names still exists

`index` reads paths and `memos` reads memos; neither reads a sentence. So a
reference telling a reader to run a command that was renamed away, a settings
key nothing honours, and a memo slug cited by a module that outlived the memo
all pass every other row here — and each one sends a reader somewhere that is
not there. `@resources/claims.py check` reads three claims a document makes,
each against the thing that answers it:

1. a `pearde <verb>` in `references/**/*.md`, against the commands
   @resources/pearde.py forwards and discovers
2. a settings or frontmatter `key:`, against `SETTING_KEYS` and
   `FRONTMATTER_KEYS` in @resources/board/init.py
3. a `memos/<slug>.md` cited in `resources/**/*.py`, against the board's memos

One direction only. Something documented that does not exist is a defect; a
command nobody documented is a judgement, and is not reported. A claim is read
only from a backtick span, a fenced block or a skill's `description:` — the
three places this repo writes a name it means literally — so a sentence saying
the pearde board, or asking whether pearde is up to date, stays prose.

Where a document names something on purpose that does not exist — a rejected
alternative, an example of drift, a key the board deliberately does not honour
— the line says so with `<!-- claims: ignore -->` on it or on the line above.
That is the second half of the fix line: rename it to what exists, or mark the
mention.

## `questions` reports four silent shapes

`@resources/questions.py check` is the only reader of the pass's format. Every
shape below is silent from the outside — a board with a broken pass and a board
with nothing to ask look identical:

1. a `## Questions` or `## Answers` heading with nothing beneath
2. a question that asks nothing, has no prepared answers to pick from, does not
   carry three, or whose recommended answer is missing or not first
3. an `## Answers` section with no `## Questions` above, an answer to a
   question nobody wrote down
4. a PRD parked on the user — `state: question`, or any parked state or `mode:`
   naming a human — never saying what the PRD asks

The same pass reads `needs:`, because a `needs:` holding prose instead of PRD
names resolves to nothing in `plan` and is reported nowhere else. An answered
pass is history and is left alone. Not `--fix`-able: what a question should
have asked is the one thing only its author knows.

## `workflows` catches the half no single file can see

`@resources/workflows.py check` is the only reader of the workflow format,
reading the library the way `memos` reads `memos/` — the closed frontmatter
set, one slug key, the required sections — plus the half no single file can
see: a step naming an atomic nobody wrote, and a `workflow:` on a `prd.md` or a
spec naming no **workflow** in the library. An atomic is a file, so naming one
is that same failure: a route was asked for and a single step was found. Both
shapes are silent from the outside, and both send a worker nowhere.

A `workflows:` pointing outside `.pearde/` is checked in full, not mirrored —
this library shared between boards, not another system's. Not `--fix`-able:
what a step should name is its author's to say.

## `grammar` catches a term defined twice

`@resources/grammar.py check` is the only reader of the vocabulary format,
reading `.pearde/grammar.md` the way `memos` reads `memos/` — the closed
frontmatter set, an ISO date, an `updated` not preceding its `date` — plus the
half no single row can see: one term defined twice, and a table row neither two
columns nor three. Both are silent from the outside. A term with two rows
answers a lookup two ways, which is what the collision table exists to stop; a
row of the wrong width is a row no reader can tell from a collision.

A `grammar:` pointing outside `.pearde/` is checked in full, not mirrored —
this vocabulary shared by the boards over one codebase, not another system's.
`stale` is no part of the check and fails no row: a term appearing nowhere in
the tree is a candidate for deletion and a judgement, not a defect, and a word
said in passes and never typed is exactly the word a grammar exists for. Not
`--fix`-able: what a word means is its author's to say.

## `health` prints `stale` and fails nothing on it

`@resources/health.py check` is the only reader of the health record, reading
`.pearde/health/` the way `memos` reads `memos/` — the closed key set on every
note and on the ranking, a score as an integer 1-100, an ISO date — plus the
half no single file can see: a note for a file the tree no longer tracks or now
skips, a ranking whose count disagrees with the notes beside it, a row with no
note.

`stale` is printed and fails nothing: a ranking twenty commits behind HEAD, or
a graph newer than the one the ranking read, is still the right pointer, and
the line ends in the command that refreshes the record. `--fix`-able in the
plain sense — the record is regenerable and `pearde health score` is the fix —
except a knob in `settings.md` that cannot be read, which is a person's to
correct.

## `harnesses` runs the board's own checks, opt-in because slow

The row runs every `verify.sh` that `find` returns under `.pearde/`, and
nothing else: a harness outside this board is not this board's business. Every
PRD is closed against one, and until this row existed nothing ran them — no CI,
no hook, no command; every green total on record was a person remembering to
type it.

**Opt-in, because the row is slow**: the one row measured in tens of seconds
where the rest answer in one, and a gate nobody can afford to run is the defect
the row fixes, repeated. `harnesses: on` in `.pearde/settings.md`, default off,
or `--harnesses` for a single run whatever the key says.

## A few at a time, so a red is a real red

The sweep runs the harnesses in parallel but caps how many are in flight at
once — `PEARDE_HCAP`, default **4**. Uncapped, forty-eight harnesses started
together and collided over the three fixed ports and the board service some of
them bind: in the sweep of 2026-09-01 nearly half the reds went green on a
serial re-run, so the row's number could not be believed without re-running
every failure by hand, which is the work the row exists to avoid.

Four is above the number of harnesses actually contending at any one moment and
far below the box's core count, so nothing waiting on a socket is starved of
CPU. The cap buys isolation, not speed: **wall-clock is not the case for the
cap** and moves either way between boxes. What stays stable is the thrashing of
an uncapped run — the sum of the harnesses' own durations was over three times
higher uncapped than capped on the same box, so most of an uncapped sweep's
work is contention rather than testing.

Raising `PEARDE_HCAP` trades isolation for time, and lowering the cap buys no
more isolation. An environment variable rather than a `.pearde/settings.md` key
on purpose: the dial for an experiment, never a contract surface a board is
meant to tune.

## The expected count is the harness's own — no ledger

A recorded total is a second copy of a number the file already carries, and
this board has twice paid for that shape. A harness pinning its denominator —
`[ "$((PASS+FAIL))" = 39 ] || no "expected 39 checks, ran $((PASS+FAIL))"` —
fails loudly when a check is dropped. A harness pinning nothing prints a
smaller total and exits 0, indistinguishable from success, and so is reported
as **unpinned** rather than trusted: named under the row, and its pass does not
make the row green on its own account.

Doctor reads the *idiom*, not the semantics — a test comparing the harness's
own executed total against an integer literal. So `[ "$((PASS+FAIL))" = 0 ]`
reads as pinned and asserts nothing, and a literal left behind at the wrong
number reads as pinned until the harness is run. Nothing forces a harness to
pin a denominator, and nothing here fails on an unpinned harness; the row
counts and names them, and only the harness's own author can enforce a pin.

## `--fix` repairs one thing, and doctor re-checks once

`--fix` repairs a view service down or not watching this board, and writes no
settings file — a status line lives in the user's own.

A harness running `doctor` itself — two on this board do — gets
`off · not run inside a harness` from the inner run. Without the guard, a board
with the key on runs doctor, which runs the harness, which runs doctor, and
never returns.

After repairing, doctor re-checks once, so the report and exit code describe
the state the repairs left behind. `--harnesses` survives the re-check. `--fix`
does not repair a red harness and cannot: what a failing assertion should have
said is its author's to say.
