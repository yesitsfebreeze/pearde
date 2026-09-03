# the obsidian vault is opt-in — analyst report

Verdict: SPECCED

Workflow followed: `probe-then-spec`. The build went through end to end. Four
specs, complexity 29, all four written from code that runs in the lane at
`.pearde/.lanes/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in`,
uncommitted, for the next worker to continue.

## What the build did

Pass one (already in the lane when this pass started) had done `init.py`'s
plugin tuple, `write_obsidian`'s key block, `community-plugins.json`,
`Dashboard.md` and `knowledge.py`. This pass finished the contract:
`install.sh` (the fetch row and a sweep for the dropped bundle),
`references/obsidian.md`, `references/files.md`, `README.md`, `doctor.sh`, and
the prose left behind in `init.py` — plus one defect pass one introduced, below.

Both halves of `## Done means` were proved on a fixture board made at run time:

- `pearde init <fresh>` writes no `.obsidian/` and no `.obsidian-api-key`
  anywhere under the project. It prints one line naming `pearde vault` and the
  text fallback.
- `pearde doctor <fresh>` prints `vault  off`. It printed `vault  broken` at
  `f8968fe` — see *The vault row was broken for a different reason* below.
- `write_obsidian` called directly on that fixture returns
  `(['dataview'], [], None)` and seeds a vault with one plugin and no key.

## Findings

### `pearde vault` and `pearde upgrade` refuse on every board this repo makes

`unhide_board` opens with `name = name or planlib.BOARD_DIR`, then refuses any
name starting with a dot. `BOARD_DIR` is `.pearde` and `LEGACY_BOARD_DIR` is
`pearde` since `c88a64a`, so the guard now refuses its own default:

```
pearde vault: refused — a board directory is one plain name with no dot in
front of it — `.pearde` is what the move is out of
```

Reproduced at `f8968fe` on a clean fixture, so it is not this PRD's doing. It
matters here because this contract makes `pearde vault` the only door to the
vault, and that door is currently shut on every board `init` writes; `upgrade`
refuses the same way, before it prints its vault line. **It is not this PRD's
to fix**: spec03 of
`the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`
already owns the `unhide_board` call at the top of `pearde vault`. That PRD
should be a `needs` of this one, or land first.

### This PRD and `the-vault-roots-at-the-project…` contradict each other on the plugin count

That PRD is `analyzing`, priority 95, and already carries four specs. Its
spec01 footprint is `install.sh`, `community-plugins.json`, `app.json`,
`plugins/unhide/data.json`, `init.py`; its spec04 is titled *the written
contract says the project root and **names three plugins***. Three is
`dataview`, `obsidian-unhide` and `obsidian-local-rest-api` — and this PRD
removes the third. After both land the count is two. Whichever lands second
must not restore the plugin this one drops. Called out inside spec02 and
spec04 so an implementer reads it before touching either file.

### `install-fetches-nothing` moves the file spec02 edits

That sibling is `specced` and its spec01 moves the whole plugin block out of
`install.sh` and behind `pearde vault`. spec02 here is the same two changes in
whichever home the fetch list has when it is picked up; the spec says so.

### Footprint overlap is now the norm on this board, against what README promises

`README.md`'s glossary says *"the paths a PRD or spec touches; two claimed PRDs
never share one"*. On the current board `references/files.md` appears in five
sibling specs, `resources/board/init.py` in four, `references/obsidian.md` in
three and `resources/doctor.sh` in two — before this PRD adds its own. Either
the rule or the board is wrong. Not fixed here.

### A defect pass one introduced, fixed by this pass

Pass one wrote `` `pearde knowledge dashboard` `` into `Dashboard.md`,
`knowledge.py`, `README.md` and `init.py`'s new console line. There is no such
verb: `pearde knowledge dashboard` prints ``unknown command `knowledge` ``.
Corrected to `python3 resources/knowledge.py dashboard`, which is how
`Dashboard.md` already spelled its sibling command. `pearde report` is a skill,
not a verb, so `references/obsidian.md` names the modules instead.

### The vault row was broken for a different reason than the contract assumed

