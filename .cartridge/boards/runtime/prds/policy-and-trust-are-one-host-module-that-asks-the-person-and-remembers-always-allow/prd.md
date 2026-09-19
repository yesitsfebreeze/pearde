---
state: "open"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
blast-radius: high
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy
  - /Users/feb/dev/cartridge/cartridge.ctg/src/trust
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/trust.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs
---

# policy and trust are one host module that asks the person and remembers always allow

## Outcome

Any consumer — a cartridge, the agent, the host itself — can ask the person for an approval, a piece of data, a secret or trust in changed files, and the person answers in a safe place. The decision, the asking, the trust record and the remembered answers are one host module, `cartridge.ctg/src/policy`, because the system cannot run without them.

Today these are four separate things. `policy.ctg` is a 122-line Lua evaluator that answers `allow`, `ask` or `deny` and, by its own help page, "never … prompts anyone". The agent keeps its own pending approval (`agent.ctg/src/lib.rs`, `approve`). `cartridge trust --ask` reads a terminal, so the daemon cannot ask: on 2026-09-19 `memo`, `lsp` and `fs` stayed failed with "has changed since it was trusted" until a person typed `cartridge trust` in a shell. `router {op:"login", key}` takes a key in the call arguments, so a secret an agent relays passes through its context.

## Decision (2026-09-19, user)

- "Yeah put everything in the policy and we can also create an always allow."
- "I think we should combine the trust and policy. We can consume the policy cartridge (it's very small) and put it into cartridge.ctg." and "its sorta mandatory for the system".
- The request function also covers "allowing cartridge updates and other things at runtime".

So `policy.ctg` is consumed into the host and deleted, `src/trust` becomes part of `src/policy`, and the host answers the `policy` and `policy.explain` keys the way it already answers `asp`. `agent`, `mcp` and `proxy` declare `policy` as a need today and keep doing so. This also removes a bootstrap problem: a policy that lives in a cartridge cannot be the thing that asks whether that cartridge may be trusted.

## Shape

One request, four kinds:

- `approve`: may this operation run. Raised when a decision is `ask`.
- `input`: the person supplies a value that matches a declared schema, and the requester receives it.
- `secret`: the person supplies a value that goes to the credential store. The requester receives `{stored: true}` and never the value.
- `trust`: files changed since they were trusted. The request carries the paths and digests; an allow runs `trust::record` and reloads. A cartridge update at runtime is this kind.

## Acceptance

- [ ] A consumer raises a request and gets back `allowed`, `denied` or `timed_out`; a timeout is a denial, an id answers once, and the wait is bounded by a declared `timeout_ms`.
- [ ] The requester's identity on a request is stamped by the host from the connection's token and cannot be supplied by the requester.
- [ ] An answer is accepted only from a person's client holding the host token. A cartridge node, and so an agent, is refused when it answers, including its own request. The answer key is not a `tool.*` event.
- [ ] Every pending request is published on the ring as a summary with its originator, so every surface shows the same list. No `input` or `secret` value is ever published.
- [ ] A `secret` answer reaches the credential store and no other process, log line or ring entry.
- [ ] A manifest that changed since it was trusted raises a `trust` request from the running daemon instead of leaving the cartridge failed; allowing it records trust and reloads that cartridge.
- [ ] The person can answer "always allow". The answer is stored as a policy rule scoped to the requester and the operation, is listed and revocable, and the next matching request is allowed without asking. `secret` and `trust` requests cannot be always-allowed.
- [ ] `policy` and `policy.explain` return what they return today for the existing smoke fixture.
- [ ] The agent's own pending-approval machinery and the terminal prompt in `cartridge trust --ask` are deleted; both go through the request. `policy.ctg` is removed from the composition and the repository in the same change that lands its replacement.
- [ ] `src/policy/README.md` exists in the fresh-eyes shape, and `README.md`, `.cartridge/help.md` and `docs/` describe the new keys.

## Questions for the analyst

- Which surfaces answer in the first version. The coordinator's default is the CLI and the proxy TUI; voice may approve and never enters a secret.
- The open PRDs on the `policy` board target `policy.ctg`. Each is either retargeted at `cartridge.ctg/src/policy` or retired as superseded by this one.

