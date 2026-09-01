# Standdown — a duplicate round worker, dispatched from session pearde-eb

A second round worker was dispatched onto this board at ~12:48 (from session
`pearde-eb`, scoped to
`seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green`,
resuming from the 12:20 round file) while another session's round worker —
the one that rewrote `.state/round.md` at 12:56:27 and landed
`6d4ff67`/`3606a76` — was already reconciling and collecting. **This window
stood down at ~13:01 and wrote nothing to the board**: no commits, no state
transitions, no edit to `round.md`. The 12:56:27 `round.md` is the
authoritative round memory; its owed list (items 2–4: the fixtures collect
with Edits A/B, the doctor→init-seeds analyst chain, the doctor.sh:743 memo)
is uncontested.

The one fact this window adds:

- **the harness census fails under concurrent sweeps, and only then.** At
  12:51:39 this window ran
  `pearde collect graph-probe-makes-harness-sweep-unaffordable` (with the
  five `--also` workflow files). It refused at spec02's gate: census
  `7 of 46 green · 148s · 8 failed` — while THREE collects' full-board
  sweeps ran at once (this one at 12:51:39, the peer's `--dry` at 12:52:30,
  the peer's real one at 12:53:13; the sweeps also thrash the parse cache
  and restart the view daemon). The peer's collect, finishing alone after
  this one exited, passed the same gate and landed. So: census reds during
  overlapping sweeps are contention, not code — **run collects serially,
  one session at a time**, and do not chase reds a concurrent sweep
  reported.

Standdown notices were sent to sessions pearde-24, pearde-3f and pearde-23
at ~13:01; replies, if any, go to the pearde-eb main conversation.
