---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
---

# Disclose cloud egress consistently when an MCP operation can send projected content to a provider.

## Do

Reuse the existing cloud-tag detection and warning language so MCP clients can see when a loopback Ollama URL still sends query, context, or project text off-machine. Expose the disclosure in setup or health and immediately before model-dependent operations when host protocol permits, without logging private prompt text. Keep CLI and MCP wording consistent. Do not add a new consent system or block configured cloud use; make configured behavior visible.

## Acceptance
Tests cover local-only tags, cloud tags through loopback URLs, and explicit remote endpoints. MCP setup or health exposes cloud-egress state before an answer request, CLI retains its warning, and neither surface includes credentials or submitted text. One shared detector determines all results.

A disclosure missing on one path is worse than none, because it teaches a
reader that silence means local. So the list was read off the dispatch table
rather than recalled: `Server::invoke`'s `match name` in
`src/rpc/src/server.rs` names twenty-five arms plus the `<kind>:<leaf>`
declaration fallback, and each arm's body was walked for a reach at
`self.llm`, `self.worker`, `embed_seed`, or `HubRpcClient`. Seven reach one:
`query` embeds `text`; `search` hands `text` to the hub, which embeds;
`ingest` enqueues the document into the embedding worker (or runs it through
synchronously); `link` completes a prompt built from both thoughts; `focus`
embeds the attractor text; `intake_drain` completes over each intake file;
`ask` embeds the question and completes over the cited facts. The other
eighteen — `log`, `events`, `report`, `forget`, `forget_by_source`,
`degrade`, `move`, `promote`, `health`, `ready`, `claim_kind`, `pulse`, `gc`,
`audit`, `setup`, `reflex`, `memo`, `plan` — and the declaration tools reach
none. The count already existed as `MODEL_DEPENDENT`, written for the
shutdown gate; the walk confirmed it arm by arm rather than trusting it, and
the disclosure now reads the same array, so a tool that grows an embed cannot
grow one without the other.

Landed: `Config::egress_warnings` is the one detector, and three surfaces
read it — the boot warning in `main::boot_config` (unchanged), a new
`egress` field on the health payload and `HealthRes`
(`src/transport/src/memory_rpc.rs`, `serde(default)`, empty from an older
daemon), and a `CLOUD EGRESS` notice appended in
`src/commands/src/commands_mcp.rs` to the description of every
`rpc::server::MODEL_DEPENDENT` tool and to no other. `tools/list` is the
notice's place because the MCP protocol has no pre-call channel and a result
arrives after the text is already gone; it is read from this process's config
rather than the daemon's health so that a missing daemon cannot silence it.
A line carries a label, a redacted URL and a model name — never the
`[embed]`/`[reason]` `key`, never a submitted byte.

Found on the way: userinfo was read as the host. `http://localhost:tok@api.example.com/v1`
matched `//localhost` in `is_local_ollama` and stopped at the first `:` in
`host_of`, so a URL that egressed every chunk answered "local" and warned
nobody. `authority_of` in `src/llm/src/llm.rs` now strips userinfo for every
host predicate, and `llm::redact_url` hides it from the warning.

The known ceiling is `search`: the text goes to the hub, which fans out to
sibling roots embedding under configs this process cannot see, so a local
config stays silent about a cloud-tagged sibling. Aggregating the hub's roots
is the upgrade; the notice says "this memory" rather than implying it surveyed
the machine.

Tests: `src/llm/src/tests/llm_test.rs` (userinfo, redaction),
`src/config/src/tests/config_test.rs` (the warning names the endpoint without
its credential), `src/rpc/src/tests/server_admin_test.rs` (health carries the
three shapes: local-only, `:cloud` behind loopback, explicit remote),
`src/commands/src/tests/commands_mcp_test.rs` (the same three shapes through
`tools/list`, marked iff the tool can reach a model), and
`src/transport/src/tests/memory_rpc_test.rs` (append-only round trip).
`just check` green; `cargo nextest run --workspace --no-fail-fast` 1472/1473,
the one red `memory::cited_paths`, owned by
[the-plan-crate-cites-an-untracked-file](../the-plan-crate-cites-an-untracked-file/prd.md).
