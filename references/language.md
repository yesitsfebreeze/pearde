# Language

Governs this definition, PRDs, specs, memos, and worker reports. Written in the
board `language` from `.pearde/settings.md`. Every rule holds in any language.

Reader: an agent, cold, without the conversation that produced the document.

## Rules

- **Structure over prose.** A fact set is a table, a sequence a numbered list,
  a rule set bullets. A paragraph carries an argument, nothing else.
- **One idea per sentence.** A comma joining two thoughts is two sentences.
- **Imperative.** `Set specced`, not `the state should then be set to specced`.
- **Name the thing.** The file, state, command, field — never `the relevant
  config` for `@references/templates/prd.md`.
- **Address, do not describe a path.** One file is `@<path>` from the repo
  root, a whole feature `@@<keyword>`, scoped in `@index.md`. Write
  `@@statusline`, not `the status line script and the progress part`.
- **`@@` where the reader needs the scope, `@` where they need the file.** A
  brief, a handle, an install step says `@@view`; a rule citing one table says
  `@references/parts/progress.md`.
- **No hedging.** No `might`, `probably`, `consider`. A real choice names who
  chooses and when.
- **No meta.** No `this section explains`, no `as mentioned above`.
- **No legacy.** Present tense only. No former names, no migration notes, no
  deprecated aliases. History lives in version control.
- **Rationale only where it changes a decision**, as a trailing clause after
  `—`. `One writer — nothing to race, so no locking` earns its clause;
  `This is important for correctness` does not.
- **Delete, do not deprecate.** A stale line reads as current.

## Density

From @references/personas/writer.md, Vera Lindqvist. Checked by
`@resources/prose.py` where the rule is mechanical.

| rule | test |
|---|---|
| Lead with the answer | the first line of a file or section is the finding, command or state — never the approach to it |
| Every heading summarises what is beneath it | headings alone read as the argument |
| Cut twice | half the words, then half of what is left, with no fact lost |
| A fact set is a table, a sequence a numbered list | a paragraph survives only where the content is an argument |
| About twenty words a sentence, on average | measured per file, `prose.py check` |
| No unbound `it`, `this`, `that`, `there` | each is deleted or names its noun; `prose.py check` flags the vague-subject shape (`it is`, `this means`, `there are`) |
| Reference describes, never teaches | instruction and explanation become a link |
| No preamble, no recap, no closer | the file opens on content and ends when the content ends; `prose.py check` flags a listed opener or closer phrase |
| Emphasis earns its place | bold and italic only where a reader needed it, never both |
| A quoted example of banned prose is backticked | bare, `prose.py check` reads the quote as the file's own prose and flags the rule that teaches it |

## Where prose stays

A memo's `## Why` and `## Alternatives considered` are arguments, not facts —
the one place paragraphs are correct. Compress them; the rest of a memo is a
table or a list.

## Shape per document

| document      | reader              | shape               |
|---------------|---------------------|---------------------|
| PRD body      | an analyst, cold    | a contract          |
| spec body     | an implementer      | a checklist         |
| atomic        | a worker, mid-step  | a checklist         |
| workflow      | a worker, cold      | a route             |
| memo          | a reader months out | decision + argument |
| worker report | the orchestrator    | verdict + evidence  |
| README        | a person, first time | quickstart, then rings |

The README is the one document with a human reader — a sentence there may
carry two ideas. Every other document keeps the rules above.
