---
state: "done"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/jev.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - '**'
commit: "78b7fe480b0f7f7a1cd6f430aaec1cc1bee48ed2"
---

# jev answers a declared judgement with a gated verdict and fails open

## Outcome

`jev.ctg` exists. A cartridge calls `jev {op:"decide", point, state, cwd}`
and gets `{answers, confidence, verdict, decision_id}`, where `verdict` is
`act`, `caution` or `escalate`, taken from the gates the judgement declares.
When JEV cannot answer, the verdict is `escalate` with a reason and the
caller's existing path runs.

## Direction (2026-09-19, user)

Asked how to speed up ASP and JEV, the user chose to build in parallel. This
leaf is built and tested against a fixture `auth.jev` and does not wait for
`@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key`. The live
profile line waits for it: the base refuses to start a cartridge whose need,
optional or not, names an event nobody declares (`cartridge.ctg`
`src/host/plan.rs:324-333`).

## Decision (2026-09-19, coordinator)

- `jev.ctg` is its own repository, added as a submodule (superproject
  `ea8ecdb`), by the director's verdict. Its remote is the user's to create.
- `needs` is `auth.jev?` and `memo?`, never `asp`. A judgement is a memo of
  kind `judgement`, declared by jev, and `declare` is the op that refuses one
  without gates or a fallback.
- A non-object answer, or a declared question without a numeric confidence,
  is `escalate` whatever the gates say.
- `jev.decided` never carries the state.
- After collect, the coordinator adds `{ id = "jev", path = "jev.ctg" }` to
  the superproject's `.cartridge/init.lua` once `auth.jev` is collected, trusts
  the project straight after (a changed `init.lua` stops every `cartridge`
  command until the project is trusted), and records `just audit jev` and `just isolation` in
  `collection.md`.

The contract with `auth.jev`, the confidence rules, the timing chain and the
decision history are in `specs/spec01.md` and `review.md`; the earlier body
is `proposals/prd-before-trim.md`.

## Acceptance

- [x] The manifest declares `needs` `auth.jev?` and `memo?`, grant
      `exec: ["bun"]` only, and `jev.decided` without state, and no sibling's
      file is included.
- [x] `declare` refuses a judgement without a gate or a fallback, and the
      shipped example judgement is valid.
- [x] Named tests against a fixture `auth.jev` cover each verdict and a
      request whose weakest answer decides it.
- [x] Named tests show that an unavailable, late, empty or partial `auth.jev`
      answer and an unknown `point` each return `escalate` with a reason and
      never throw.
- [x] `README.md` and `.cartridge/help.md` exist, and help names the
      `judgement` kind.
