---
complexity: 14
footprint:
  - resources/board/collect.py
  - resources/board/edit.py
  - resources/board/prdfile.py
  - resources/board/specs.py
---

# spec01 — `collect.py`, `edit.py`, `prdfile.py` and `specs.py` delegate their duplicate primitives to `common.py`

Every duplicate definition of `common.py`'s git runner or section extractor
in these four files becomes a one-line call into `run_git`/`section`,
keeping its own failure shape. `boards.py` is in this PRD's file list but
gets no edit — see Findings for why its `find_board` is a documented
exception, not a gap.

## What already stands

All four edits are written, in the lane:

- `collect.py`: `section(text, name)` is now `return common.section(text,
  name, ci=False, default="")` — case-sensitive exact-line match, `""`
  absent, byte for byte what the old inline regex gave. `git_out(root,
  *args, input=None, shared=False)` keeps its own scratch-index `env`
  computation and now runs the git call through `common.run_git(root,
  *args, check=True, raise_as=Stop, input=input, env=env, timeout=None,
  stdout=True, msg=...)` — same `Stop` exception, same message text, no
  timeout (the old code had none either).
- `edit.py`: gained the standard `pearde_path`/`import common` two lines
  every other module under `resources/` opens with (it had neither before —
  it was the one leaf module with no sibling imports at all).
  `write_atomic(path, text)` is now `return common.atomic_write(path,
  text)` — the two were already byte-identical (temp file, write, `os.replace`).
- `prdfile.py`: `_h2_sections(body, name)` is now `return common.section(body
  or "", name, all=True, prefix=True, word=True, ci=False)`.
- `specs.py`: `section_text(text, name)` is now `return common.section(text,
  name, prefix=True, default="", chomp=True)`.

