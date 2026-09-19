# asp-shows-recently-used-memory-and-its-reasons review history

Plan: memory::asp-shows-recently-used-memory-and-its-reasons, [prd.md](prd.md). This is an executable leaf. There are no inherited rounds. The independent reviewer is `/root/architecture_review`. The round limit is five and the delegated passing threshold is 90/100. The user supplied no numeric rating.

## Round 1 — 2026-09-19

This assessment binds the uncommitted plan and material source content below. Specs are not yet applicable. The user’s current clarification requires Memory to stand alone as a clean project following cartridge conventions.

| Input | SHA-256 |
| --- | --- |
| Plan | `9b935ffb132a371abbf4780398b713338cdb6712ed992ed7b5d21df482b2064d` |
| `memory.ctg/Cargo.toml` | `f6d80a68e49b82c4a2407d038439c88722b84a48f086781aa8e836f7dff5c173` |
| `memory.ctg/src/graph/Cargo.toml` | `2b9ae3f4fba08e3265c4296045d73781a340420e6a1e2c7918deb7ab8329a3f8` |
| `memory.ctg/README.md` | `d20da0add5999f0eaf16cea4335c4d8dd0f278738c083fab77fb1b5d071e86ba` |
| `.worktrees/memory-crystallization/src/cartridge/src/asp/search.rs` | `01b1001b920387b82397fd9f027efe3ba958504ff9d643479fb76d542b038069` |
| `.worktrees/memory-crystallization/src/cartridge/src/asp/expand.rs` | `77124d73c29f467a059b8df89d6dcfe523a111851c04eedc0c1f92d0ba3b991b` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The leaf exposes recent retrieval usage distinctly from recurrence. |
| Ownership and reuse | 19 | ASP and Scope remain generic consumers of the memory-owned graph. |
| Dependencies and implementable slices | 17 | A bounded projection is named, but continuation of larger groups and dependencies are underspecified. |
| Observable acceptance and baseline evidence | 16 | Visibility and non-mutation are specified, but named tests and an integrated proof boundary are missing. |
| Failure, recovery and compatibility | 16 | Direct reason visibility, revision stability and truncation recovery need concrete contracts. |
| Reviewer total | 87 / 100 | FAIL. |

Specify how a group larger than 256 nodes remains navigable, using bounded continuation or an explicit bounded projection contract with discoverable truncation and a route to omitted entities. Add a named integrated test for search and expansion with access/heat/recurrence unchanged, since the current ASP search calls op=query and records access. Specify visibility checks on direct reason-ID expansion, including private or inactive endpoints. Clarify that observational usage attributes do not change the content/provenance revision. Add a proof/recovery section and explicit prerequisite links.

Validation consisted of executing `./task prompt`, reading both PRDs and the recorded source, and computing SHA-256 digests successfully from `/Users/feb/dev/cartridge`. No runtime proof is claimed by this planning review. The task runner has changed from `just` to `./task`; implementation evidence should use the current runner.

Disposition: revise. Result: FAIL. Unresolved blocking findings: the contract and proof gaps above. Rounds used: one; remaining: four. Next action: revise the bounded projection contract and obtain round 2 review.


## Round 2 — 2026-09-19

The revised uncommitted PRD resolves the previous contract gaps. The implementation remains in progress and is not approved by this plan rating.

| Input | SHA-256 |
| --- | --- |
| Revised plan | `e41343f9d654a8ccd8409217ba5c6ac23f6d5ce8c9b5a6f73d825c51a6d28758` |
| `.worktrees/memory-crystallization/src/rpc/src/experience/view.rs` | `bb14d9bd750fb921af0822e3bdc4b80e3dd7fd34f7e198971dd12bd980ae077d` |
| `.worktrees/memory-crystallization/src/cartridge/src/asp/mod.rs` | `95bca2ce20cd384e0a6068d5145932473b7609f747c02a546fbdca771084287c` |
| `.worktrees/memory-crystallization/src/cartridge/src/asp/expand.rs` | `77124d73c29f467a059b8df89d6dcfe523a111851c04eedc0c1f92d0ba3b991b` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The graph-native navigation and recent-use distinction remain intact. |
| Ownership and reuse | 19 | The memory engine and adapter retain their established boundaries. |
| Dependencies and implementable slices | 18 | Three prerequisite leaves are named, with independently verifiable existing-memory navigation. |
| Observable acceptance and baseline evidence | 19 | Named graph/RPC/cartridge tests cover continuation, hidden endpoints and non-mutating browsing. |
| Failure, recovery and compatibility | 18 | Malformed continuation refusal, stable content revisions, direct endpoint visibility and refresh semantics are explicit. |
| Reviewer total | 93 / 100 | PASS. |

All round-1 planning blockers are resolved. Continuation tests must cover entity reason pages as well as group pages, asserting that every returned edge originates from a returned node and reaches a returned child. Continuation subjects must retain the same adapter evidence and privacy checks as direct expansion. A bounded response should serialize only the selected page, rather than constructing JSON for every graph entity before slicing.

Source inspection of the in-progress implementation identified violations of those contracts and reported them to the coordinator. They do not change this assessment of the revised plan; they must be fixed and tested before implementation completion. Validation in this round consisted of reading the revised PRD and named source and computing SHA-256 digests. No runtime test was run during this round.

Disposition: keep. Result: PASS. Unresolved planning blockers: none. Rounds used: two; remaining: three. Next action: complete implementation, fix the reported continuation and bounded-work issues, then execute the named proof.
