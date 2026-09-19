---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/policy.ctg"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: policy
work-kind: leaf
footprint:
- "init.lua"
- "cartridge.json"
- ".cartridge/tests/policy.rs"
- ".cartridge/docs/explain.md"
- ".cartridge/docs/policy.md"
- ".cartridge/help.md"
needs:
- "@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/the-host-answers-policy-and-policy-explain-with-the-evaluator-policy-ctg-had"
---
# Policy refuses unbounded searches with a teaching reason

Port the checks of `pi/packages/coding-agent/src/core/search-guard.ts` into `policy.ctg/init.lua` as pure Lua rules. Because the policy "knows no tool", the guard is opt-in configuration naming which tool and input field carry a command line (e.g. `policy.search_guard = { shell = "command" }`, declared in `cartridge.json`, default empty); the composition enables it for `shell` (pty's `tool.shell`, `input.command`). Each command is split on `&& || ; |` and newlines outside quotes. Refused: `grep` with a recursive flag whose roots are absent, `.`, `./` or `/` (unless it excludes `.git` and a vendor dir); `find` whose roots are absent, `.`, `./`, `/` or `~` without `-maxdepth N`. A leading `# guard-off` line is a per-call override.

## Acceptance

- [ ] `grep -rn x .` and `find . -name x` on the guarded tool get `deny` with rule `search_guard.grep` / `search_guard.find` and a reason naming the unbounded part and a bounded form; the same through `policy.explain`.
- [ ] `grep -rn x src`, `find src -name x`, `find . -maxdepth 2 -name x` and a chained `cd x && find . -maxdepth 1` are not refused by the guard (they fall through to the ordinary rules).
- [ ] `# guard-off\nfind . -name x` is not refused by the guard, the response carries `override` naming the bypassed rule, and the next call without the marker is refused again.
- [ ] A tool not named in `search_guard`, and an empty `search_guard`, are unaffected; an explicit tool/operation `deny` still wins over an override; invalid `search_guard` config is rejected and the prior policy retained.
- [ ] `policy` responses carry `rule` (and `override` when set) so consumers can record them; the evaluator revision version is bumped; `.cartridge/docs/explain.md`, `policy.md` and `.cartridge/help.md` name the rules and triggers.
- [ ] All of the above are table-driven cases in `just test policy`; no shell is spawned.

## Proof and recovery

Footprint: `init.lua`, `cartridge.json`, `.cartridge/tests/policy.rs`, `.cartridge/docs/{explain,policy}.md`, `.cartridge/help.md`; composition enablement in `/Users/feb/dev/cartridge/.cartridge/config.lua` (currently dirty in the shared checkout) plus the `policy.ctg` pointer. Gates, cwd /Users/feb/dev/cartridge: `just test policy`, `just check policy`.

The composition enablement in `/Users/feb/dev/cartridge/.cartridge/config.lua` is a separate superproject change. It lands after this leaf, through the parent collection or a follow-up. This leaf proves the rules with fixtures.

Split from `@policy/bounded-search-guard-rules` on 2026-09-16 (analyst-1). No review rounds used before the split.

Per the user's 2026-09-19 answer on `@policy/bounded-search-guard-rules/the-policy-owner-gate-runs-against-the-current-host` (deferred, superseded by the runtime child above), the policy evaluator this PRD's rules extend is moving to `cartridge.ctg/src/policy`; `policy.ctg` itself is being removed. This leaf's repo and footprint (`init.lua`, `cartridge.json`, `.cartridge/tests/policy.rs`, the `.cartridge/docs/*` and `.cartridge/help.md` files, all under `policy.ctg`) still name the outgoing Lua module. Its analyst must re-home the footprint onto `cartridge.ctg/src/policy` (likely moving this PRD, or its footprint, onto the runtime board) before speccing, rather than porting Lua rules that are about to have no host.
