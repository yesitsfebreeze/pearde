Verdict: SPECCED

# Report — pending gets an expiry, not a decree

Built the whole contract in `resources/knowledge.py`: `CONFIG["pending_expiry_days"]`
(default 14), `expires:` written by `enqueue`, `pending_expiry_date()` and
`archive_expired_pending()`, `query` running the archive last and naming
what it moves, `doctor` flagging only a row past its own expiry and still
un-archived, and a `keep:` exemption. Updated the board seed
(`resources/board/knowledge/WORKFLOW.md`, a new `pending/.expired/_index.md`
marker) and the docs (`references/knowledge.md`, `references/files.md`) to
match. Verified with a new `probe/verify.sh` (11/11 green against this
build, 3/11 against the unmodified tool — not vacuous). One spec, `spec01`,
covers it whole; see `## What already stands` there for the full list.

## IMPORTANT — a side effect this pass caused, not a manual edit

While checking `spec01.md`'s format I ran `python3 resources/pearde.py
specced pending-gets-an-expiry-not-a-decree` **without `--check` or
`--dry`**, not realizing that verb performs the real transition rather than
previewing it. It already wrote `prd.md`: `state: specced`,
`complexity: 15`, and removed the `claim:` key. `blast-radius:` is still
empty — I did not pass `--blast`, and `resources/board/specs.py`'s
`SPECCED_FROM = ("analyzing",)` now refuses a second run from `specced`, so
neither I nor a normal `pearde collect --report` can set it through that
verb any more. `.pearde/prds/` is untracked in the board's own git repo, so
nothing landed in history — but the state on disk is real. I did not try to
revert it myself: the brief forbids editing frontmatter, and no command
moves `specced` back to `analyzing`. The complexity and footprint this
pre-empted transition wrote match this report's own `spec01` exactly, so
the only outstanding repair is `blast-radius: mid` (reasoning below) —
likely a direct `edit.set_key` on `prd.md`, or whatever the orchestrator's
own tooling allows from here. `pearde collect` on this PRD will refuse
rather than silently double-apply; that refusal is expected, not a new
defect.

## Other findings (not this PRD's scope, not fixed)

- The contract's own prose is internally inconsistent: "The change" section
  names `pending/.expired/` while "Done when" says "`pending/.absorbed/`-style
  storage" for the same thing, and "The change" names the knob
  `pending-expiry-days` while "Done when" shortens it to `pending-expiry: 0`.
  Built to the more specific, repeated spelling (`pending_expiry_days`,
  `.expired/`, underscored to match the codebase's existing
  `auto_enqueue` / `min_sources_per_conclusion` convention) since no tool
  read either literal hyphenated key before this pass.
- The mandatory `knowledge.py query` for this PRD's own question returned
  "103 hit(s), 103 strong" with every top result irrelevant to pending
  expiry — `score_note`'s bag-of-words scoring appears to count nearly
  every note as a "strong" hit regardless of topic, so a real gap never
  auto-enqueues (no new file appeared under `wiki/pending/`). Not this
  PRD's contract; a defect in `query`'s relevance, not in pending's expiry.

## Scores

complexity: 15
blast-radius: mid
workflow: probe-then-spec
