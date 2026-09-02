# Calling a persona

Putting one problem to one colleague, mid-pass, without switching.
@references/personas/INDEX.md is the roster. The brief is the **Consultant**
one in @references/parts/workers.md. Switching the session is a different
question — @references/parts/personas.md.

`pearde brief --consult <id> --question "<q>" [--transcript <path>]` prints
that brief filled — the id, the transcript path, the board, the repo and the
question as the user put it. Nothing is composed by hand.

**You call one yourself.** `ask <id> <question>` is the user doing what you
can already do. Reaching a colleague is ordinary work, the way dispatching a
worker is, and needs no permission.

Personas are cheap to call and expensive to become. A switch re-aims the whole
pass; a question aimed at one problem needs no switch — calling the skeptic
about one PRD gets the adversarial read without the next three passes being
adversarial.

## When to call one, unprompted

| you are about to                                                        | call       |
|--------------------------------------------------------------------------|------------|
| write `done` on work this session implemented                             | `skeptic`  |
| accept a worker's report you cannot check from inside your own frame      | `skeptic`  |
| name a user-facing thing, or decide a flow, inside an engineering pass    | `designer` |
| recommend a fork to the user that turns on something they must understand  | `mentor`   |
| work a field the roster does not cover, and it governs the decision        | `persona create <topic>` first, then call it |

- **Call on the decision you are about to defend**, not on every transition. A
  call whose purpose you cannot state in one sentence is a call you do not need.
- **Never call the persona you are wearing.** Asking yourself in a second
  context is not a second opinion.

## It is a conversation

- **Keep the one you called.** It holds the exchange — what it read, what you
  already told it, what it ruled out. Follow up in the same thread; under an
  agent that names its subagents, a message to the one you have.
- **A second dispatch is a second colleague**, with no memory of the first.
  Sometimes you want exactly that — a genuinely independent read — and never a
  substitute for a follow-up.
- **Push back.** A consultant that hedges was asked a hedged question.
- **It can ask you first.** A clarifying question back is it working. Answer
  it; never re-dispatch over it.
- **Two or three exchanges settle it.** Past that the disagreement is real and
  belongs to the user — one question, per @references/drill.md, both readings
  named.

## What a call cannot do

- **It writes nothing.** No state, no `prd.md`, no spec, no code, no commit. A
  consultant wanting a file changed says so, and you decide — one writer per
  file, @references/parts/roles.md.
- **It fetches its own context.** Hand it the session's `transcript_path`, the
  board path and the question, nothing else. A summary of the problem hands it
  your reading of the problem, the thing you were asking someone else for.
- **Your persona does not move**, and the pass line still carries yours. A
  consultant never prints a `▸ … · as <id>` line — that form is what the
  status line reads, and one from a consultant shows a persona nobody wears.

## Relaying

Say who you asked and what they said — `skeptic: <the answer>` — then answer
in your own voice if you disagree. An answer laundered into the pass as your
own view costs the user two readings and gives them one. A call that changed
nothing is still worth one line: a skeptic that found nothing is evidence, and
dropping it makes the next `done` look unchecked.
