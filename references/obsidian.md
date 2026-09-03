# Obsidian — the board read natively

The board is the vault: Obsidian roots at `.pearde/` and renders what pearde
writes — `prds/**/prd.md` through the generated board notes, `memos/`,
`workflows/`, the knowledge layer under `wiki/`. Backlinks, link resolution and
the graph view are the read layer.

## The root is `.pearde/`, never the repo root

Obsidian skips every path starting with a `.` before reading any setting, and
`userIgnoreFilters` only adds ignores. A repo-root vault sees no board; rooted
at `.pearde/` it sees every child. So every path the board writes — Dataview
sources in `Dashboard.md`, wikilinks in `wiki/board/` — is `.pearde/`-relative,
an older board reading one level off until `knowledge.py board` regenerates
it.

## The register is written only with Obsidian closed

`obsidian://open` resolves only against Obsidian's own register
(`~/Library/Application Support/obsidian/obsidian.json`,
`~/.config/obsidian/obsidian.json` on Linux), the file `▸vault` reads for the
board's id (@references/parts/statusline.md). Unregistered, a folder opens its
registered ancestor — the repo root, the wrong tree.

Obsidian reads the register at launch and rewrites it *from memory* on quit: an
entry added under a running app goes unseen (`Unable to find a vault for the
URL`) and dies on exit. Quit → write → launch:

```sh
pearde vault --wait --open        # quit Obsidian when it says to
```

Seeds `.pearde/.obsidian/` if missing, waits for the process to go, writes the
entry, opens the vault; without `--wait` it refuses while the app runs. `init`
calls the same writer, saying so when Obsidian is up; `doctor`'s `vault` row
reads the register back, `broken` with no entry.

## `doctor` resolves the home from passwd, never from `HOME`

The register lives under a home, and doctor runs in shells exporting no `HOME`:
`env -i`, launchd, a container, a scrubbed harness. Under `set -u` an
unguarded read ends the report rather than failing one row: everything below
`vault` stops printing. Trusting the variable lets `env -i` read a failure as
`ok`, so the home comes from passwd, as in the `plugins` row.

| order | resolver | why not sooner |
|---|---|---|
| 1 | bash expands `~` from passwd — a builtin: no PATH, no subprocess | — |
| 2 | `getpwuid` through `python3`, `HOME` unset in the subshell — `~` follows a set-but-empty `HOME` | those shells often lack `python3`, macOS `/usr/bin/python3` being a stub exiting non-zero without the Command Line Tools |
| 3 | `broken`, the home unresolvable, as `index broken · no python3 to read it` | only a uid with no passwd entry; an unrun check has not passed |

Precedence inside the home is unchanged: macOS `Library/Application Support`
where it exists, then `XDG_CONFIG_HOME`, then `~/.config`. The row never claims
the uid **has** no home, nor Obsidian absent.

## Two plugins, seeded by `init` and never overwritten

Settings at `@resources/board/obsidian/`, pinned bundles fetched by
`install.sh --apply`, both seeded with a fresh API key into a new board's
`.pearde/.obsidian/` by `@resources/board/init.py`, which overwrites no plugin,
key or hand-tuned config. Obsidian loads a vault's plugins only on first open —
until then the port is silent.

| plugin | does |
|---|---|
| dataview | runs the DQL/DataviewJS views in `Dashboard.md` and the `_index.md` files, vault open |
| obsidian-local-rest-api ("Local REST API with MCP") | the port a tool talks to — HTTPS on `127.0.0.1:27124`, its `/mcp` endpoint in the same server: Obsidian-as-tools installs nothing more |

## The graph view colours by tag, never by folder

The colour groups are `tag:` queries, one per kind: `#prd`, `#memo`,
`#workflow`, `#atomic`, `#conclusion`, `#source`, `#pending`, `#graph`. As
`path:` queries they died silently on 2026-09-02, the day the layout moved: a
group matching nothing draws grey, leaving the wiki's own links — the folder
tree, not the board. A tag survives a move, a path never does.

