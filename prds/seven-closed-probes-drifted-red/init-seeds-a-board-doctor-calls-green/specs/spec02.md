---
complexity: 5
footprint:
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
---

# spec02 — the quickstart proves the board green for a reader who has never installed Obsidian

The quickstart's five lines run under whatever home the machine has. On this
machine that home holds an Obsidian register, so `2 doctor closes green`
proved the board green **here** and said nothing about the reader the
quickstart is written for — someone who has never installed Obsidian. The
sibling PRD `the-doctor-completes-without-a-home` (commit `ca29535`) gave the
`vault` row four separated answers; this unit is the one that drives the
second of them from the newcomer's path.

The obligation lands on exactly one file: `probe/quickstart.sh` in the
`readme-in-three-rings` PRD, the only quickstart in the tree, and the PRD
whose two `H` rows are this unit's acceptance evidence. **This is the one
place this PRD writes outside its own directory** — see the report's
`## Writing into a neighbour's PRD` for why, and for the alternative that was
rejected.

**What already stands** — the whole unit is in the tree, uncommitted, as one
new section `6.` between `5. view` and the live-registry check:

- `NOOBS="$TOP/no-obsidian"` — an empty directory under the same `mktemp -d`
  everything else uses, so it holds neither `Library/Application
  Support/obsidian` nor `.config/obsidian`.
- Doctor is run over the **same fresh board** twice: once as the machine has
  it (`$WITH`), once as `env -u XDG_CONFIG_HOME HOME="$NOOBS"`. Scrubbing
  `XDG_CONFIG_HOME` is load-bearing: doctor honours it over a home with no
  macOS register, so an ambient one would leak the real register back in and
  the leg would silently be testing nothing.
- Five checks: doctor exits 0 there; it closes green; the `vault` row's
  verdict is `ok`; the row names the machine (`Obsidian not installed here`)
  rather than reporting a fault; and **no** row's verdict moves between the
  two homes.
- A `rows()` helper reduces a report to `<name> <ok|broken|off>` per row, and
  a tripwire check pins that it read **18** rows rather than zero — without
  it, an extractor that matches nothing makes the diff a comparison of two
  empty strings, which is a check that cannot fail. That is not hypothetical:
  the first version of both `rows()` and the vault read used BSD-`sed`-hostile
  `\|` alternation in a basic regex, matched nothing, and passed.

**What is left** — nothing in the footprint. `resources/doctor.sh` is driven,
not edited; its behaviour under a scrubbed home is the sibling PRD's, already
committed.

## Acceptance

Every box below has been seen red, by mutation, with the red quoted.

- [x] Under a home holding no Obsidian config, doctor over the fresh
      `init --example` board exits 0 and closes `pearde: every part this repo
      owns checks out.`
      **Seen red** on the pre-fix tree, which is where this PRD's whole
      contract was visible: the quickstart's own
      `FAIL: 2 doctor closes green — missing 'pearde: every part this repo
      owns checks out.'`, `31 checks · 30 pass · 1 fail`, exit 1 — on
      `memos broken · README.md: the kind index is stale` and
      `knowledge broken · graph.json missing — run relink`. And again under
      mutation **M3** below.
      **How to fail it again:** revert spec01, or apply M3.
- [x] The `vault` row's **verdict field** reads `ok` — read with
      `sed -nE 's/^  vault +(ok|broken|off) .*/\1/p'`, never as a substring,
      because `ok` is inside `br·ok·en`.
      **Seen red** under mutation **M3** — the fixture home given a register
      naming a different vault
      (`Library/Application Support/obsidian/obsidian.json` holding
      `{"vaults":{"zz":{"path":"/tmp/some-other-vault","ts":1}}}`):
      `FAIL E the vault row answers rather than faulting — got: broken ·
      want: ok`.
      **How to fail it again:** plant that register in `$NOOBS`.
- [x] The row names the machine, not the board — it holds
      `Obsidian not installed here`. This box separates two *different* `ok`
      answers, so it cannot be satisfied by any home that happens to work.
      **Seen red twice.** Under **M3**: `FAIL E ...naming the machine, not the
      board — missing: Obsidian not installed here`. And under mutation
      **M4** — `NOOBS="$HOME"`, this machine's real home, one line changed in
      `quickstart.sh` — where doctor still closed green and the row still read
      `ok`, and only this box caught it:
      `FAIL: 6 ...naming the machine, not the board — missing 'Obsidian not
      installed here'`, `37 checks · 36 pass · 1 fail`, exit 1, over
      `vault ok · … registered with Obsidian — ▸vault opens this board`.
      **How to fail it again:** M4 — point `NOOBS` at any home that has
      Obsidian.
