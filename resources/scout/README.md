# scout — one door onto four layers: discover, ask, curate, wire

`scout.sh <verb>` is the one entry point onto all four. It used to be four
files — `scout.sh` (sweep/delta/trending), `toolscout.sh`, `route.sh` and a
name you had to already know for the reading list and the quality gates —
sharing the buckets, the snapshots, the ranking-page shape and the findings
record while meeting a newcomer as four `--help` texts. `toolscout.sh` stays,
a compat entry that execs `scout.sh tool "$@"` — nothing that already calls
it by name breaks.

## Commands

`scout.sh` with no verb prints this same table, generated from the `registry`
function at the top of the file — each row in the function is a row here, and
a `scout.sh` verb this table omits, or a contract this table states
differently, is what `scout.sh`'s own `registry` says, never what got typed
here by hand.

| verb | contract | lands in |
|---|---|---|
| `sweep` | snapshot every bucket's star counts | `snapshots/<date>.tsv` |
| `delta [days]` | what gained the most stars since ~N days ago | `snapshots/` (diffed, no new write) |
| `trending [window]` | GitHub's own trending feed, a discovery channel | none kept — pipe to a file to save it |
| `tool <query>` | one-off dependency ranking: stars + what stars hide | none kept — pipe to a file to save it |
| `find <id> [query]` | call one ranking page by id (was `route.sh`) | `routes.md` defines it; a settled pick goes in `findings.md` |
| `reading` | check the curated reading list: mappings present, archived rows marked | `reading-list.md` |
| `quality` | the passive quality gates and their templates | `templates/` |

Four layers behind the seven verbs, each answering a different question:

1. **discover** — what is out there, ranked (`sweep`, `delta`, `trending`,
   `tool`)
2. **ask** — one job, answered off many ranking pages and written down
   (`find` + `routes.md` → `findings.md`)
3. **curate** — what is worth *reading*, mapped to what it teaches a specific
   tree (`reading` — the check over `reading-list.md`)
4. **wire** — the passive quality gates that keep the trees honest (`quality`
   + sccache, which stays a manual `~/.cargo/config.toml` edit — see below)

Stars are the discovery layer, never the verdict. A 74k-star case-study corpus
beats a 243k-star hype repo for *improving the product*; a 10k-star archived
TUI library is a worse dependency than a 3k-star active one. The curated layer
exists for those two cases.

## Layout

| path | what |
|---|---|
| `scout.sh` | the one entry point — all seven verbs, `registry` is their source |
| `toolscout.sh` | compat entry — execs `scout.sh tool "$@"` |
| `route.sh` | `scout.sh find`'s reader of `routes.md`, holds no list of its own |
| `routes.md` | **index one** — every page a ranking comes from, one shell block each |
| `findings.md` | **index two** — what won, on which axis, when |
| `buckets.txt` | the taxonomy — `name<TAB>query` per line; **the knob** |
| `snapshots/` | star counts, one TSV per day, capped at the 90 most recent (`SCOUT_SNAP_KEEP`) |
| `reading-list.md` | the curated, mechanism-mapped list |
| `templates/` | quality-gate configs + workflows for wiring a new tree: `quality.yml`, `scout.yml`, `dependabot.yml`, `_typos.toml`, `deny.toml` |
| `README.md` | this file — the skill's entry is `references/skills/pearde-scout.md`, two levels up |

## Commands, in detail

### `scout.sh sweep`
Snapshot every bucket in `buckets.txt` into `snapshots/<date>.tsv` — one GitHub
search call per bucket, sort=stars, top N. The **first** sweep is a baseline;
every sweep after is a measurement. Run daily on a local cron and the delta
accumulates while nobody looks, no cloud needed. `templates/scout.yml` is the
GH Actions equivalent for a repo running the sweep in CI. Each sweep prunes
`snapshots/` to the 90 most recent TSVs, overridden with `SCOUT_SNAP_KEEP` —
enough daily history for every `delta [days]` window named here, plus slack for
cron gaps, without growing forever.

### `scout.sh delta [days]`
What gained the most stars since ~N days ago, computed by **diffing our own
snapshots** — the stargazers API is restricted as of 2026-06-30, leaving no
other route. `NEW` marks a repo that entered a bucket's top-N, the useful
signal: the repo displaced established work.

### `scout.sh trending [daily|weekly|monthly]`
Scrapes GitHub's own trending as a discovery channel for buckets nobody thought
to define. The response is layout-coupled HTML; a row misalignment fails
loudly, not silently.

### `scout.sh tool '<query>'` (compat: `toolscout.sh '<query>'`)
One-off ranker for a specific choice: `topic:tui language:rust stars:>1000`.
Stars ranked, plus `STATE` — days since push, ARCHIVED, issue load, license —
so the dead-3-years 10k-star repo reads as dead. `toolscout.sh` execs this
verb unchanged, so the two commands produce byte-identical output for the
same query.

### `scout.sh find list | <id> [query] | check`
Forty-five ranking pages beyond GitHub, one shell block each in `routes.md`,
addressed by id: `hn`, `brew`, `arch`, `popcon`, `crates`, `scorecard`, `osv`,
`cht`, `marginalia`, `wayback`, `crawl`, `mcp`, `skills`, `skillrepo`,
`openalex`. `scout.sh find check`
runs every one against its own example and prints `ok` or `DEAD` — the file
cannot claim a route works without the claim being runnable. `find` is
`route.sh` under this door: adding a route is still editing `routes.md`, and
`route.sh` itself keeps working by name for anything that already calls it.

