# The guard

@resources/guard.py — the loop's rules as a mechanism rather than a sentence.

@references/parts/loop.md says a step is one command and one decision, the
board is read with one `scan`, and an established fact is cited rather than
re-run. A model ignoring those sentences still burns the context window; the
pass that cost 318,584 output tokens ignored all three. The guard is the same
three rules where ignoring them is impossible.

## What it refuses

| the call | what it says |
|---|---|
| a board walked by hand — `find … prd.md`, `grep -r state:`, `ls prds/*/prd.md` | step 1 is `plan.py scan`, and it already answers this. A walk carried as data — inside a heredoc body or a quoted string a script or an editor is given — is not a walk and passes; the string a walker itself or `sh -c` runs is |
| a board-reading command run twice with nothing changed since | the output is byte-for-byte what you have; cite it from `.pearde/.state/pass.md` |
| a third read of the same file, unchanged since the first | what you needed from it belongs in the pass file. Counted **per window**, never per session: one session id and one transcript cover the orchestrator and every worker it dispatches, so the stamps are keyed by `agent_id` as well as by path. A second `pearde-pass` worker opens empty and is never refused the first read of a file the first one read |
| a third read of a **reference** file — this manual, through any install link | the manual does not move while a pass runs. @references/parts/loop.md and @references/parts/pass.md are exempt, because a compacted pass has to be able to re-read the steps |
| an `Edit` or `Write` that changes the `state:` line of a `prd.md` — or writes a new `prd.md` carrying one | `use pearde set <prd> <state>`: the command checks the gate of @references/parts/states.md, and a new PRD is `pearde add` or `pearde refine`. A body edit passes. @resources/board/transitions.py writes through @resources/board/edit.py, never through a tool call, so it is never matched — and a worker's shell passes every gate a command has, which is why "never run a transition" stays a sentence in the brief |
| an `Edit` or `Write` whose `file_path` resolves — through any install link, or by name — to a file under this skill's own root, from a session whose board is not this repo's | the install is links into this working tree, per `.pearde/memos/the-install-is-live-symlinks.md`: the refusal names the real path the link resolves to, the memo, and the two ways out — file a PRD on the skill's own board, or hand the edit to a session working it. The same repo passes, a session with no board in scope passes, and a write under this repo's `.pearde/prds/` passes — that is how another board files a PRD here |
| a `Bash` line holding `git reset --hard`, `checkout --`, `clean` or a real `stash` aimed at a tree this session does not own | the refusal names the command, the tree, who holds it, and the memo `pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work.md` — three sessions shared one checkout and a `reset --hard` destroyed a whole uncommitted PRD. `@resources/board/refuse.py` is the reader, and the board's own call sites ask it the same question; this row is the half that reads what a session TYPES. Owning a tree is two rules: the ledger's row for it carries this session's pid, or it is the worktree this process is working inside and no other live session holds it — so a worker's own lane and a person's own shell are never refused. The board that decides is the one above the TREE, not above the cwd, and `git stash create`, `clean -n`, `reset --keep`, `restore --staged` and a plain `checkout <branch>` discard nothing and pass |

And two it only comments on:

- The first read of a spec says the boxes are counted for you — `boxes c/t` in
  the scan. The spec is read for its contract, never to count.
- A `prd.md` written while `.pearde/.state/pass.md` is older than it says the pass
  file is owed. A command is never a tool edit, so every transition command
  says the same on its own line — `pass file owed`, before `as`.

A reference is keyed by its real path, so the same file read once here and
once through a skill folder of links is one file, not two.

The skill-tree refusal matches `Edit` and `Write` only. What the `Bash` hook
reads is the shape of the command — a hand-walked board, a repeated board
read, a destructive git — and never where a redirection points, so a `>` or a
`tee` into a skill file through a link passes unrefused. A gap, said here
rather than papered over: no brief asks a pass to write the skill from a
shell, and a pass that does is not stopped by this guard.

## The ceiling, measured from the floor

`context-budget` (@references/settings.md) is a budget on what a window
**grew**, not on how large it is. A window opens already holding the system
prompt, the tool schemas, `CLAUDE.md` and the skill: 50,229 tokens on this
repo's `/pearde` session of 2026-09-01, before the pass had read anything.
Measured absolutely, half a 100k budget was gone on the first turn and the
ceiling fired on a pass that had run one scan — which is how a ceiling meant
to stop a half-million-token window ended up stopping the work instead.
`budget_floor` in the session file is the smallest window the session has been
billed for, and the refusal is on `ctx - floor`.

Two things it never does. It never measures a **worker**: the hook is handed
the dispatcher's transcript, a worker's turns are absent from it, and a call
carrying `agent_id` is skipped rather than judged by somebody else's number —
a pass worker ends itself by `transitions-per-pass`, per
@references/parts/dispatch.md. And it never leaves a session with nowhere to
go: at the ceiling, dispatching a worker and asking the user stay allowed
alongside the pass file and the steps, so the answer to the ceiling is a
handover, not a stop.

## What it counts

The drill is one of the refusals the loop names where the guard is wired: a
`claim` over an unput frontier — the scan printed a **drill** section and
`## Asked` does not yet carry its questions — is refused by the command itself
(`asking N — drill first`, @references/parts/loop.md step 2) and lands in the
transition window's `refused` count like every refused call, on the row the
next transition writes. The pass reads the scan's drill section instead of
dispatching.

The guard sees every tool call a session makes on a board, so the guard is
where the pass's cost is counted — no second hook, no second process. Per
board, in the session's file under `boards`:

| key | is |
|---|---|
| `calls` · `reads` · `bash` · `edits` · `refused` | tool calls since the session first saw the board, by kind, and how many it refused |
| `since` | the time of the last transition |
| `transitions` | how many this session made on the board |
| `mark` | the counters as they stood at the last transition, with `tokens` — the transcript's output-token sum then |

A transition is where the count is spent. @resources/board/transitions.py
reads the live session's block — the newest file, because the guard touches
its file on every call and the call running the command is the last it saw —
and writes `calls`, `reads`, `refused` and `tokens` on its `.transitions.jsonl`
row: counter minus mark, then the mark moves and `since` with it.
`.history.jsonl` is untouched. `tokens` is the output-token sum the session's
transcript grew by, when the hook input named one and the file is readable;
otherwise `null` — unmeasured, never zero. A session with the guard off writes
`null` in every one of the four: it records nothing.

`pearde status` prints the block as one line — `this session: <calls> calls ·
<refused> refused · <n> transitions · <calls/n> per transition` — and `no
guard` with no session file at all. The analytics view draws the same numbers
as two series, per @references/parts/view.md. Calls are the proxy for tokens,
and the page says so.

One JSON file per session, in the board it counted on:
`<board>/.state/guard/<session>.json`. `PEARDE_GUARD_STATE` moves the
directory for the guard and its readers alike; a harness feeding hook JSON to
a temp project sets it, and so writes into no real board.

**It refuses only what is provably redundant.** "Nothing changed" is the
newest mtime of any `.md` under the board and its members — 7 ms on a
227-PRD master board. An unchanged stamp means an identical answer, which
makes the refusal safe; a board that moved lets the same command straight
through. `plan.py` itself is never refused: a pass recovering from a
compaction has to be able to ask again, exactly when the board has not
moved.

Anything outside a board is not its business, and a guard that throws exits
zero — a broken guard must never be able to block a tool call.

## Wiring it

`pearde guard on [<repo>]` — `<repo>` is the repo the board lives in, by
default the one above the working directory. It reads
`<repo>/.claude/settings.json`, creating it when absent, and adds only what
is missing: `env.MAX_THINKING_TOKENS` when unset, and the four hook entries
below — three naming this skill's absolute `resources/guard.py`, one naming
its `resources/board/serve.py`. Every other key stays, in its order; an entry
already present is skipped, a second `on` says
`already wired, nothing changed` and writes nothing, and a non-JSON file is
refused untouched. It prints the file and each line it added, then the one
sentence to keep: a new settings file is read after `/hooks` or a restart.
`pearde guard off` removes exactly those entries and nothing else —
the env key stays, an event list it emptied is dropped, `hooks` itself
stays. `pearde guard status` prints `doctor`'s `guard` row alone and exits 0
for `ok`, 1 for `off`, 2 for `broken`.

What `on` writes, `<pearde>` being this repo's absolute path:

```json
{
  "env": { "MAX_THINKING_TOKENS": "8000" },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash|Read",
      "hooks": [{ "type": "command",
                  "command": "python3 <pearde>/resources/guard.py pre" }]
    }, {
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command",
                  "command": "python3 <pearde>/resources/guard.py pre" }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command",
                  "command": "python3 <pearde>/resources/guard.py post" }]
    }],
    "SessionStart": [{
      "hooks": [{ "type": "command",
                  "command": "python3 <pearde>/resources/board/serve.py ensure >/dev/null 2>&1 || true" }]
    }]
  }
}
```

**The `SessionStart` entry brings the board up.** Opening a session in the
repo runs `@resources/board/serve.py ensure`, which starts the view daemon if
none runs and registers this board with it — so after a reboot the first
session in a board's repo turns `doctor`'s `view` row from `off` to `ok` with
nobody typing `pearde view`. Measured: 0.05s with the daemon already up, 0.16s
cold. Three details are load-bearing.

| detail | why |
|---|---|
| no `matcher` | the matcher there is the start reason — `startup`, `resume`, `clear`, `compact`, `fork` — and this wants all of them |
| `>/dev/null 2>&1` | a session start prints nothing extra; `ensure` is chatty on success |
| `\|\| true` | `ensure` exits 2 outside a board, and the hooks contract reserves exit 2 for refusing the session — the wrapper is the promise that a session outside a board, or with the port held, or with no python3, still starts |

`doctor`'s `guard` row notes the entry when absent: `no SessionStart
hook — the view is not brought up on a session start; pearde guard on writes
it`. `pearde guard off` removes it with the other three.

The `state:` refusal is a mechanism exactly where this block is wired and a
sentence everywhere else. `doctor` reports `guard` as `ok`, `off` or `broken`
and prints the file it looked in, and its `off` fix line is `pearde guard
on`; it does not write the block itself, for the same reason it does not
wire a status line — a settings file is the reader's, and this one decides
what their tools may refuse. `guard on` is the reader asking. A newly
created `.claude/settings.json` is picked up after `/hooks` or a restart: the
settings watcher only watches directories that had a settings file when the
session started.

**`MAX_THINKING_TOKENS` is the other half.** The guard bounds what a pass
re-reads; the cap bounds the thinking in one response. The pass that prompted
all of this produced five responses that each hit a 32,000-token output
ceiling inside a thinking block, emitted nothing at all — no tool call, no
text — and were retried into the same analysis. No productive thinking block
in that session exceeded 7,073 tokens. 8,000 is above every one of them and a
quarter of the ceiling being hit.

## Turning it off

`pearde guard off`, or set `disableAllHooks` for a session that needs a free
hand. The guard holds no *plan* on the board — one JSON file per session
under `<board>/.state/guard/`, machine-local and gitignored like everything
else that corner rebuilds.

An orchestrator that hits a refusal it believes is wrong should say so in the
pass rather than working around it: a false refusal is a bug in the stamp,
and the stamp is one function.
