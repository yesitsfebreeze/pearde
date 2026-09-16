---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: the-agent-stages-a-flow-and-a-person-approves-it
---

# The agent stages a flow and a person approves it

The point of the flow engine is that a person describes an intent and the agent builds the topology. Port the agent surface: tools that read the graph, report what a node's paths reach, report what the graph lacks, and stage a change — and nothing that applies one. A staged change is previewed against the graph as it is now, never as it was when the call was made, and what leaves the system leaves through approval.

Approval is not this cartridge's invention here: `stage_change` is the one tool with an effect, and it routes through `policy.ctg`, which already owns tool decisions, and through the agent loop's existing approval answer. That is the composition's version of the upstream's stage-preview-approve loop, with the approver being the surface the user already answers on.

## Acceptance

- [ ] The tool surface exposes read, reachability, readiness and stage operations; no operation applies a change to a stored graph.
- [ ] A batch call answers one result per item, aligned by index, and a refused item carries its own typed refusal without affecting the other items' answers.
- [ ] A staged change is previewed against the current graph: a graph that moved between staging and preview is previewed against what it moved to, and the preview says so.
- [ ] A stage call is decided by `policy.ctg` before it takes effect; denying it leaves no staged change, and allowing it applies exactly the previewed change.
- [ ] Two tools registering the same name is refused at registration with both names in the error, rather than one shadowing the other.
- [ ] The surface answers offline in `just test flow` with the model and store seams unfilled, and an unfilled seam refuses by name rather than answering empty.

## Proof and recovery

Port from upstream `ctrl` `src/agent/` (tool, surface, turn, proposal, author, graph, report, claim, search, packet, error). Drop upstream's `src/chat.rs`: the composition's model turns belong to `agent.ctg` over `router.ctg`, and this cartridge fills the model seam from there. Drop upstream's `--stage-out` file approval in favour of the policy decision. Upstream's `src/serve.rs` HTTP control plane is not ported in this child; a UI surface over these same operations is separate work.

Depends on the workflow graph child. The corpus-backed search and claim tools are declared here and answered by `memory.ctg`.

Gates, cwd `/Users/feb/dev/cartridge`: `just test flow`, `just check flow`. Not run for this plan.
