# Report — the vault ignores the paths the board writes

## Verdict: DONE

5 of 5 boxes ticked in `specs/spec01.md`. One spec. Verify block exits 0;
negative-tested to exit 1.

## What I changed

One line, in `.obsidian/app.json`: `"graphify-out/"` → `".pearde/graphify/"`.
`resources/board/obsidian/app.json` I did not touch — a concurrent writer had
already corrected it at 18:21, and its value was right.

## Re-verification of the four boxes the analyst ticked

| box | as ticked | on disk | action |
|-----|-----------|---------|--------|
| 1 template list | named `graphify-out/` | dead path | **was false** — corrected |
| 2 lists identical | claimed identical | differed on entry 2 | **was false** — converged |
| 3 all entries exist | exempted `graphify-out/` | exemption bogus | **was false** — now all 10 exist, no exemption |
| 4 no old-layout paths | claimed clean | `graphify-out/` is one | **was false** — now clean |

All four were stale by the time I ran. Box 2 broke because a second writer
edited the template but not the live file, leaving the pair disagreeing —
the exact condition box 2 asserts against.

`graphify-out/` is not a sometimes-absent regenerable path, which is what the
analyst's box-3 exemption claimed. It is never produced at all:
`resources/graph/graph.sh:51` sets `GRAPHIFY_OUT="$FOLDER_ABS/.pearde/graphify"`,
redirecting graphify's own default away from it. `.pearde/graphify/` is live
on disk (graph.json, graph.html, GRAPH_REPORT.md, written 18:21).

Proof, both files, after the fix:

```
OK   .claude/                            OK   .pearde/wiki/Dashboard.report.md
OK   .pearde/graphify/                   OK   .pearde/wiki/graphs/
OK   .pearde/.state/                     OK   .pearde/wiki/pending/
OK   .pearde/.claims/                    OK   .pearde/wiki/sources/.absorbed/
OK   .pearde/wiki/.graphify/             OK   resources/board/state/
OK  10 entries, both files, all present
```

Both files byte-identical: sha256 `d86ad1b5e8fe6e36c365c45fcb66f2dee8cc884a50f37a835edbb0e501952eb2`.

## Box 5 — closed against the running app, not by eye

The box asked a person to open the vault and look. I closed it from the app's
own index instead, which is stronger and repeatable.
`~/Library/Application Support/obsidian/obsidian.json` registers
`/Users/feb/dev/infra/pearde` as a vault with `open: true`; Obsidian is
running (pid 52579). Its IndexedDB index holds this vault's files
(`index.md`, `README.md`, `references/*.md`) and:

| path | hits in the live index |
|------|------------------------|
| `resources/board/knowledge/` (non-dot, not ignored) | indexed |
| `resources/board/state` (non-dot, ignored) | 0 |
| `.pearde/` | 0 |
| `.claude/` | 0 |

A non-dot sibling indexed while the ignored non-dot path beside it is not is
the filter biting — dot-folder hiding cannot explain that pair. No human
opened the file explorer; if the board requires a human's eye specifically,
this box is the machine equivalent, not that.

Caveat, stated plainly: the index was last written 16:05, before the list was
edited. It therefore proves the mechanism honours the list, and proves the
ignored paths are absent right now. It does not prove the app has re-read the
two entries changed after 16:05.

## Verify block was not a gate — fixed

The block as written ended on a `python3` print loop that exits 0 whatever it
finds, and `collect` reads the last command's exit code. Any failure would
have reported success. Replaced with a single heredoc that compares both
lists to the expected ten, checks each path exists, and
`sys.exit(1 if bad else 0)`. Confirmed: exit 0 as the tree stands, exit 1 when
fed one bogus expected entry.

## Finding: the PRD body is wrong about `resources/board/state/`

Kept the entry, per instruction. Recording the evidence: `resources/guard.py`
defaults `STATE` to `board/state/guard` under the code root, overridable only
by `PEARDE_GUARD_STATE`, and the directory is live. The PRD's "no longer
exists as a board path at all" is false. Not fixed — the PRD body is not mine.
Whether guard.py's default should move under `.pearde/` is a separate PRD.

## Finding: two more stale ignore lists, both outside my footprint

Neither touched.

1. `resources/board/.obsidian/app.json` — a **third** ignore list. `resources/board/`
   is itself a vault. Its four entries all name `vicky/…`, none of which
   exists:
   ```
   MISS vicky/sources/.absorbed/   MISS vicky/graphs/
   MISS vicky/pending/             MISS vicky/.graphify/
   ```
   The PRD's premise, "Two files carry the same list," undercounts by one.
2. `resources/board/obsidian/graph.json` still filters the old top-level
   layout: `-path:"prds/knowledge/.graphify" -path:"prds/knowledge/graphs"
   -path:"prds/knowledge/pending"`. Same defect class as this PRD, one file
   over. It is already modified in the working tree, so someone is on it.

## Note: the live file is gitignored

`.gitignore:7` holds `.obsidian/`, so my one-line fix is machine-local and
`collect` will see only `resources/board/obsidian/app.json` change. That is
correct — `resources/board/init.py`'s `write_obsidian` copies the preset into
every new board's `.obsidian/`, so the template is what governs, and the live
file is this machine's own copy.

## Repo gate

`bash resources/doctor.sh`: `plugins`, `index`, `statusline`, `board`,
`vision`, `memos` ok. `skills`, `guard`, `origin`, `workflows` broken — all
pre-existing, none in this footprint, and doctor has no row reading either
`app.json`. Not caused by this change and not mine to fix.

## Scores

complexity: 5
blast-radius: low
workflow: none fit