The contract reads as though doctor said `broken` because Obsidian was absent.
It did not: the *first* arm of the row fires on a board named `.pearde`, and
`init` writes exactly that, so every board this repo makes reported `vault
broken` whatever was installed. Moving the `no .obsidian/` arm above it is the
whole fix and gives the contract what it asks for. That arm's own `fix` line —
`pearde upgrade`, which would move the board back to the undotted layout the
invariant `the-board-directory-is-pearde-and-the-compat-symlink-is-gone`
forbids — is left untouched: it belongs to the PRD named above.

### `init` at `f8968fe` registered fixture boards in the machine-wide Obsidian register

Confirmed on a throwaway fixture: `init: registered baseOKXJ with Obsidian`.
Removing `register_vault` from `cmd_init` takes that away as a side effect —
the same pollution the sibling PRD flags in its own contract. It is not
hypothetical: this machine's `obsidian.json` holds eight fixture vaults right
now, from three earlier sessions' scratchpads and two deleted `tmp.*` dirs.
They are other sessions' entries and were left alone.

### Pre-existing red, unchanged by this pass

`resources/index.py check` prints the same four problems before and after
(`resources/common.py` with no row; `references/files.md` and `@@view` naming
`resources/board/hotreload-test.js`, deleted at `b1d3f5d`;
`references/parts/commits.md` citing an absent memo). The board's own
`## Deliverable` makes `index.py check` a gate, so this board's gate is red
independently of this PRD. `install.sh --check` treats a lone `--check` as the
skills directory and emits `usage: dirname string [...]` — also pre-existing.

### Harnesses

`index.py check`: 4 problems before, 4 after, same four.
`install.sh --check`: rows unchanged except `obsidian-local-rest-api` moving
from `ok` to `stale`, which is the intended new report.
Invariants: `a-board-s-own-file-commits-in-the-board-repo`,
`a-master-need-is-the-union-of-its-members`,
`every-artifact-lands-inside-the-board`,
`no-destructive-git-runs-in-a-tree-the-session-does-not-own` and
`one-copy-per-machine-of-what-every-lane-regenerates` all pass in the lane
(the last two take minutes each and were run detached; both exit 0, the fifth
reporting `450 link(s), none of them visible to git status` and `0 claim(s)
failed`). `no-colour-group-in-the-vault-preset-is-a-path-query` reports `BROKEN: no
board at pearde/` in the lane and passes in the main checkout — the lane
worktree carries no board, so that is the harness's environment, not a
regression.

### Knowledge

`knowledge.py query` on the contract returned 91 hits, 77 strong; nothing
auto-enqueued into `.pearde/wiki/pending/`. No fact in this pass came from
outside the tree, so nothing was written back with `remember`.

## Specs

| spec | goal | complexity | footprint |
|---|---|---|---|
| spec01 | `init` writes no vault, mints no key, `pearde vault` is the only door | 12 | `resources/board/init.py`, `resources/board/obsidian/community-plugins.json` |
| spec02 | the installer ships one bundle and sweeps the one it dropped | 5 | `resources/install.sh` |
| spec03 | doctor's vault row reads `off` when no vault was asked for | 4 | `resources/doctor.sh` |
| spec04 | the written contract says optional viewer, and the text fallback is named | 8 | `README.md`, `references/obsidian.md`, `references/files.md`, `resources/board/knowledge/Dashboard.md`, `resources/knowledge.py` |

Sum 29, four specs — inside the board's caps of 40 and 6.

**Union of the footprints:**

```
README.md
references/files.md
references/obsidian.md
resources/board/init.py
resources/board/knowledge/Dashboard.md
resources/board/obsidian/community-plugins.json
resources/doctor.sh
resources/install.sh
resources/knowledge.py
```

**complexity 22** — the work is subtraction across nine files with one
behaviour change per file, all of it built and running in the lane; what makes
it more than trivial is that four of those files are contested by three
sibling PRDs, so an implementer has to read before it edits.

**blast-radius mid** — it changes what `init` writes on every board anyone
makes and removes a credential from the layout, but nothing reads that
credential, no verb is removed, and a vault already on disk is untouched.

## Scores

complexity: 22
blast-radius: mid
workflow: probe-then-spec
