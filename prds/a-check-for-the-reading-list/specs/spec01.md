---
complexity: 12
footprint:
  - resources/scout/scout.sh
  - resources/scout/README.md
---

# spec01 — `scout.sh reading` checks the reading list's shape and state

Adds the `reading` verb to `scout.sh`: a check pass over `reading-list.md`
that (a) fails, naming the row, when a row's mapping column ("what to
steal") is blank, and (b) marks a row `<!-- stale: archived YYYY-MM-DD -->`
in place, in the repo-link cell, when the row's repo has gone `ARCHIVED` —
never deleting the row. State is resolved the way `toolscout.sh`'s `STATE`
column is: the newest `snapshots/*.tsv` is checked first (free, already
fetched), and `gh api repos/<owner>/<repo>` is called only for a repo no
snapshot names, so a full run of the list does not pay one network call
per row.

The probe already built and rehearsed the whole thing against the real
`reading-list.md` (0 stale — nothing in it is actually archived today, 17/17
rows carry a mapping) and against fixtures for every branch: a bare row, an
archived row (`facebook/react-native-fbsdk`, archived since 2021 — a stable
fixture), an idempotent second run, and the snapshot-guard (stubbed `gh`,
proved uncalled when a snapshot row exists). `.pearde/prds/a-check-for-the-reading-list/probe/verify.sh <path-to-scout.sh>`
reruns all six checks in a scratch `mktemp -d` fixture — it touches no real
file. This spec is largely a formalization pass: read the diff already in
the tree (`git diff resources/scout/scout.sh resources/scout/README.md` in
the lane), run the probe, and decide whether the design choices below stand
or need a different call.

Two behaviours are deliberate and not forks to re-open without cause:

- The `owner/repo` is parsed from the GitHub **URL**, not the markdown link
  text — the build hit a real counter-example (`[cargo-mutants](.../sourcefrog/cargo-mutants)`,
  where the link text is not `owner/repo`).
- A repo the API cannot resolve (renamed, deleted, private) is left
  unmarked. Unknown state is not treated as stale; this is a silent no-op,
  not an error, on the theory that a false "stale" costs more trust than a
  missed one — revisit only if that theory is wrong in practice.

## Acceptance

- [x] `scout.sh reading` exits non-zero and names every row whose mapping
      column ("what to steal") is blank, without modifying the file.
- [x] `scout.sh reading` exits 0 when every row has a mapping, and marks
      `<!-- stale: archived YYYY-MM-DD -->` in place on any row whose repo
      reads `archived: true`, leaving every other row's line untouched.
- [x] A second run over an already-marked file does not duplicate the
      comment or re-run the network for that row.
- [x] A repo present in the newest `snapshots/*.tsv` is resolved from that
      row and no `gh api` call is made for it — verified by a stubbed `gh`
      that logs any invocation.
- [x] `resources/doctor.sh` gains no new row for this check — it stays part
      of the verb, per the PRD's `## Done when`.
- [x] `README.md`'s command table and the four-layers overview mention
      `scout.sh reading` — the check should not be findable only by reading
      the script.

## Verify and Proof

```sh
bash .pearde/prds/a-check-for-the-reading-list/probe/verify.sh resources/scout/scout.sh
bash -n resources/scout/scout.sh
grep -c 'reading' resources/scout/README.md   # >0: the verb is documented
# bare `grep … || true` cannot fail: a doctor row would land and the block
# would still pass. Written so the wrong answer reddens it.
if grep -q 'scout' resources/doctor.sh; then echo 'doctor gained a scout row'; exit 1; fi
```
