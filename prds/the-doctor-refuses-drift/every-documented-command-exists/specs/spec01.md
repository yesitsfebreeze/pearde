---
complexity: 20
footprint:
  - resources/claims.py
---

# spec01 — the checker: three claims, one direction

`resources/claims.py` reads every claim a document makes about a name and
checks it against the thing that answers it: a `pearde <verb>` against
`pearde.py`'s commands, a `key:` against the registry spec02 adds, a
`memos/<slug>.md` cited in code against the board's memos. One direction only
— something documented that does not exist. The reverse, a command nobody
documented, is a judgement and is not reported.

The whole build stands at `probe/claims.py`; it runs green against the tree
and reports nine drifted names. What is left is to land it as
`resources/claims.py` and to keep its two anti-noise rules, which are the
reason the file is not a grep:

- **Prose is not a claim.** `the pearde board`, `is pearde up to date` and
  `pearde already ships` are English. A command claim is read only from a
  backtick span, a fenced block, or a skill's `description:` — and inside a
  `description:` only the slash form `/pearde <verb>`, because the rest of
  that field is prose about the board. Without this rule the check reports 19
  misses of which 16 are sentences.
- **A citation wraps.** A long memo slug breaks across lines in prose
  (`a-long-` newline `slug.md`) and across a Python string concatenation
  (`"a-long-"` newline `"slug.md"`). `fold` rejoins them and keeps the line
  each character came from, so `refuse.py`'s wrapped citation of
  `a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work`
  is recognised as the real memo it is rather than reported as a phantom.

A key claim is read from a backtick span holding `key: value` within 140
characters of a mention of `settings.md` — the window is what keeps `state:`,
`needs:` and `verify:`, backticked all over this repo, out of the settings
check. `references/parts/contract.md` is read whole instead, every key in it
being a frontmatter claim by definition.

A document that names a command on purpose that does not exist says so with
`<!-- claims: ignore -->` on the line or the line above it.

## Acceptance

- [x] `python3 resources/claims.py check <board>` prints one line per miss as `file:line: <what> — <why>`, prints nothing and exits 0 when clean, exits 1 when not
- [x] `python3 resources/claims.py verbs` prints every name `pearde` answers, read from `pearde.py`'s `FORWARD` and `discover()` and not from `pearde help`'s printed lines
- [x] `python3 resources/claims.py keys` prints the registry, one `settings <key>` or `frontmatter <key>` per line
- [x] Planting `Run ` backtick `pearde frobnicate` backtick in any `references/**/*.md` adds exactly one line naming that file and line; removing it returns the count to what it was
- [x] Planting a backtick span `frobnicate: off` beside a mention of `settings.md` adds exactly one settings line; planting `.pearde/memos/no-such-memo-at-all.md` in any `resources/**/*.py` adds exactly one memo line
- [x] Adding `<!-- claims: ignore -->` to a planted line removes its report and nothing else
- [x] No line is reported for `the pearde board`, `is pearde up to date`, `pearde already` or any other prose form outside a backtick span, a fenced block or a `description:`
- [x] `resources/board/refuse.py`'s line-wrapped citation of the shared-checkout memo is not reported, and a wrapped slug that names no memo is reported at the line it starts on
- [x] The file imports `common` for `read_text` and `find_board` and `memos` for `scan`, defining neither itself

## Verify and Proof

```sh
python3 resources/claims.py verbs | wc -l
python3 resources/claims.py keys | wc -l
rc=0; python3 resources/claims.py check > /dev/null || rc=$?; echo "exit=$rc"
B=$(python3 resources/claims.py check | wc -l || true)
printf '\nRun `pearde frobnicate`.\n' >> references/parts/doctor.md
A=$(python3 resources/claims.py check | wc -l || true); [ "$A" = "$((B+1))" ] || echo FAIL plant
printf '\nRun `pearde frobnicate`. <!-- claims: ignore -->\n' >> references/parts/doctor.md
C=$(python3 resources/claims.py check | wc -l || true); [ "$C" = "$A" ] || echo FAIL ignore
git checkout -- references/parts/doctor.md
[ "$(python3 resources/claims.py check | wc -l || true)" = "$B" ] || echo FAIL restore
```
