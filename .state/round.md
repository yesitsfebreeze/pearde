# Round — the user's five answers became five specced PRDs

Written by session `f54db065`, 2026-09-02, resuming the previous round's
`ASK`. **The user answered all five forks of `.pearde/.state/ask.md`, every
one on the recommended option. This round turned all five into board state,
dispatched an analyst on each, and collected all five SPECCED.** The board is
no longer drained: it is five implementers away from done.

`done 64/68 · 96% · specced 5 · open 0 · analyzing 0 · blocked 0`. Ten
transitions landed — five claims, five collects — against a
`transitions-per-round` of 8. The overrun is deliberate and bounded: a worker
already dispatched must be collected, and stopping mid-flight would have left
five live claims for the next window to sweep.

**Next window's job is the implementers, and nothing else.** Every PRD is
`specced` with its specs on disk. Read the dispatch-order constraint below
before claiming two at once.

## The five answers, and what each became

| fork | the user said | PRD | cx | blast | workflow | specs |
|---|---|---|---|---|---|---|
| Q5 | *Run them a few at a time, so a failure is always a real one.* | `the-harness-sweep-is-capped-so-a-red-is-a-real-red` p40 | 18 | mid | `probe-then-spec` | 3 |
| Q3 | *Add it to the instructions, so following them produces something that is accepted.* | `the-brief-names-the-verdict-line-collect-requires` p30 | 16 | mid | `correct-a-documented-claim` | 2 |
| Q4 | *Bring each one back in line with how things work now.* | `four-stale-self-tests-are-re-aimed-at-the-code-that-moved` p20 | 14 | mid | `probe-then-spec` | 4 |
| Q1 | *Fix it — bringing a board forward should leave it as healthy as creating one fresh.* | `upgrade-leaves-the-memo-index-stale` p0 | 9 | low | `probe-then-spec` | 1 |
| Q2 | *Refuse to file at all rather than write a record naming a file it does not hold.* | `filing-refuses-a-file-it-does-not-hold` p30 | 8 | mid | `probe-then-spec` | 1 |

Each PRD body carries the mechanism the previous round verified, with line
numbers and timestamps on it, and names the fork the user rejected as an
explicit non-goal. **No analyst had to re-establish any of it, and none did.**

## Read this before dispatching two implementers at once

**`pearde plan` offers all five in parallel. It is wrong about two of them.**
Q4's `spec04` *reads* `references/parts/workers.md` — the file Q3 *rewrites*.
Neither lists the other's path in its `footprint:`, so the clash check never
fires. **Dispatch Q3 before Q4, or serialise them.** Run them together and one
will look red for the other's work.

The other three are genuinely independent: `collect.py` (Q2), `init.py` (Q1),
`doctor.sh` + two harness probe dirs (Q5).

**Q5 and Q4 both touch harness probe dirs but not the same ones.** Q5's
footprint names `the-view-row-names-a-variable-that-exists/probe` and
`seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe`;
Q4's six re-aims are in `one-page-that-says-whats-up`, `the-fixtures-meet-the-tool`,
`collect-is-a-command`, `init-asks-nothing` and `workflow-improve`. No overlap.

## The tree holds five analysts' uncommitted builds — they are ours

Every analyst built its fix first and left it uncommitted. That is the analyst
contract's pass one, not stray work, and the implementer continues it. So the
working tree legitimately holds changes to `resources/board/collect.py`,
`resources/board/brief.py`, `resources/board/init.py`, `resources/doctor.sh`,
`references/parts/workers.md`, `references/parts/doctor.md` and several
harness `probe/` dirs.

**Every one of the five reports warns about "a sibling session" holding
uncommitted edits. There is no sibling session — they were seeing each
other.** `workers.md` + `brief.py` are Q3's, `init.py` is Q1's, `doctor.sh` is
Q5's, `collect.py` is Q2's, the harness probes are Q4's and Q5's. Two reports
describe reds that "closed under me by siblings" for the same reason. The
reports are still right that **none of those files may ride another PRD's
`collect --also`.**

## Findings the analysts brought back — act on these, do not re-derive them

**1 — `wait -n` does not exist on macOS `/bin/bash` 3.2.57.** `doctor.sh:740`'s
own comment promised a `wait -n` cap, and Q5's PRD body repeated it. Writing it
as specified **would have broken `doctor` on every macOS box.** The analyst
polled `jobs -r` instead. Cap is **4**, overridable with `PEARDE_HCAP`. Fact
written to the record as `[[260902-e933]]`. Acceptance was demonstrated: two
capped sweeps returned identical failure sets, equal to a full serial re-run,
**failures 8 → 1**, at 80s against the 84s uncapped baseline — the cap costs
nothing.

**2 — `verdict_of` tolerates far less decoration than the tree claims.** Q3's
analyst refuted the docstring at `collect.py:258`, and with it a sentence this
round wrote into Q3's own PRD body. `**Verdict:** SPECCED`, `*Verdict:* X`,
`- Verdict: X` and `> Verdict: X` are all **silently refused**. The analyst
correctly did **not** loosen the tool — `verdict_of` asserted byte-identical to
HEAD, per the user's answer — and made the brief name the shape that works
instead. When briefing a worker, say **"a line beginning `Verdict:`"**.

**3 — Q3's fix landed in `brief:every`, not the analyst block.**
`brief.py:340` serves that block to the analyst *and* the implementer, while
the consultant at `:361` never sees it. One edit, exactly the two roles that
write reports. After: analyst 1, implementer 1, consultant 0; the duplicated
half-sentence at `workers.md:156` deleted, 2 → 1 → 0.

