# install-fetches-nothing — analyst report

Verdict: SPECCED

Two specs, `complexity` 8 + 4. The build went all the way through: the
installer reaches no network in any mode, `--remove` deletes no bundle, and
`pearde vault` fetches what the preset is missing at the pin. Nothing in the
contract was undefined, so there is no question to put to anyone.

- `specs/spec01.md` — the fetch leaves the installer and lands behind
  `pearde vault`. `complexity: 8`, footprint `resources/install.sh`,
  `resources/board/init.py`.
- `specs/spec02.md` — every claim that the install fetches, corrected, plus
  the standing harness. `complexity: 4`, footprint `references/files.md`,
  `references/obsidian.md`, `resources/board/shared.py`,
  `resources/update.sh`.

Union of the footprints: `resources/install.sh`, `resources/board/init.py`,
`references/files.md`, `references/obsidian.md`, `resources/board/shared.py`,
`resources/update.sh`.

Workflow followed: `probe-then-spec` — it fits exactly (an open PRD, contract
to specs, this being its second pass on the same route). No new workflow, no
new atomic.

## What the build did

Pass one had already cut the `PLUGIN_DIR`/`PLUGINS` block out of
`resources/install.sh` (47 lines, the only `curl` in the repo) and moved the
pins into `resources/board/init.py` as `OBSIDIAN_BUNDLES`, with
`bundle_state`, `fetch_bundle`, `ensure_bundles` and `copy_bundles`, called
from `cmd_vault` before anything is copied or registered. This pass re-ran it,
closed the two claims it had left standing, and turned the probe into a harness
that can fail.

Measured, in the lane
`.pearde/.lanes/the-tree-holds-only-what-a-board-uses-install-fetches-nothing`:

- `install.sh --apply <scratch>` behind a dead proxy (`http_proxy`,
  `https_proxy`, `ALL_PROXY` all `127.0.0.1:1`) exits 0, builds 19 skill
  folders, prints no fetch line.
- `ensure_bundles(("dataview",))` against an empty preset returns
  `(['dataview'], [])` and `bundle_state` goes `ok`; the second call returns
  `([], [])`.
- `copy_bundles` fills a vault with no plugin directory once and leaves an
  installed plugin alone.
- `pearde init` on a scratch repo, then `pearde vault --dry`, both run clean.
- `probe/verify.sh`: `7 passed, 0 failed` on the lane; exit 1 with six
  failures against the unpatched checkout.
- `resources/index.py check` and `resources/memos.py check`: unchanged from the
  baseline taken before the edits (the four index problems below are HEAD's,
  not this PRD's).
- Both spec verify blocks run green in the lane under `bash -e -o pipefail`
  with stdin closed, and both exit 1 on the unpatched checkout.
- `specs.check_spec` on both files: no refusal, no warning.

Two claims this pass closed, both drift the change itself created:

- `references/files.md` row for `@resources/board/init.py` still said the
  preset was one "the install fetched" and named "a bundle the install never
  fetched". Pass one had corrected the neighbouring `@resources/board/obsidian/`
  row and missed this one.
- `resources/update.sh`'s row filter carried `# agents and plugins report too`.
  `install.sh` emits no plugin row any more, so the comment named a row that
  cannot appear.

## Findings

**A fetch inside a lane detaches that lane from the shared store.** The
preset's `main.js`, `manifest.json` and `styles.css` are shared-store symlinks
(`resources/board/shared.py`, three glob `Share` rows). `fetch_bundle` renames a
real file over that path, so the lane silently stops sharing and holds its own
2.4 MB copy until `pearde share apply` runs again. Seen for real: the first
probe run un-shared `dataview` in this lane and `pearde share apply` re-merged
all three files. The harness now repoints `initlib.OBSIDIAN_PRESET` at a temp
directory so it never writes through the real preset, and spec01 says a person
who runs `pearde vault` inside a lane should re-run `pearde share apply`. The
same is true of the old `install.sh` fetch, so this is not a regression — but it
is now reachable from a verb people run often, which the installer was not.

**A sibling on this board writes the same file.**
`the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in` is
`analyzing` at the same time and its contract is `resources/board/init.py` too —
the vault preset moves out of `init`, and `obsidian-local-rest-api` is dropped
entirely, which would delete one of the two rows of `OBSIDIAN_BUNDLES` spec01
adds. The two footprints are not disjoint and the two implementers must not run
at once. Not something either PRD can fix from inside itself.

**Four index problems predate this PRD.** `resources/index.py check` on the
clean checkout at `f8968fe` reports: `resources/common.py` on disk with no row
in `references/files.md`; `references/files.md` and the `@@view` keyword both
naming `@resources/board/hotreload-test.js`, deleted in `b1d3f5d`; and
`references/parts/commits.md` referencing a memo that is not on disk. That is
the sibling `the-documented-board-matches-the-code`'s contract, not this one's.

**Doctor rows broken before this PRD and untouched by it:** `vault` (the board
is `.pearde`, a dot-segment), `origin` (5 derived PRDs with no `from:`),
`health` (ranking 29 commits behind), `knowledge` (`graph.json` behind two
notes), `questions` (one `## Answers` with no `## Questions` above it, in
`resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule`).

**No grammar gap and no knowledge gap.** Every word in the contract —
`preset`, `bundle`, `lane`, `share` — is either in the vocabulary or plain
English. `knowledge.py query` on the contract returned 90 hits, 23 strong, and
enqueued nothing into `.pearde/wiki/pending/`. Nothing was learned outside this
repo, so nothing was written back with `knowledge.py remember`.

**A job that recurs and already has its file.** "Move a step out of one verb
and into the verb that actually wants it, then chase every claim that named the
old one" is the shape of `correct-a-documented-claim` bolted onto
`probe-then-spec`; both files exist and neither needed changing.

## Reasoning for the scores

`complexity: 12` — the whole change is one deletion (47 shell lines, no
replacement) and one relocation of a pinned download into a module that already
owns the preset. The specs sum to 12 and the work is already standing in the
lane; what is left is landing it.

`blast-radius: mid` — `install.sh` is the first command anyone runs and
`init.py`'s `write_obsidian` is called by `init`, `upgrade` and `vault` alike,
so a mistake here is felt on a fresh machine. It is `mid` and not `high` because
nothing in the loop, the board or the view reads any of it: a broken bundle
fetch costs a person their Dataview views, not their board.

## Scores

complexity: 12
blast-radius: mid
workflow: probe-then-spec