## Proof and recovery

Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`, `just audit`, `just isolation`, and a live probe with `cartridge call policy`. Not run. This PRD is too large to implement as one leaf; refine it into children before speccing.

## Split

Refined 2026-09-19 by analyst-2 for coordinator cartridge-4b, anchored on cartridge.ctg `324f36e`. Full evidence: `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`. Every child below updates the README, `.cartridge/help.md` and `docs/` text for the keys it adds, so the PRD's documentation box is covered by the children and needs no child of its own. Children, in order:

1. **the host answers policy and policy.explain with the evaluator policy.ctg had.** Repo `cartridge.ctg`, priority 100, needs none. Footprint: `src/policy/mod.rs`, `src/policy/evaluate.rs`, `src/policy/explain.rs`, `src/policy/settings.json`, `src/policy/README.md`, `src/lib.rs`, `src/host/plan.rs`, `src/host/mod.rs`, `src/host/socket.rs`, `src/loader/document.rs`, `.cartridge/tests/unit/src/policy/`, `README.md`, `.cartridge/help.md`, `docs/settings.txt`, `docs/architecture.txt`.
   Outcome: the host's own plan (`host_plan`, `src/host/plan.rs:57`) declares and listens to `policy` and `policy.explain` the way it already owns `tool.asp`. `Host::bail` answers them in process, the way it answers `asp`, and the socket's `event` branch serves a cartridge's call. The 122-line Lua evaluator is ported to Rust with the same outputs, and its settings are read from the composition's `policy` table on every reconcile, not once. A manifest that declares `events.policy` is refused, the same way `events.asp` is.
   - [ ] Named unit tests reproduce the smoke table with `policy={default="ask",tools={read="allow",docs="allow",write="ask"}}`: read→allow, docs→allow, write→ask, unknown-tool→ask. A `null` request is rejected.
   - [ ] Named unit tests cover operation-over-tool precedence, whole-tool deny wins, a malformed request→deny `malformed_request`, and the `policy.explain` `authorization` block for allow, deny and ask with each `authorization_route`. The `revision` string is byte-identical to the Lua `policy-evaluator:3|…` form.
   - [ ] A changed `policy` table in `config.lua` changes the next answer after a `reload`, with no daemon restart. An invalid table is refused and the previous rules stay in force.
   - [ ] `src/policy/README.md` exists in the fresh-eyes shape.
   Window: until child 2 lands, a live `policy.ctg` fails with "`policy` is already declared by `host`". This is harmless, because the host answers the same way.

2. **policy.ctg leaves the composition and the repository.** Repo `/Users/feb/dev/cartridge` (the superproject), priority 100, needs 1. Footprint: `.gitmodules`, `policy.ctg`, `.cartridge/init.lua`, `.cartridge/justfile`, `.cartridge/tests/integration/smoke.test.ts`, `.cartridge/memos/routine/cartridge-smoke.md`, `graft/policy.ctg`, `cartridge.ctg`.
   Outcome: the submodule and its `init.lua` row (`.cartridge/init.lua:30`) are removed, and `policy` is dropped from the `check`/`test`/`smoke` owner lists (`.cartridge/justfile:100-102`). The smoke fixture's policy profile becomes a host with no cartridges (`init.lua` `return {}`) that is still answered by `cartridge run policy`. The pointer moves to child 1's commit, all in one superproject commit.
   - [ ] `just smoke policy` passes against a profile that composes no `policy.ctg`, with the same four decisions and the `null` rejection.
   - [ ] `git submodule status` lists no `policy.ctg`, and no file outside `prd.ctg` names `policy.ctg`.
   - [ ] `just test runtime`, `just isolation` and a live `env -u CARTRIDGE_YOLO cartridge call policy '{"tool":"read","input":{},"context":{}}'` all exit 0.

3. **a consumer raises an approve or input request and a person answers it from the command line.** Repo `cartridge.ctg`, priority 100, needs 1. Footprint: `src/policy/request.rs`, `src/policy/pending.rs`, `src/policy/channel.rs`, `src/policy/mod.rs`, `src/host/plan.rs`, `src/host/mod.rs`, `src/host/socket.rs`, `src/cli/request.rs`, `src/cli/args.rs`, `src/cli/mod.rs`, `.cartridge/tests/unit/src/policy/`, `.cartridge/tests/unit/src/host/socket.rs`, `README.md`, `.cartridge/help.md`, `docs/transport.txt`.
   Outcome: `policy.request` is a host-owned event with a declared `timeout_ms`. It takes `{kind: approve|input, operation, summary, schema?, timeout_ms}` and resolves to `allowed | denied | timed_out`, plus `value` for `input`. The requester is stamped from the connection's token. Today `Caller::Cartridge` drops the id (`socket.rs`: `host.caller(token).map(|_| Caller::Cartridge)`), so it must carry it. `answer` and `requests` are socket methods, never events and never `tool.*`, granted only to the host token. The empty token no longer passes as `Caller::Host` (`socket.rs`, the `ponytail:` comment). Every pending request's summary is published on a host channel, `policy`, that clients `subscribe` to like `lifecycle`. The command line gets `cartridge request [list|follow|answer <id> allow|deny|--value <json>]`.
   - [ ] Named tests: a timeout answers `timed_out` and counts as a denial; a second answer to an id is refused; the wait is bounded by `timeout_ms`.
   - [ ] Named tests: a `requester` field supplied in the data is ignored or refused, and the stamped id is the calling cartridge. A cartridge token, and the empty token, get `UNAUTHORIZED` on `answer`, including for the cartridge's own request.
   - [ ] Named test: a channel subscriber receives each pending summary with its originator. An `input` value appears in no channel entry and in no log line, which the test checks by capturing the tracing output.
   - [ ] `cartridge request answer` from a terminal resolves a request raised with `cartridge call policy.request`, shown by a transcript in the evidence.

4. **a changed cartridge raises a trust request from the running daemon instead of staying failed.** Repo `cartridge.ctg`, priority 100, needs 3. Footprint: `src/policy/trust.rs` (moved from `src/trust/mod.rs`, with `src/trust/` deleted), `src/policy/mod.rs`, `src/host/mod.rs`, `src/cli/trust.rs`, `src/cli/project.rs`, `src/cli/host.rs`, `src/cli/setup.rs`, `src/loader/document.rs`, `src/lua/mod.rs`, `src/node/mod.rs`, `src/settings/files.rs`, `src/lib.rs`, `.cartridge/tests/unit/src/cli/trust.rs`, `.cartridge/tests/unit/src/policy/`, `README.md`, `.cartridge/help.md`.
   Outcome: when `reconcile` marks a slot failed with a trust refusal (`host/mod.rs:348-354`), the host raises a `trust` request carrying the paths and digests. An allow runs `trust::record` on the cartridge root and `replace(id)`. `cartridge trust --ask` and its terminal prompt (`cli/trust.rs:67-165`), and the `ask` call on project open (`cli/project.rs:20`), are deleted. An untrusted project's `init.lua`/`config.lua` also becomes a request from a daemon that starts with the host alone.
   - [ ] Named test: editing a trusted fixture cartridge's manifest yields one pending `trust` request naming the file and its new digest. Allowing it leaves the cartridge active without a daemon restart, and denying it leaves it failed with the refusal.
   - [ ] `grep -rn 'read_line\|IsTerminal' src/cli/trust.rs src/cli/project.rs` finds nothing, and `cartridge trust --ask` is an unknown flag.
   - [ ] Under `CARTRIDGE_YOLO=1` no trust request is raised (today's yolo behaviour holds), which a named test checks.

5. **the person can always-allow an operation and revoke it later.** Repo `cartridge.ctg`, priority 100, needs 3. Footprint: `src/policy/always.rs`, `src/policy/evaluate.rs`, `src/policy/request.rs`, `src/policy/mod.rs`, `src/cli/request.rs`, `src/cli/args.rs`, `.cartridge/tests/unit/src/policy/`, `README.md`, `.cartridge/help.md`, `docs/settings.txt`.
   Outcome: `answer <id> always` resolves the request as allowed and stores a rule `{requester, tool, op}`. The rule lives in a 0600 file under `$CARTRIDGE_HOME/policy/<project-hash>.json`, next to the trust store. The evaluator consults stored rules before it returns `ask`. `cartridge request rules` lists them and `cartridge request revoke <rule>` removes one.
   - [ ] Named test: after `always`, the next matching `policy.request` from the same requester and operation is allowed without a pending entry. A different requester or op still asks.
   - [ ] Named test: `always` on a `trust` or `secret` request is refused, and the request stays pending.
   - [ ] Named test: after `revoke`, the same request asks again. The rule list survives a host restart.

6. **the agent asks through the host request and keeps no approval of its own.** Repo `/Users/feb/dev/cartridge/agent.ctg`, priority 100, needs 3. Footprint: `src/lib.rs`, `src/module.rs`, `cartridge.json`, `.cartridge/tests/unit/run_state.rs`, `.cartridge/tests/integration/loop.rs`, `README.md`, `.cartridge/help.md`.
   Outcome: on `ask`, `prepare_tool` calls `policy.request {kind:"approve", operation:{tool, op}, summary}` with no tool input in the summary, and maps `allowed` to run and anything else to `permission denied`. The following are deleted: `Approval`, `live.pending`, `fn approve`, `fn answer`, the `answer` op in `cartridge.json` and `module.rs`, the `awaiting_approval` phase and `approval_requested` kind, and `approval_timeout_secs`, which becomes the request's `timeout_ms`. `cartridge.json` needs `policy.request`.
   - [ ] Named test in `loop.rs`: an `ask` decision raises exactly one `policy.request` whose summary carries no input. `allowed` runs the tool, and `denied` and `timed_out` return `permission denied`.
   - [ ] `grep -n 'awaiting_approval\|approval_requested\|"answer"' src cartridge.json` finds nothing, and `just test agent` and `just check agent` pass.

7. **a secret request stores the person's value with auth and never returns it.** Repo `cartridge.ctg`, priority 100, needs 3 and `@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values` (cross-board, analyzing). Footprint: `src/policy/secret.rs`, `src/policy/request.rs`, `src/policy/mod.rs`, `src/cli/request.rs`, `.cartridge/tests/unit/src/policy/`, `README.md`, `.cartridge/help.md`.
   Outcome: `kind: "secret"` names `{provider, field}`. The person's value goes from the CLI (read without echo) to the host and on to auth's store key only. The requester receives `{stored: true}`.
   - [ ] Named test with a fake store listener: the requester's result is exactly `{stored:true}`, and the value appears in no channel entry, pending summary, log line (captured tracing) or reply other than the store call.
   - [ ] Named test: `always` on a secret is refused, and the CLI never takes a secret from argv, only from stdin with no echo.

Shared files that force these children to integrate one after another: `src/host/socket.rs`, `src/host/mod.rs` and `src/host/plan.rs` (children 1, 3, 4, and the ASP sessions landing there), and `src/policy/request.rs` with `src/cli/request.rs` (children 3, 5, 7). Children 4, 5 and 6 can run in parallel after child 3, but 4 and 5 both touch `src/policy/mod.rs`.

Answers to the analyst questions (recommendations; neither blocks the split):
- Surfaces in v1: the command line only (`cartridge request`), plus the host `policy` channel so any surface can subscribe later. Evidence: proxy.ctg has no TUI (`proxy.ctg/src` is an HTTP server and has no ratatui/crossterm dependency), and mcp states "This server has no interactive approval channel" (`mcp.ctg/src/service.rs:481`). Voice approval and a proxy TUI would each be a follow-up leaf that subscribes to the channel. Voice may approve and never enters a secret.
- Open `policy` board PRDs: `bounded-search-guard-rules`: retarget at `cartridge.ctg/src/policy/evaluate.rs`, needs child 1. `…/policy-refuses-unbounded-searches-with-a-teaching-reason`: retarget at `cartridge.ctg` (`src/policy/`, unit tests replace `.cartridge/tests/policy.rs`). `…/policy-refusals-and-overrides-reach-the-caller-and-the-observation-journal`: keep; it targets agent.ctg and mcp.ctg, and its agent footprint must be reconciled with child 6. `…/the-policy-owner-gate-runs-against-the-current-host` (question): retire; superseded by child 1's unit tests. `improve-policy-programme` (deferred): retire; superseded. `improve-policy-resource-scope` (deferred): retire; its scope is file-backend binding, not policy.ctg, and can be re-raised against fs if wanted.