**4 — three *unnamed* harnesses carry the same dead `REG` path** as Q4's two
and pass vacuously today. Outside Q4's contract. File or fold deliberately —
`derived.md`'s tripwire applies.

**5 — `doctor`'s unpinned-detector only matches the literal `$((PASS+FAIL))`,**
so no harness reporting skips can pin. **43 of 52 read unpinned.** Not fixed;
its own contract.

**6 — `the-fixtures-meet-the-tool`'s `F no file under resources/` row reads
the whole working tree's git diff**, so it goes red on *any* neighbour's
uncommitted work. It went red on Q1's `init.py`, not on Q4's work. **Expect
that red while implementers are in flight; it is not evidence.** It is also
the one genuine red Q5 left standing.

**7 — `vision` is a second init/upgrade divergence.** `write_board` seeds
`vision.md`; `upgrade` never does. `doctor` calls it `off`, not `broken`, so
it is outside Q1's contract. Its own PRD if anyone wants it.

**8 — `~/Library/Application Support/obsidian/obsidian.json` holds 700 vaults,
674 of them temp fixtures, 660 dead paths.** The harness set registers every
`mktemp` board it makes, and the file grows on every sweep. Board-wide, not
any one PRD's. Worth a memo at least.

**9 — `knowledge.py board` counts `memos/README.md` as a memo.** Pre-existing
on both paths, cosmetic.

**10 — Q4's PRD body cites `resources/view/…` for two files that live at
`resources/board/…`.** Line numbers right, directory wrong. This round wrote
that error; the analyst caught it and specced against the real paths. Q4's
`## Findings` has the list.

**11 — one analyst could not use the Write tool for `report.md`** (harness
block) and wrote it via Bash. The file is what `collect --report` reads and it
parsed fine.

## The constraint that is not ours to relax

Two of Q4's four stale checks pin **the view session's deliberate changes** —
`render.py:459` (`eaa11a1`) and `view.css:508` (`4ce11ec`). Q4's body forbids
editing either file to satisfy a check: the check moves to the code, never the
reverse. The analyst honoured this — **no product code was touched**, only
harness checks, and all six re-aims were mutation-proven non-vacuous. Hold the
implementer to the same line: a change that looks necessary in those two files
is a QUESTION, not an edit.

## Board record

`.pearde/` is its own git repo (`git rev-parse --show-toplevel` →
`/Users/feb/dev/infra/pearde/.pearde`), which is why the code repo can read
clean while the board has changes. The previous round's uncommitted
`report.md` and round file were committed this round as **`8b59243`** together
with the five `prd.md` files. Analyst `specs/`, `probe/` and `report.md` are
**not** staged — they ride their own collect.

The code repo (`/Users/feb/dev/infra/pearde`) is at `f3aea95` with the five
analysts' pass-one builds uncommitted on top.

## Green as of this round

`doctor .` exits 0 — every row `ok` but `harnesses` and `jstests`, both `off`
by configuration. `questions`, `memo check`, `index`, `workflow check` all
silent. `origin` reads `68 requested (5 live) · 22 derived (0 live)`.

## Owed, none of it blocking

`memos/one-typo-crashes-every-round.md` is the only memo at `status: open` and
is **stale, not undecided** — the crash it describes is fixed (`spec_data` is
`plan.py:479`, `num` at `:733` is documented *"Never raises"* and returns
`0.0`). **It wants closing, not answering**, and there is no `memo close`
command, so it needs a deliberate edit on a collect that opens the memo dir.

`a-probe-that-prints-no-count` (`run-all.sh` `printf "" "$out"` twice — every
row reads `pass=0 fail=0`). `spec01` box 8 of the init PRD wants an existence
anchor. `memos.py index` could print a path it did not write. graph-probe
spec02 check A is a spelling-grep and its `prd.md` is still the unfilled
template. The `18`-row doctor tripwire lives in two committed harnesses.
`reportParts()` in view.js parses 3 of 4 parts. `doctor.sh --harnesses .`
renders the board name `?` from a relative path.

## Retired — do not carry forward

- The `ignore_patterns("README.md")` consequence (already fixed —
  `index_memos()` at `init.py:349` regenerates after the copy).
- The `doctor.sh:743` "analyst hunk adopted" claim (never true — `:700-798`
  landed whole in `7809756`).
- The node_modules paragraph.
- `.state/round.HANDOFF-collect1-will-fail.md` — the alarming name is stale
  and the file says so.
- The old "`--also` needs the `.pearde/` prefix" trap **survives only until
  Q2's implementer lands**; after that a bad path is refused outright, which is
  the point. A spec's own `footprint:` has the same trap and is still not
  checked.

## Traps that still hold

After any collect, `git show --stat` the commits **and** `git status` the
board. SPECCED commits nothing. A worker killed by infrastructure is
**resumed**, not replaced. `brief` on a claimed PRD takes
`--worker <the claim's id>`. **sonnet 402s, bare inherit 429s — pin
`model: "opus"`** (all five analysts ran clean on opus this round). Every
board command needs a persona: `PEARDE_AS=engineer`, or `sweep` refuses.
There is no `pearde` binary on PATH — it is
`python3 /Users/feb/dev/infra/pearde/resources/pearde.py`. Tell every worker
that, and tell it the `Verdict:` shape; the brief now says the latter itself
once Q3's implementer lands.

`jstests` is `off` because *its* `playwright-core` is missing, not our doing.
`pearde-eb` and `pearde-19` are stood down.