- [x] No row's verdict moves between the two homes: the `<name>
      <ok|broken|off>` reduction of both reports diffs to zero lines. This is
      the check that catches a home-dependent row anywhere else in the report,
      whatever it is.
      **Seen red** under **M3**: `FAIL E no row's verdict moves between the
      two homes — got: 2 · want: 0` — the `vault` row moving `ok`→`broken`
      and doctor's own verdict with it.
      **How to fail it again:** M3.
- [x] The row reader read the whole report — 18 rows, not zero.
      **Seen red** by construction: on the first writing, `rows()` used
      `sed -n 's/…\(ok\|broken\|off\)…/p'`, and BSD `sed` has no `\|`
      alternation in a basic regex, so it emitted nothing on every call and
      the diff above compared two empty strings and passed. Reproduced
      directly:
      `printf '  vault       ok      /x\n' | sed -n 's/^  vault *\(ok\|broken\|off\) .*/\1/p'`
      prints nothing, while the `-E` spelling prints `ok`. This tripwire is
      what makes the previous box falsifiable at all, and it stayed **green**
      under M3 (`ok E the row reader read the whole report — 18 rows, not
      zero`) while every other E box went red — which is what a tripwire
      should do.
      **Also seen red where it matters most** — the vacuous-fixture attack,
      run by the implementing pass: `doctor` over a directory holding **no
      board at all**, under the same scrubbed home, exits `0` and closes
      `pearde: every part this repo owns checks out.` So boxes 1 and 4 above
      would both pass on a fixture that never had a board. Three checks
      refuse it, and this is one: the row reader reads `7` rows there, not
      `18`. The other two are the `vault` verdict field, which comes back
      empty (`[]`, not `ok`), and `Obsidian not installed here`, which is
      absent. The leg cannot pass by the fixture being empty.
      **How to fail it again:** restore the basic-regex spelling in `rows()`,
      or add or remove a row from `doctor.sh`; or point the leg at a
      boardless directory, where it reads 7.
- [x] The two `H` rows of `readme-in-three-rings`' own `verify.sh` — the PRD
      this unit's acceptance evidence lives in — read green:
      `H quickstart.sh exits 0` and `H ...and every check passed`.
      That harness now reports `74 checks · 73 pass · 1 fail`, and the one
      failure is **not** an `H` row and not this unit's: `FAIL: G index.py
      check is silent — got '115', want '0'`, the sibling session's untracked
      playwright drop under `resources/board/node_modules/`. Before this PRD
      it was `2 fail` — the `H` rows and `G`.
      **Seen red** on the pre-fix tree, quoted in box 1.
      **How to fail it again:** revert spec01; the `H` rows go red again on
      `2 doctor closes green`.
- [x] The quickstart still proves what it proved before: it exits 0 and its
      count grew only by this leg, `31 checks` → `37 checks · 37 pass · 0
      fail`, with checks `1`–`5` and the live-registry check unchanged.
      **Seen red** under M4 (`37 checks · 36 pass · 1 fail`, exit 1) and on
      the pre-fix tree (`31 checks · 30 pass · 1 fail`, exit 1).
      **How to fail it again:** any of M3, M4, or reverting spec01.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# the leg exists, scrubs XDG, and reads the verdict field rather than a
# substring of the row
grep -n 'env -u XDG_CONFIG_HOME HOME="$NOOBS"' \
  .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
grep -n "sed -nE" \
  .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh

# the quickstart end to end — its own five lines plus this leg
bash .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
# expects: 37 checks · 37 pass · 0 fail, exit 0

# the acceptance evidence: the two H rows of the PRD this leg lives in. That
# harness exits 1 on the neighbour's index red, and `collect` runs this block
# under `pipefail` — so it is captured, then read. Gating this spec on that
# exit would make this unit's pass conditional on a drop nobody here owns.
NB=$(bash .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh 2>&1 || true)
printf '%s\n' "$NB" | grep -E '^FAIL|checks ·'
# expects: 74 checks · 73 pass · 1 fail — the one FAIL is
#   `G index.py check is silent — got '115'`, the neighbour's untracked
#   node_modules drop. NO row beginning `H ` may be among the failures:
printf '%s\n' "$NB" | grep -c '^FAIL: H ' || true   # 0

# this PRD's own probe drives the same leg from its own fixture (section E)
bash .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh
# expects: 41 checks · 41 pass · 0 fail · 0 skip
```
