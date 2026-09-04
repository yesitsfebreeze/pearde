---
state: specced
origin: requested
priority: 45
complexity: 29
blast-radius: mid
workflow: probe-then-spec
---


# the obsidian vault is opt-in

The vault preset is written by `pearde vault`, not by `init`. `obsidian-local-rest-api` is dropped — no code calls it — with its docs and the key mirroring in `init.py`; Dashboard falls back to `knowledge dashboard` text; README states the vault is an optional viewer needing Obsidian + Dataview.

## Done means

`pearde init` writes no `.obsidian`; doctor's vault row reads off, not broken, when Obsidian is absent.

## Needs

No gate.

## History

**failed, retried 2026-09-03 21:37**

**2026-09-03 21:4x — the claim is dead; the report is the analyst's**

The report on disk is the analyst's SPECCED (mtime earlier than the claim's
`since`), so no implementer ever returned. The worker's session was reaped —
no process on this machine holds it. The claim only reads live because its
footprint names shared files other sessions keep writing
(`silence-measures-the-workers-own-tree` names the artefact). The analyst's
work stands in `specs/`; the next implementer continues from it.

## Blocked

**2026-09-03 21:57 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `main`; 6 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `session/s62223`; 6 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `main`; 6 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `session/s62223`; 6 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `session/s62223`; 6 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 02:48 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `session/s62223`; 6 file(s) disagree:

- `references/files.md`
- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `session/s85810`; 5 file(s) disagree:

- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 04:04 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `main`; 5 file(s) disagree:

- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 04:06 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `main`; 5 file(s) disagree:

- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.

**2026-09-04 04:21 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` does not land on `main`; 5 file(s) disagree:

- `references/obsidian.md`
- `resources/board/init.py`
- `resources/board/obsidian/community-plugins.json`
- `resources/doctor.sh`
- `resources/install.sh`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/the-obsidian-vault-is-opt-in`.
