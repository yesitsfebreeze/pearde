---
complexity: 6
footprint:
  - resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
  - references/files.md
  - .pearde/memos/a-pass-holds-its-turn-until-its-workers-are-in.md
---

# spec02 — a harness that fails the moment any of the four loses the rule

An invariant script asserts the hold rule is still written in
`references/parts/loop.md` and `references/parts/dispatch.md`, and in the two
sites that let it be lost quietly — `references/parts/workers.md`'s liveness
paragraph and `references/agents/pearde-pass.md`'s verdict table. It is filed
the way this board files a harness: a `kind: invariant` memo whose `verify:`
runs it, so `pearde memo verify` is what fails.

**What already stands.** The analyst's probe wrote the script at its footprint
path, untracked, and added the `references/files.md` row; both are green. The
memo is drafted, unplaced, at
`.pearde/prds/a-pass-holds-its-turn-until-its-workers-are-in/probe/memo-draft.md`.
What is left is to place the memo on the board, run `retag` on it, and judge
the script's phrasing.

**The script.** Seven `want <file> <phrase> <what it is>` assertions over four
tracked files and nothing else — no repo-wide command, no `git status`, no
live board, per the memo
`a-harness-that-reads-the-whole-checkout-is-not-a-harness`. Each file is read
with markdown emphasis stripped and whitespace collapsed to single spaces, so
a re-wrapped paragraph or a bolded phrase still matches and only the words can
break it. A missing file is a failure with its own message. `ROOT=` points the
whole run at another copy of the tree, which is how each assertion is proved
able to go red. Exit 0 while every assertion holds, 1 and a `LOST <file> — <what
it is>` line otherwise.

**The memo.** `.pearde/memos/a-pass-holds-its-turn-until-its-workers-are-in.md`,
`kind: invariant`, `status: decided`, `verify: bash
resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh`,
`prds:` naming this PRD. Its `## Why` is the 2026-09-03 measurement from the
PRD — six workers dispatched in a pass's last turn, transcripts stopping
between 10:02 and 10:10 with no `API Error`, five empty `specs/` directories,
44 uncommitted paths dropped by `sweep --apply`. Its alternatives are the three
the build weighed: letting workers outlive their pass (already refused in
`the-board-assumes-unlimited-agents`), keeping the liveness check as the whole
rule (what shipped, and what failed), and returning a status for the dispatcher
to poll. Move the draft, do not retype it; then run `python3
resources/memos.py retag <board>`, which writes the `tags:` block the checker
expects, and delete the draft from `probe/`.

**The manifest row.** `references/files.md` carries the row for the new script,
beside the other `@resources/invariants/` rows. Without it `python3
resources/index.py check` grows a fifth line.

## Acceptance

- [ ] `bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh` exits 0 against the tree and names each site it checked.
- [ ] The script reads only the four files it asserts on: it runs no repo-wide command, no `git` invocation and no board command.
- [ ] Every assertion can go red. Against a copy of the tree under `ROOT=`, deleting each asserted phrase in turn makes the script exit 1, and so does removing one of the four files.
- [ ] `.pearde/memos/a-pass-holds-its-turn-until-its-workers-are-in.md` exists with `kind: invariant`, a `verify:` naming the script, and a `tags:` block matching its kind and status.
- [ ] `python3 resources/memos.py check <board>` reports nothing against that memo.
- [ ] `python3 resources/memos.py verify a-pass-holds-its-turn-until-its-workers-are-in <board>` prints `holds` and exits 0; with a phrase removed from `references/parts/dispatch.md` it prints `BROKEN` and exits non-zero.
- [ ] `references/files.md` carries a row for the new script, and `python3 resources/index.py check` prints the same four lines it printed before the change and no fifth.
- [ ] `.pearde/prds/a-pass-holds-its-turn-until-its-workers-are-in/probe/memo-draft.md` is gone, its content on the board.

## Verify and Proof

```sh
bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
grep -Ec 'git |index\.py|doctor\.sh|pearde\.py' resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
D=$(mktemp -d); mkdir -p "$D/references/parts" "$D/references/agents"
cp references/parts/loop.md references/parts/dispatch.md references/parts/workers.md "$D/references/parts/"
cp references/agents/pearde-pass.md "$D/references/agents/"
ROOT="$D" bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
perl -0pi -e 's/return ends its children/return closes its children/' "$D/references/parts/dispatch.md"
ROOT="$D" bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh; test $? -eq 1
rm -rf "$D"
python3 resources/memos.py check . 2>&1 | grep 'a-pass-holds-its-turn' ; test $? -eq 1
python3 resources/memos.py verify a-pass-holds-its-turn-until-its-workers-are-in .
python3 resources/index.py check; test "$(python3 resources/index.py check 2>&1 | wc -l | tr -d ' ')" = 4
```
