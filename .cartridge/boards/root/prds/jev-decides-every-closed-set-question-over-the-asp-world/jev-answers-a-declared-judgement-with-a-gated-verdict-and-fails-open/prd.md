---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
needs:
  - '@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key'
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - 'jev.ctg/**'
  - '.cartridge/init.lua'
  - '.cartridge/justfile'
  - '.cartridge/memos/routine/cartridge-development.md'
---

# jev answers a declared judgement with a gated verdict and fails open

## Outcome

`jev.ctg` exists. A cartridge calls
`jev {op:"decide", point, state}` and gets
`{answers, confidence, verdict, decision_id}`, where `verdict` is `act`,
`caution` or `escalate`, taken from the gates the judgement declares. When
JEV cannot answer, the verdict is `escalate` and the caller's existing path
runs.

## Decision (2026-09-19, coordinator)

- The cartridge is TypeScript on bun, laid out like `web.ctg`, which is the
  smallest complete cartridge (323 lines).
- A `judgement` memo holds `questions` in the API's own shape, `gates`
  (`act` and `escalate` thresholds per question) and `fallback`. The
  confidence of a request with several questions is that of its least
  certain answer, which is the rule in TypeSafe's function-calling cookbook.
- Every decision publishes `jev.decided`
  `{decision_id, point, verdict, confidence, answers, usage, latency_ms}`.
  The event never carries the state, which may hold content that must not be
  retained.
- `jev.ctg` starts as a plain directory tracked by the superproject, the way
  `web.ctg` does (`3dba7f2`), and not as a submodule (2026-09-19,
  coordinator-b0). A submodule needs the remote
  `github.com/yesitsfebreeze/jev.ctg`, which does not exist and which only the
  user may create. `just audit` and `just isolation` find cartridges by
  listing `*.ctg` directories, so both see a plain directory. A later PRD
  splits it out with `git subtree split` if it needs its own history. The user
  was asked and may overrule this before the claim. No `jev` board exists
  until then, because a board's `repo` must be a git repository; the two
  sibling PRDs stay on the root board and serialise on `jev.ctg/**`.
- `needs` is `auth.jev?` and `memo?`, both optional, and never `asp`
  (2026-09-19, coordinator-b0, from the analyst's pre-draft). `asp` is the
  base's own service key (`cartridge.ctg/docs/asp.txt`, REACHING IT;
  `src/loader/document.rs:183`), it is reached without a need, and this leaf
  never calls it. A judgement is a memo, so jev needs `memo`, and
  `decide` takes the caller's `cwd` like every other caller of the memo
  service. An optional need is how fail-open is declared; `live.ctg` already
  declares `memo?`.
- memo enforces nothing about a kind's fields, and `memo.ctg` is outside this
  footprint. The refusal in Acceptance box 2 is therefore
  `jev {op:"declare"}`. A judgement written around that door is caught on
  read and escalates with the reason `invalid judgement`.
- `jev.decided` also carries an optional `reason`, so an escalation can be
  explained from the ring.
- A `noul` answer carries no confidence from the API; only `choice` and
  `score` do (https://docs.typesafe.ai/confidence.md: "Noul answers don't
  carry one."). jev's confidence for a `noul` is its own measure,
  `max(p, 1-p)`, which equals TypeSafe's symmetric yes/uncertain/no band on
  `p`. The docs say it is jev's measure and on a different scale from a
  `choice` confidence; a judgement that needs the API's confidence asks a
  two-option `choice` (2026-09-19, coordinator-b0, from the `auth.jev`
  analyst).
- A judgement's `questions`, and the `answers` that come back, are maps keyed
  by question id, in the API's own shape, not lists. The pre-draft spec's
  "non-empty list, each with an `id`" is revised to a map before the claim.
- jev passes `auth.jev`'s failure message through as its `reason`; that
  message already starts with a type word such as `overloaded`. jev does not
  prefix it again with `unavailable:`.
- The pre-draft spec is `proposals/spec01-draft.md`, read at superproject
  `801aa8e`, `cartridge.ctg` `7af748a` and `auth.ctg` `d875108`. It is
  revalidated against the base at claim time.
- Registration is three superproject files (2026-09-19, coordinator-b0, from
  cartridge-78's port work):
  `.cartridge/init.lua`, the owner lists in `.cartridge/justfile`'s `_fan`
  recipe, and the owner loop and `_cargo` case arm in
  `.cartridge/memos/routine/cartridge-development.md`. Without the last two,
  `just check jev` and `just test jev` do not resolve. The `init.lua` entry
  lands in the same collect as `jev.ctg/cartridge.json`, because a profile
  entry whose path has no manifest fails `just audit` for every session.
  `.cartridge/justfile` carried a foreign uncommitted edit on 2026-09-19;
  check its status before collecting.

## Start at

- `web.ctg/cartridge.json`, `web.ctg/src/main.ts`, `web.ctg/src/wire.ts`.
- `memo.ctg/src/record.rs:690-734`: a kind is declared before its
  instances.
- https://docs.typesafe.ai/confidence.md and
  https://docs.typesafe.ai/patterns/confidence-routing.md.

## Acceptance

- [ ] `jev.ctg` is a cartridge directory listed in `.cartridge/init.lua`,
      `just check jev` and `just test jev` resolve, and
      `just audit` and `just isolation` report nothing for it.
- [ ] The kind `judgement` is declared, and one example instance ships. A
      write that lacks a gate or a fallback is refused.
- [ ] Named tests against a fixture `auth.jev` cover a confidence above
      `act`, one between the gates, one below `escalate`, and a request
      whose weakest answer decides the verdict.
- [ ] Named tests show that an unavailable `auth.jev`, a timeout and an
      unknown `point` each return `escalate` with a reason, and never throw
      into the caller.
- [ ] `jev.decided` is declared in `cartridge.json`, and a named test
      asserts that it carries no state.
- [ ] `README.md` and `.cartridge/help.md` exist, and help names the
      `judgement` kind.