Every note carries its kind's tag, untyped:

| note | tags | written by |
|---|---|---|
| `wiki/board/<prd>` | `prd`, `state/<state>`, `origin/<origin>`, `blast/<blast>` | `knowledge.py board`, per regeneration |
| `memos/<slug>` | `memo`, `kind/<kind>`, `status/<status>` | `memos.py add`, `memos.py retag` |
| `workflows/<slug>` | `atomic` or `workflow` | `workflows.py add`, `workflows.py retag` |
| `wiki/sources`, `wiki/conclusions` | `source` / `conclusion`, plus subject tags | `knowledge.py remember` / `conclude` |
| `wiki/pending`, `wiki/graphs` | `pending` / `graph` | `knowledge.py enqueue` / `wiki` |

The axis tags say what a folder cannot: `#state/open` is a node every open PRD
hangs off, `#kind/invariant` gathers the memos that bind. A PRD's `workflow:`
stays a wikilink, its edge drawn.

`showTags` is on, so tag nodes draw. Preset:
@resources/board/obsidian/graph.json — a seeded vault keeps its scale, node
size and forces, `init` and `upgrade` overwriting `colorGroups`, `search` and
`showTags` alone, via `init.repair_graph_view`.

## Two ways in — REST for a script, MCP for a client

| | direct REST (curl / urllib) | MCP |
|---|---|---|
| setup | zero — the port answers | one config line per client (`/mcp` endpoint) |
| transport | `curl -sk https://127.0.0.1:27124/<route>` | an MCP handshake against `https://127.0.0.1:27124/mcp` |
| best for | passes, scripts, `knowledge.py` verbs — anything local | a client wanting named tools: `read note`, `search`, `patch` |
| auth | same bearer key | same — the plugin's API key |

Both die with the app: the files remain, the port does not.

## The connection facts

```
https://127.0.0.1:27124              base URL (HTTPS, self-signed certificate)
Authorization: Bearer <key>          every call, no exceptions
<board>/wiki/.obsidian-api-key       the key a tool reads — mirrors
                                     .obsidian/plugins/obsidian-local-rest-api/data.json,
                                     and is rewritten to match it whenever
                                     the two disagree
GET  /                               alive? -> {"status": "OK", "authenticated": …}
GET  /vault/<path>                   one note's bytes
PUT  /vault/<path>                   write one note (whole file)
PATCH /vault/<path>                  a targeted insert — Content-Type:
                                     application/vnd.olrapi.patch
POST /search/simple/?query=<q>       Obsidian's own search index, scored
POST /search/                        structured — Content-Type:
                                     application/vnd.olrapi.jsonlogic+json,
                                     {"==": [{"var": "frontmatter.state"}, "open"]}
GET  /commands/ · POST /commands/<id>   list and fire the app's 190+ commands
GET  /active/                        the note a person is looking at
GET  /open/<filename>                open one in the app
/mcp                                 the plugin's MCP server endpoint
```

The key rides at `.pearde/wiki/.obsidian-api-key`, minted by `init` in the v5
schema the plugin reads; `.pearde/wiki/` is gitignored.

## Queries worth running

```sh
K=$(cat .pearde/wiki/.obsidian-api-key)
# every open PRD, through Obsidian's own frontmatter index
curl -sk -X POST https://127.0.0.1:27124/search/ -H "Authorization: Bearer $K" \
  -H "Content-Type: application/vnd.olrapi.jsonlogic+json" \
  -d '{"==": [{"var": "frontmatter.state"}, "open"]}'

# read the dashboard a person sees
curl -sk https://127.0.0.1:27124/vault/wiki/Dashboard.md \
  -H "Authorization: Bearer $K"
```

REST `search/` answers one flat predicate per call. Before the port:
`plan.py scan`, `knowledge.py query`, a file read; for joins `knowledge.py`
and `plan.py`. The deep views stay in Dataview — DQL over `wiki/board`,
`memos`, `workflows` per `Dashboard.md`, `file.inlinks` backlinks included,
in-app.
