# The report

The board's one document written for a person. Its reader — whoever the work
is for, reading fast, never having seen the board — wants what is planned,
what is in progress, and what is stuck or waiting on them.

## One state, not a log

- **One file.** `.pearde/report.md`, next to `settings.md`, parsed by
  nothing. With no board in scope, write the text and say where it goes.
- **Rewritten whole.** Never appended, never dated, never a section per pass —
  today only; git holds every earlier state.
- **Written on demand, and at the end of a pass that moved anything** —
  @references/parts/loop.md step 7.

## Human, not agent

The board's own vocabulary is the failure mode; none of it survives:

| never write            | write instead                                  |
|------------------------|-------------------------------------------------|
| a PRD directory name   | plain words — "the login screen"                 |
| `specced`, `claimed`, `refine` | what that means for the reader            |
| `complexity`, weights, `priority` | "big", "small", "next"               |
| `origin: derived`      | "we found we also need"                          |
| a percentage of weight | one plain fraction, in the lead, or nothing      |

- **Prose, lists, or one table per section.** Whichever is shorter.
- **Present tense, current state.** Not the story of arriving at it.
- **Every entry says what the reader gets** — or what its absence costs.
- **Fits one screen.** Past six entries, a table — or a summary with the tail
  counted: "and four smaller cleanups".

## Shape

@references/templates/report.md is the file. Four parts:

1. **A lead** — two or three sentences: where the work stands, what landed
   since it last mattered, a fraction if it helps.
2. **Planned** — not started, ordered as the board would run it: first entry,
   next thing to happen.
3. **In work** — someone or something is on it now.
4. **Undecided or failing** — needs a decision, waits on a named event, or was
   tried and failed; each entry names the one thing that moves it.

## What goes where

Every PRD lands in exactly one section; a PRD in none is a bug.

| state       | section                | written as                            |
|-------------|------------------------|----------------------------------------|
| `done`      | the lead               | what now exists, in one clause         |
| `analyzing` | In work                | "being worked out"                     |
| `claimed`   | In work                | "being built"                          |
| `specced`   | Planned, first         | "ready to start"                       |
| `open`      | Planned                | plain, no qualifier                    |
| `refine`    | Planned                | "too big as one piece — being split"   |
| `question`  | Undecided or failing   | the decision itself, as a question     |
| `blocked`   | Undecided or failing   | "waiting on <the event>" — name it     |
| `failed`    | Undecided or failing   | what was tried, and what it needs      |
| parked      | one line, at the end   | "set aside" — @references/parts/states.md |

- **Questions are the point of the section.** A reader answering three
  unblocks the board, so each is a real fork with its choices spelled out, not
  "needs input on auth".
- `blocked` and `failed` read differently: one is waiting, one went wrong.
  Never merge the wording.
- On a master board, group by project — the member's name as the reader knows
  it, not its path. @references/parts/master.md.
