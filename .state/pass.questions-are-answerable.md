# round — questions are answerable: per-question submit/reopen, format enforced

Not a board round. A direct feature request from the user, worked in
`resources/board/`, `resources/questions.py` and the format prose.
Moved out of round.md — the dispatcher's round worker rewrites that whole.

The user asked directly, mid-session, for the question-flow rework; this lane
edited `view.js`, `view.css`, `viewtest.js`, `serve.py`, `edit.py`,
`questions.py` and the format prose. **That overlaps the ⌘K palette lane's
claim on three files** — every edit here applied cleanly against the disk
state at write time, and `viewtest --example` and the served master both pass
49/49 after; palette lane, rebase on disk before your next write.

What changed, whole:

- **Per-question submit and reopen.** `questionsHTML` gives every question
  its own `answer Qn` and (once answered) `reopen Qn`; the round-level
  "answer & reopen" and "take the recommended" bulk submits are gone from
  both the inspector and the asks cards (`collectAnswers`/`takeRecommended`
  deleted). The answered panel's rows carry `reopen` too.
- **Reopen is a write.** `edit.py retract_answer(path, qid)` removes the
  `**Qn**` block under `## Answers` (heading too when emptied); `/edit`
  accepts `"retract"`; the view's `reopenOne` sends it plus
  `state: question`. Round-tripped against the live daemon: append+retract
  restores the file byte-identical.
- **Unaskable cards say so.** A round that does not parse, a parked PRD with
  no round, and a `blocked` PRD with neither `## Blocked` nor a round get a
  `.qbad` notice plus "send back — rewrite as questions", which replies under
  `## Answers` and reopens — no more PRD-body dumps in asks.
- **The checker grades the format.** `questions.py`: open questions must
  carry prepared answers, exactly three, recommended first; `blocked` with no
  wall written is reported. drill.md/template/view.md/doctor.md updated to
  "three answers, best first, recommended is answer 1".
- **Masonry + scroll.** `#asks` and `#memos` are CSS columns
  (`break-inside:avoid`), not grids; `.ask2 .q` and `.memo pre` clip instead
  of scrolling and open on click; `#asks textarea:not(:focus)` does not
  scroll.

Owed by nobody: the three master-board blocked cards trace to prose `needs:`
on `@model/phase-8` and `@shared/rename-conserved-to-shared` (checker now
names both) — fixing those files is member-board work, not this lane's.
