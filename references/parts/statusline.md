# The status line

@resources/statusline.sh renders the pass's numbers continuously, for a person
watching the terminal rather than the pass. The loop reads nothing here. The
state-change line behind the numbers is @references/parts/progress.md.

```
<dir> <branch> *<dirty> ↑<ahead> ↓<behind> · <model>
▸pearde <rd>/<rn> <rp>% · +<dr>d · open <o> <q>% · <persona> · ▸board
```

Two rows — the progress line's numbers, what the working tree owes, and a link
to the board. Sharing one row pushes the board off a narrow terminal; no board
in scope, no second row.

| term | is |
|---|---|
| `<rd>/<rn> <rp>%` | requested work only |
| `+<dr>d` | derived PRDs not yet `done` — the backlog, not the tree. Suppressed at zero, which reads as "drained" and not merely "none" |
| `*<dirty>` | uncommitted entries |
| `↑<ahead> ↓<behind>` | commits against upstream. No upstream renders `no-upstream`, never `↑0` |
| `<persona>` | who is working, as the id |
| `▸board` | an OSC-8 hyperlink to the live view |
| `▸vault` | the board as an Obsidian vault |

`PRD_STATUS_LINK=off` prints the `▸board` and `▸vault` labels bare. Both links
are optional.

## `+<dr>d` is the remainder, because a total cannot answer its own question

Until 2026-08-30 the row rendered `<dn>`, every derived PRD — a count rising
and never falling. A dotfiles board showed `+99d` with 95 of the 99 closed,
read as 99 things outstanding; this repo's own board showed `+7d` with
nothing outstanding. The remainder stops a derived tree growing unseen.

The progress line has room for both halves and carries them as
`derived <dd>/<dn>`. This row has room for one, and takes the one that moves.

## The persona is read from the transcript, the only channel open

Nothing on disk holds a persona, and the status line runs in a process of its
own. @resources/statusline.sh takes the last `· as <id>` a pass printed,
matched with the `▸` in front of it so prose cannot supply one.

Before the first pass the term is absent rather than `engineer`: an unstated
persona is `engineer` anyway, and rendering a default nobody chose reads as an
answer. The id renders, not the name, because the id is what you type back.

## `▸vault` roots at the board, and names the vault by its registered id

A native `obsidian://open` URI needs no plugin, key, or daemon, and renders
whenever `.pearde/.obsidian/` exists (@references/obsidian.md), daemon or no.

The vault roots at the board, not the repo: Obsidian hides a dot-directory
inside a vault, so `.pearde/` is invisible from a repo-root vault and visible
in whole from its own.

The URI names the vault by the id `obsidian.json` holds for that exact path
(`?vault=<id>`). A path Obsidian has not registered opens its ancestor vault
instead — the repo root, where the repo is a vault too — so an unregistered
board falls back to `?path=`. `pearde init` registers the board.
