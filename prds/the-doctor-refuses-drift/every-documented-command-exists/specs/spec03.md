---
complexity: 10
footprint:
  - resources/doctor.sh
  - references/parts/doctor.md
  - references/files.md
  - index.md
---

# spec03 — the `claims` row, and the new file on the map

One row in `pearde doctor`, between `index` and `statusline`: `ok` with the
counts when every name a document uses exists, `broken` with one `file:line`
note per miss when not. It finds its script with `res claims.py`, like every
other row, and its fix line names both repairs — rename it to what exists, or
mark the mention where the name is meant not to exist.

`resources/claims.py` is a new tracked file, so it needs its row in
`references/files.md` and its place in the scopes `index.md` defines, or
`index check` — the row directly above this one — goes red on the file that
was added to make doctor stricter.

The row is written and working at `probe/row-and-registry.diff`.

**Note for whoever runs this:** the sibling PRD `one-primitive-one-definition`
adds its own row to the same three files. Whichever lands second rebases onto
the first rather than editing the same block twice.

## Acceptance

- [x] `bash resources/doctor.sh <repo>` prints a `claims` row, placed between `index` and `statusline`
- [x] Clean, the row reads `ok` and names the command count and the key count
- [x] Dirty, the row reads `broken` with the miss count, one indented note per miss naming `file:line`, and a `fix:` line naming both repairs
- [x] The row sets doctor's exit to 1 when it is broken, through `row`, and does not otherwise change any other row's text
- [x] Without python3 on PATH the row reads `broken` and names python3 as the fix, like `index` and `memos`
- [x] `references/files.md` holds a row for `resources/claims.py` and `index.md` resolves it under the doctor scope, so `python3 resources/index.py check` prints nothing about it
- [x] `references/parts/doctor.md` describes the row in the list of what doctor checks, naming the three claims and the `<!-- claims: ignore -->` escape

## Verify and Proof

```sh
bash resources/doctor.sh . | grep -E '^  (index|claims|statusline) ' || true
python3 resources/index.py check | grep -q claims.py && echo "FAIL claims.py not on the map"
for f in references/files.md index.md references/parts/doctor.md; do
  grep -q claims "$f" || echo "FAIL $f does not name claims"
done
```