### `scout.sh reading`
Check pass over `reading-list.md`: every row's *mapping* column (the last
one, "what to steal") must be non-empty — a bare row fails the check and is
named, exit non-zero. Every row's repo is then resolved for state — archived,
last push — the same signal `toolscout.sh`'s `STATE` column reads, checked
against the newest snapshot first and only reached over the network (`gh api
repos/<repo>`) for a repo no snapshot names. A repo that reads `ARCHIVED` is
marked `<!-- stale: archived YYYY-MM-DD -->` in its row, in place — never
deleted, and never re-marked once it carries the comment. A repo the API
cannot resolve (renamed, deleted) is left as-is: unknown state is not stale. See
[The reading list discipline](#the-reading-list-discipline) below for what
earns a row.

### `scout.sh quality`
Lists the gate templates in `templates/` and what each wires in — `_typos.toml`,
`deny.toml`, `dependabot.yml`, `quality.yml`, `scout.yml`. See
[The quality layer](#the-quality-layer--accelerate-quality-by-just-using-it)
below for what each gate catches and how to copy them into a new tree.

## The research loop — one job, two indices

`routes.md` is where numbers come from. `findings.md` is what the numbers
decided. The loop between them:

1. **Phrase the job as a choice.** "Recursive search over a source tree", not
   "is ripgrep good". A job with nothing to reject has nothing to measure.
2. **Pick routes by axis, at least two.** Attention (`hn`, `lobsters`),
   installs (`brew`, `arch`, `popcon`, `crates`, `npm`), stars (`gh`,
   `codeberg`), hygiene (`scorecard`, `osv`, `depsdev`). Axes that disagree are
   the finding — a tool with distro breadth and no installs is abandoned, and
   only two axes together say so.
3. **Run them.** `scout.sh find <id> <query>`, every candidate through every axis.
4. **Write the row.** Pick, what it beat, the numbers with their routes, the
   date, and what would overturn it. A pick on one axis is marked `weak`.
5. **Anything unanswered goes to `## Open`** in `findings.md` — a queue, so the
   next sweep knows what was already asked.

Six months is the expiry. A finding past six months is re-measured or deleted,
with no third option.

## The reading list discipline

A repo earns a row in `reading-list.md` only by answering in writing *which
file in which tree changes because we read this*. `reading-list.md` carries the
genres, the entries and the anti-list. `scout.sh reading` holds the *shape*
honest — a bare mapping fails the check — and the state current — an
archived repo is marked stale in place — but writes no row itself; the
curation stays human.

## The quality layer — "accelerate quality by just using it"

Every quality gate below ran green on the family's trees as of 2026-08-25, then
went into CI to run itself. The weekly schedule is the point: a new CVE against
a locked dep turns the tab red on Monday with no human action.

- **typos** (`_typos.toml`) — 2,000+ md files where the prose IS the spec. A
  typo in a frontmatter key is a silent behaviour change. The config is the
  record of deliberate spellings, not an ad-hoc suppression.
- **gitleaks** — full-history secret scan. `quality.yml` names a
  `.gitleaks.toml` for the allowlist — fixtures asserting on fake keys, each
  with a recorded reason — but `templates/` ships none: gitleaks runs on its
  defaults until the tree writes its own.
- **cargo-deny** (`deny.toml`) — RustSec advisories hard-gated. The ignore
  list is the audited unmaintained-transitive set, by ID, with reasoning. A
  NEW advisory fails the job. 0.20.x has no `unmaintained` severity key —
  ignore by ID with `unused-ignored-advisory = "allow"`.
- **cargo-machete** — unused deps caught as they appear.
- **sccache** — one shared compile cache across the workspaces. The
  precondition (identical toolchain pins) is met in this family; install and
  add `rustc-wrapper = "sccache"` to `~/.cargo/config.toml`.

Wire a new tree by copying `templates/` — `quality.yml`, `dependabot.yml`,
`_typos.toml` and `deny.toml` — then adjust the deny.toml ignore list to that
tree's actual advisories, and write a `.gitleaks.toml` if the tree needs an
allowlist.

## Maintenance

- Edit `buckets.txt` and `routes.md`, not the scripts. A bucket is
  `name<TAB>query`; a route is a `### id` heading, four bullets and one `sh`
  block.
- `SCOUT_MAILTO=you@example.com` puts every polite-pool route in the fast tier.
  Without it ecosyste.ms answers `402 Payment Required` and the registries
  throttle.
- `scout.sh find check` before writing a finding. A route that dies twice moves to
  the dead-ends table in `routes.md` with its observed status, and every
  finding that stood on it goes with it.
- `pushed:` filters in queries compose with `stars:>`; keep a stars floor or
  the tail is noise.
- The `delta` output rewards hype by construction — a repo gaining 10k
  stars/week is being *talked about*, orthogonal to whether it's good. Treat
  it as a reading list, never a shortlist.
- The scout's activity heuristic flags long-quiet but *finished* tools
  (hyperfine, tokei) as "slow". Right to flag, wrong about what the flag
  means.
