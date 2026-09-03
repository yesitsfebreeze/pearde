---
complexity: 18
footprint:
  - resources/common.py
---

# spec01 — `common.py` gains one git runner and one section extractor

`resources/common.py` gains `run_git(root, *args, ...)` and `section(text,
name, ...)`, each parameterised (`check=`, `default=`, `raise_as=`, and for
`section` its own match/shape knobs) so that every existing duplicate of
either primitive across the tree can point at this one definition, keeping
its own return-or-raise contract, in a one-line delegation.

## What already stands

Both functions are written, in the lane, at the bottom of `common.py`:

- `run_git(root, *args, check=False, default=_UNSET, raise_as=None,
  timeout=60, input=None, env=None, stdout=False, strip=False, msg=None)`
  — runs `git -C root <*args>` once. A failure is git missing/timing out,
  or (`check=True`) a non-zero exit; it raises `raise_as(message)` when
  given, else returns `default` when one was passed, else re-raises the
  process-level error or (a checked failure with neither) raises
  `RuntimeError`. `msg(args, root, completed_or_exc)` builds the failure
  text when a caller's own wording is part of its contract. Success
  returns the `CompletedProcess`, or `.stdout` (`.strip()`ped when `strip`)
  when `stdout=True`.
- `section(text, name, *, all=False, lines=False, prefix=False, word=False,
  ci=True, heading=False, chomp=False, default=None)` — the body under
  `## <name>`, to the next `## ` line. `name` matches a heading's text
  exactly, as a prefix (`word` requiring a word boundary after it), or —
  `name` a compiled pattern — via `.match()`. `all=True` returns every hit
  in file order instead of the first; `heading=True` pairs each body with
  its heading; `lines`/`chomp` control the one leading newline a plain
  regex search on this body carries.

Every current duplicate this repo holds of either primitive was read and
matched against the new one, one call site at a time, in
`probe/probe_common.py` — a direct import of the real sibling modules
(`workflows.py`, `board/specs.py`, `board/collect.py`, `board/prdfile.py`,
`board/transitions.py`, `questions.py` for the section extractor;
`shared.py`, `repos.py`, `orphans.py`, `refuse.py`, `board/collect.py`'s
`git_out` for the git runner), asserting the new call reproduces the old
function's output byte for byte on both a success and a failure path.
`python3 probe/probe_common.py` (root auto-detected, or `PEARDE_ROOT=<the
lane>` while unmerged): `PASS: every checked caller contract reproduced`.

`PEARDE_ROOT=<lane> python3 resources/index.py check` and `PEARDE_ROOT=<lane>
bash resources/doctor.sh` were run before and after the edit; the only
diffs are (a) the statusline row picking up this file's own uncommitted
change and (b) an unrelated `workflows` row moving `broken → ok` between
the two runs — a concurrent session on the shared board retagging files
under `.pearde/workflows/`, nothing this footprint touches. `common.py is
on disk with no row in references/files.md` was already failing before
this edit — see Findings.

## What is left

Nothing in this file. The three sibling PRDs this one's `needs:` row feeds
(`the-core-board-modules-delegate-to-common`,
`the-lane-and-repo-modules-delegate-to-common`,
`the-top-level-resources-modules-delegate-to-common`) do the actual
one-line delegation at each of the ~17 call sites the probe catalogues;
this spec's job was only to prove the primitive's shape covers every one
of them, not to edit them — editing any of those files is outside this
PRD's footprint.

## Acceptance

- [x] `common.py` defines `run_git` and `section` with the signatures
  above, stdlib only (`os`, `re`, `subprocess`, `sys`).
- [x] A probe reproduces, for every cataloged caller, both its success
  shape and its failure shape (a raised exception, or a returned default)
  from a one-line call into the new primitive.
  `PASS: every checked caller contract reproduced`
- [x] `resources/index.py check` and `resources/doctor.sh` show no new
  failures against the pre-edit baseline.
  index.py check: identical 3-line output before and after (all
  pre-existing, none naming `run_git` or `section`) · doctor.sh: only the
  statusline's own dirty-file count and one concurrent, unrelated
  `workflows` row differ

## Verify and Proof

```sh
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/common-py-gains-a-git-runner-and-a-section-extractor/probe/probe_common.py
python3 -c "import ast; ast.parse(open('resources/common.py').read())" && echo "common.py parses"
```
