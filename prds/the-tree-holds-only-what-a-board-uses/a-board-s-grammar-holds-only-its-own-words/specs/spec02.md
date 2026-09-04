---
complexity: 10
footprint:
  - resources/board/init.py
  - resources/pearde.py
  - references/parts/grammar.md
  - references/skills/pearde-grammar.md
  - references/grammar.md
  - references/files.md
  - index.md
---

# spec02 — an old board is trimmed by `pearde upgrade`, and the map says so

A board written before the shipped file carries 300 lines of pearde's own
words, and a merge over it would print each of them twice. `pearde upgrade`
runs the trim: a group goes only when the shipped file holds every one of its
rows, spelling and meaning, so one edited row, one added row, one row a newer
shipped file no longer has, and the whole group stays with the row that kept it
named. `## This repo` is never read. The verb is forwarded as
`pearde grammar trim`, and the documents that said a board starts with the
vocabulary in it now say where it lives.

**What stands.** All of it, uncommitted in the lane. `init.py` grew
`trim_grammar()` beside `plant_grammar()` and `cmd_upgrade` calls it on the
already-planted branch, printing the reporter's lines; `pearde.py` forwards
`trim`; `references/files.md` has the row for `references/grammar-board.md` and
the template row no longer claims pearde's own words are in it; `index.md` has
the file in `@@grammar`; `references/grammar.md`,
`references/parts/grammar.md` and `references/skills/pearde-grammar.md` name
the shipped file, the merge, which verbs read it and which do not, and `trim`.

**What is left.** This repo's own board still carries the 318-line copy. It is
a write into `.pearde/`, outside this PRD's footprint, so it is one command at
land time and not an edit: `python3 resources/pearde.py upgrade .` — the last
box. Run it after spec01 is green, never before: a trim under the losing merge
would have cost this board 34 rows.

## Acceptance

- [x] `pearde grammar trim <board>` runs the trim, and the usage `pearde grammar <unknown-verb>` prints names it.
- [ ] On a board holding the old copy, `pearde upgrade` reports the groups dropped and rewrites `grammar.md` to under 40 lines; `grammar show prd` still answers afterwards.
- [ ] A second `pearde upgrade` on that board writes nothing and says the file is its own words already.
- [x] A group holding one edited or one added row is kept whole, and the report names the row that kept it.
- [x] `references/files.md` has one row for `@references/grammar-board.md`, and the `@references/templates/grammar.md` row no longer says pearde's own words are in it.
- [x] `@@grammar` in `index.md` resolves to `@references/grammar-board.md`, and `python3 resources/index.py check` prints nothing it did not print at baseline.
- [x] No document still says `pearde init` writes the board vocabulary into the board's file.
- [ ] This repo's own `.pearde/grammar.md` is under 40 lines and `doctor`'s `grammar` row still reads 183 terms.

## Verify and Proof

```sh
bash .pearde/prds/the-tree-holds-only-what-a-board-uses/a-board-s-grammar-holds-only-its-own-words/probe/probe.sh
python3 resources/pearde.py grammar nosuchverb 2>&1 | grep -q trim || exit 1
if grep -rn "already.holding the board vocabulary\|pearde's own already in it" references/ index.md 2>/dev/null; then exit 1; fi
# index.py check is a repo-wide gate with four pre-existing baseline lines —
# captured and printed; only a line naming a grammar file decides.
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'grammar-board|grammar\.py|templates/grammar\.md|parts/grammar\.md|pearde-grammar\.md|board/init\.py|resources/pearde\.py'; then exit 1; fi
# doctor is a repo-wide gate — captured; its grammar row must still read 183.
dout=$(bash resources/doctor.sh . 2>&1) && rc=0 || rc=$?
printf '%s\n' "$dout" | grep '^  grammar'
printf '%s\n' "$dout" | grep '^  grammar' | grep -q '183 terms' || exit 1
wc -l < .pearde/grammar.md   # 318 until the land-time `pearde upgrade .`; under 40 after it
```
