---
state: "done"
origin: requested
priority: 77
repo: "/Users/feb/dev/cartridge"
capability-owner: web
needs:
- "the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/web-ctg-exists-as-a-cartridge-and-fetches-a-page-as-readable-text"
footprint:
- "web.ctg"
commit: "73540349688b52d82caa7342037ace7a3c07029e"
---

# Search returns ranked results, each with its source URL

## Outcome

`{op: "search", query, limit?}` returns
`{query, results: [{rank, title, url, snippet}]}` from the chosen backend. A
missing or rejected credential is reported as an error naming the setting to
set — never a crash, and never an empty result list pretending there were no
results.

`needs` names the fetch child because both live in the same files; they
serialize.

## Answer (2026-09-17, from the user)

**Brave Search API, the key from a declared optional setting that names an
environment variable, and no second backend.** This is the recommendation below,
chosen by the user directly, and it settles the three parent Acceptance boxes
that waited on it:

- `grant.net` names exactly one host, `api.search.brave.com`.
- The result shape is Brave's ranked JSON, one URL per result, used as returned;
  the cartridge does no parsing to satisfy "ranked results, each carrying its
  source URL".
- The credential is the user's own Brave key, declared as an optional setting
  naming an environment variable, in the shape `auth.ctg` already uses. The
  setting arrives as `null` when unset, so the implementation must treat an
  absent key as "no search configured" and say so, rather than re-checking a
  bound the host already settled.

No alternative backend is added, and the DuckDuckGo scrape is rejected on the
analyst's ground: a scrape has no schema, breaks silently, and its ranking is
whatever the page rendered that day.

The question that produced this answer, and the alternatives that were weighed,
are kept below as the evidence for the choice.

## Questions (answered above)

**Which search backend does `web.ctg` call, and what credential does it use?**

The answer fixes three of the parent's five Acceptance boxes — what `grant.net`
names, what the result shape is, and whether the cartridge can work at all on
this machine — and it cannot be derived from the repository or probed here.

Nothing in the composition searches the web today. No cartridge holds a search
credential, and the one place a key could already be is unreadable to an agent:
the safety net blocks `ls .cartridge/credentials` (rule
`secret.basename.credentials`), so the analyst could neither confirm nor deny a
key on this machine. Every credible search API needs a key the user owns; the
only keyless options are a scrape or a service that has to be running.

### Recommended answer

**Brave Search API (`api.search.brave.com`), the key from a declared optional
setting that names an environment variable, and no second backend.**

- It returns ranked JSON with a URL per result, which is exactly the parent's
  box 2 ("ranked results, each carrying its source URL") with no parsing.
- One host in `grant.net`, matching the shape `auth.ctg` already uses
  (`grant.net: ["api.openai.com"]`).
- The free tier is enough for a voice coworker's "is that still how that library
  works".

### Alternatives, and what each costs

| Option | Credential | Cost |
| --- | --- | --- |
| Brave Search API | the user's key | one host, clean ranked JSON — *recommended* |
| Tavily / Exa | the user's key | agent-shaped results (text already extracted), a second vendor |
| Serper / Google CSE | key plus `cx` | two settings, Google's terms |
| DuckDuckGo `html.duckduckgo.com` | none | a scrape: no schema, breaks silently, grey terms. The analyst rejects it — box 2 says "ranked results", and a scrape's ranking is whatever the page rendered that day |
| local SearXNG | none | a service that must be running; moves the problem rather than solving it |
| Through the model (a hosted `web_search` tool) | reuses an existing credential | `auth.ctg` serves only `status` for `openai/live` and returns no secret, and a credential never leaves the router. `web.ctg` would have to go through `proxy`/`router`, which makes a model call out of every lookup and buries the source URLs in annotations. The heaviest option |

Answer this and the child is unblocked; the fetch sibling needs no answer and
can land first.

## Acceptance

- [x] `{op: "search", query}` returns results ranked, each carrying its source URL.
- [x] The credential is one declared, optional setting with a `doc` line; absent, a search returns a reported error naming it, and `web.ctg` still loads and still fetches.
- [x] `bun test` covers a recorded backend response, a backend error and the missing-credential path, all against a local server — no live network in any test.
- [x] `README.md` and `.cartridge/help.md` name the backend, the host in `grant.net`, and how to supply the key.
- [x] `just audit web` and `just isolation` report nothing hard for it.