Verified in `probe/probe_core_delegate.py` — each delegated function's
success and failure/edge shape checked against its pre-edit behaviour
(`collect.section` case-sensitivity, `git_out`'s message text and its own
`env`, `write_atomic`'s bytes, `_h2_sections`'s case-sensitivity and word
boundary, `specs.section_text`'s prefix match) — `PASS: every delegated
caller in the core board modules reproduced its pre-edit contract`. The
sibling PRD's own `probe_common.py` (which first proved the primitive's
shape covers these callers) still passes unchanged against the edited
tree: `PASS: every checked caller contract reproduced`.

`PEARDE_ROOT=<lane> python3 resources/index.py check` before and after:
identical 3-line output (all three pre-existing, none naming these
functions). `PEARDE_ROOT=<lane> bash resources/doctor.sh` before and after:
the only diffs are two `claims` rows' line numbers shifting by one (the
memo they cite moved down one line because of this edit, the broken
reference itself is pre-existing) and the `statusline` row's own dirty-file
count — no new failing row.

## What is left

Nothing in the four edited files. `boards.py` is named in this PRD's
contract but not edited — see Findings.

## Findings

- **`boards.py`'s `find_board` is not delegated.** It duplicates
  `common.find_board`'s board-resolution logic, but on failure it calls
  its own `die(msg, code=2)` — every refusal in `boards.py` exits 2, by
  file-wide convention (checked: every `die(` call in the file uses the
  default). `common.find_board(arg, prog)` fails with `sys.exit(f"{prog}:
  ...")`, and passing a string to `sys.exit` is always exit code 1 — its
  own docstring already says it is "kept as a copy" of the planner's
  resolver for exactly this kind of reason. A one-line delegation here
  would silently turn every `boards.py` refusal from exit 2 into exit 1.
  Confirmed in `probe_core_delegate.py` by running both through a
  subprocess: `boards.find_board` (via `plan`, its public entry point) on a
  bogus path exits 2; `common.find_board` on the same path exits 1.
  Nothing currently reads that exit code (grepped the tree for `== 2` or
  `returncode == 2` near a `find_board` caller — none), so today it costs
  nothing, but a one-line delegation is not possible without either
  widening `common.find_board`'s signature with a failure hook (out of
  this PRD's footprint — `common.py` is not in it) or catching and
  re-raising `SystemExit` at the call site, which is not "one-line".
- **`boards.py` duplicates the whole board-resolution family, not just
  `find_board`.** `is_board_dir`, `board_link`, `named_boards`,
  `board_scanned`, `board_in` and `board_above` all exist in both
  `boards.py` and `common.py`. The parent PRD's `primitives` doctor row
  (not yet built) is contracted to watch five named primitives —
  `find_board`, `parse_frontmatter`/`split_frontmatter`, `atomic_write`, a
  git runner, a section extractor — and none of those six helper names is
  on that list, so they will not turn the row red. They are the same class
  of duplication all the same; worth the row-writer's attention when it is
  built, not a spec of its own here.
- **`edit.py`'s `split_fm` and `section_span` are not duplicates of
  `common.py`'s primitives, despite similar names.** `split_fm` returns
  the frontmatter as its own raw *lines* plus the untouched head/tail text
  — built for a round-trip rewrite (`set_key`, `del_key`, `set_body`,
  `set_title` all reassemble the file from its three pieces).
  `common.split_frontmatter`/`parse_frontmatter` return a *parsed dict*
  (and, for the latter, the title and body) — built for reading, and lossy
  of comments and exact formatting on the way in. `section_span` returns
  `(start, end)` **offsets** into the body, because `append_section` and
  `retract_answer` splice new text in at a position; `common.section`
  returns the body **text**, never a position — there is nothing in its
  API a span-consumer could call. Confirmed the shapes differ in
  `probe_core_delegate.py` rather than asserted from reading. Neither is a
  second definition of one of the five tracked primitives; both stay as
  they are.
- **The corrected claim:** the sibling PRD's own `probe_common.py` (which
  this PRD's `needs:` names) validates `prdfile._h2_sections` against
  `common.section(BODY, name, all=True, prefix=True, word=True)` with no
  `ci=False` — leaving `ci` at its default of `True`. `_h2_sections`'s
  original regex embedded `name` with no `re.I` flag, so it is
  case-**sensitive**: a body with both `## Questions` and `## questions`
  headings, queried for `"questions"`, matches only the second under the
  old code. The sibling's probe never tried a case-mismatched query, so
  the default going the wrong way passed unnoticed. This PRD's delegation
  uses `ci=False`, and `probe_core_delegate.py` carries the case-mismatch
  test that would have caught it. No spec changes at the sibling PRD — it
  is already collected — so this is recorded here as the finding it is,
  not filed as a new PRD.

## Acceptance

- [x] `collect.py`'s `section` and `git_out`, `edit.py`'s `write_atomic`,
  `prdfile.py`'s `_h2_sections` and `specs.py`'s `section_text` each call
  `common.run_git`/`common.section`/`common.atomic_write` in one line,
  keeping their own return-or-raise shape.
  `git diff --stat`: `collect.py | 19 +++++++------------`, `edit.py | 12
  ++++++++----`, `prdfile.py | 9 +++------`, `specs.py | 7 ++-----` — a net
  reduction in every file, no new duplicate logic added.
- [x] A probe reproduces, for each delegated function, its pre-edit
  success and failure/edge shape from the new one-line call.
  `PEARDE_ROOT=<lane> python3 probe/probe_core_delegate.py`: `PASS: every
  delegated caller in the core board modules reproduced its pre-edit
  contract`. Mutation-tested on the second pass, one delegation at a time
  in the lane and restored after each: `specs.py chomp=True→False` →
  `FAIL: 2 mismatch(es)`; `prdfile.py ci=False→True` → `FAIL: 2
  mismatch(es)`; `collect.py ci=False→True` → `FAIL: 1 mismatch(es)`.
  `edit.py`'s `common.atomic_write(path, text)` → a plain
  `open(path,"w").write(text)` passed — the probe read only the bytes and
  the absent `.tmp`, both of which a truncating write also gives. Three
  assertions added (inode changes across an overwrite, `None` return,
  post-overwrite contents); the same mutation now gives `FAIL: 1
  mismatch(es) - write_atomic renames over rather than truncating in
  place: got False want True`.
- [x] The sibling `common-py-gains-a-git-runner-and-a-section-extractor`
  PRD's own probe still passes against the edited tree.
  `python3 <that PRD>/probe/probe_common.py`: `PASS: every checked caller
  contract reproduced`.
- [x] `resources/index.py check` and `resources/doctor.sh` show no new
  failures against the pre-edit baseline.
  `index.py check`: identical 3-line output before and after. `doctor.sh`:
  only two pre-existing memo-reference line numbers shifting and the
  `statusline` row's own dirty-file count differ. Re-measured on the second
  pass against a real pre-edit tree (the lane's four footprint files
  restored from `HEAD`, run, then restored): all 21 board harnesses that
  name a footprint path exit identically before and after — `0 1 0 0 0 0 0
  0 0 1 1 0 1 1 1 0 0 1 0 0 0`, the same seven red before the first edit;
  every 21 doctor row status identical; the only harness count that moved
  is `every-module-finds-its-siblings-by-one-rule`'s `ok 32 modules open
  with the one rule` → `ok 33`, which is this spec's own `edit.py` gaining
  the `pearde_path` rule, and its row was `ok` on both sides.

## Verify and Proof

```sh
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-core-board-modules-delegate-to-common/probe/probe_core_delegate.py
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/common-py-gains-a-git-runner-and-a-section-extractor/probe/probe_common.py
python3 -c "import ast
for f in ('resources/board/collect.py', 'resources/board/edit.py', 'resources/board/prdfile.py', 'resources/board/specs.py'):
    ast.parse(open(f).read())
print('all four parse')"
```
