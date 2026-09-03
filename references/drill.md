# Drilldown

Interview the user until the understanding is shared; record it as a **PRD
tree**, every decision branching into the decisions hanging off it.

## One pass asks the whole frontier

The **frontier** is every decision whose prerequisites are settled — askable
now without guessing at answers not yet heard.

1. Compute the frontier.
2. Ask all of it in one pass, numbered, three prepared answers each.
3. Wait for the user's picks — or their own words, equally an answer.
4. Settled decisions push the frontier outward. Recompute and repeat.
5. Done when the frontier is empty — every branch visited, nothing assumed.
   Do not act until the user confirms the shared understanding.

## The pass maps onto the ask-user-question mechanism

The **header** is the `### Qn:` title, the **question** is the fork, the
**three options** are the prepared answers with their labels, and the
free-text choice is *write your own*. Without such a mechanism, print the pass
in the same words, *or write your own* as the fourth line.

The HTML comment under the third answer is the technical anchor — the files,
the slug, the spec the answer lands in. The orchestrator reads it; the checker
never sees it, the view strips it, nothing shown to a person carries it.

Mapped here: @references/parts/loop.md carries the seven commands only, under
a 120-line cap.

## A question is a fork, never a briefing

**Two sentences, then the question mark** — what is being chosen, and what
changes for the person answering. A question restating the PRD body is not a
question; the user has the PRD.

Every question carries **exactly three prepared answers**, each **one plain
sentence of what they get**, never how the work is done:

- A complete decision — picking one settles the question.
- Three genuinely different outcomes, not three phrasings of one.
- The best first, marked `(recommended)`; the view pre-selects answer 1.
- Writing them is your work; the user's is one keypress, or their own
  sentence.
- Last line, always: **or write your own** — numbering for the three readers,
  words for the person.

### What a question may never say

For the person who asked, not the orchestrator — fork, answer labels, answer
text:

| never                                    | because                                                    |
|------------------------------------------|------------------------------------------------------------|
| a backtick, a path, a file extension     | the reader has no tree open                                |
| a PRD slug, a `Q<n>` cross-reference     | a ticket number to an outsider                             |
| board vocabulary — states, frontmatter keys, worker or persona words | the orchestrator's, not theirs |
| over 60 words in the fork, 25 in an answer | past that, a briefing                                    |
| "should we also…", a fact a build could find | dispatched, never asked — *Facts vs decisions*          |

`pearde release <prd> question` runs `python3 @resources/questions.py check
[board]`: one line per row it catches, naming the word, and a failing pass
refused rather than written.

Pass format — in the PRD's `## Questions`, in the pass put to the user, parsed
by the view:

```
### Q1: <question title>

<the fork, two sentences, ending in "?">

1. **<label>** — <complete answer, paste-ready as the decision> (recommended)
2. **<label>** — <a genuinely different complete answer>
3. **<label>** — <a third direction, not a compromise of 1 and 2>
```

Worked:

```
### Q1: What the page shows first

You are choosing what a person sees first when they open the board: the work
in progress, or the questions waiting on them. Whichever is first is what they
will act on; the other needs a click?

1. **Questions first** — the page opens on what is waiting on you; the work is one click away. (recommended)
2. **Work first** — the page opens on what is happening; your questions are one click away.
3. **Ask each time** — the page remembers whichever you opened last.

<!-- for the board: serve.py `/` default route; the-page-shows-the-pass spec02 -->
```

Answer format under `## Answers`, numbers matching:

```
**Q1** — <the picked option's text verbatim, or the user's own words>
```

The view adds a stamp — `**Q1** *(answered 2026-08-28 14:22)* — …` — and
orders its answered panel by it; optional at a terminal.

## An empty `## Questions` or `## Answers` heading is a bug

`## Questions` says a pass waits on the user, `## Answers` says one came back;
left empty, the first stops the board on nothing and the second reads as
answered. **Write a heading when it has content, delete it when it does not.**
An
`## Answers` with no `## Questions` above answers a question nobody wrote
down; a parked PRD with no pass never says what is asked — both look, from
outside, like a board with nothing to ask.

The same checker, in `doctor`'s `questions` row, also reports:

- a heading with nothing under it, a question that asks nothing
- one with no prepared answers, or more or fewer than three
- one whose recommended answer is not first, or missing
- an answer to nothing, a parked PRD that never asked

An answered pass is history, left alone.

## A blocked board is a drill already written down

Two entry points, both in @references/parts/loop.md:

| entry point | trigger | the pass |
|---|---|---|
| step 8 | nothing dispatchable — every PRD left waits on a person | one drill over all of them, never a report naming them |
| the second entry point — `pearde scan` prints the **drill** section | more than one unanswered question, headed `asking N over M PRDs` | opens on that drill first, though the board still moves |

- The drill is the orchestrator's: a worker has no user to ask.
- `pearde claim` refuses with `asking N — drill first` until the questions
  are out, on the PRDs a question can reshape: the asker, its ancestors, its
  descendants, what `needs:` one of them.
- The rest dispatches first, running while the user answers.
- One standing question is not a gate — put as any pass is; zero prints
  nothing.

Pass one's frontier is the board itself: every unanswered `## Questions`,
every PRD parked with no pass, every `refine` with no usable split,
every `failed`, every `blocked` only a person can land.

- **One pass for the board, never one per PRD.** Five stuck PRDs are one
  numbered pass.
- **A question already out is carried, not re-put** — `## Asked` in
  `.pearde/.state/pass.md` is what is out. Widen: ask what the stalled
  question depends on; a frontier entirely out ends the pass.
- **Answers go back where they were asked** — `## Answers` in each PRD,
  numbers matching, then `open`; a `refine` answer becomes children, per step
  3 of the loop.

The tree below is for a drill from a request, not a board already holding
one.

## Facts vs decisions

| kind | whose job | how |
|---|---|---|
| **fact** | yours | dispatch a worker — never ask for what you could look up |
| **decision** | the user's | put it to them and wait |

Never block on a fact: a running exploration is an unsettled prerequisite, so
only the questions downstream wait — ask the rest now.

## Output: a wide tree, written through the commands

The board's own shape, per @references/parts/board.md: one directory per
decision holding a `prd.md`, its own decisions as subdirectories, never by
hand. Root: `pearde add "<title>" --body -`, the contract on stdin. Branch:
`pearde refine <prd> < split`, a `## Split` table of the child decisions
(`| child | contract | needs |`) per level. Every PRD arrives `state: open`
from the template; a hand-made `state:` is the edit
@references/parts/guard.md refuses.

**Wide, not deep.** Every branch is dispatched the moment its gates clear,
nothing caps how many run at once, and the tree's shape is the build's speed.

- Siblings with `—` in the `needs` column run together.
- A `needs` only where a child consumes what a sibling makes.
- Siblings own disjoint files — split by what each owns, never by phase.
- Children forming one chain are one branch with steps; `pearde refine` says
  so.
- Ask which decisions are independent first: those are the siblings.

Attach a workflow as the tree is written: `python3 @resources/workflows.py
list` is the library; where a workflow's `## Use when` fits a branch,
write `workflow: <slug>` on that child, handing whoever takes it the route. A branch nothing
fits carries no key — the brief alone is honest. A new workflow is the
analyst's, at spec time — `## Route` in its report, `runs: 0` from `specced` —
never the drill's.
