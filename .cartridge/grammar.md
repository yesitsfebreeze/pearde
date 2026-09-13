---
grammar: cartridge-system
subject: Shared cartridge development vocabulary
date: 2026-09-13
---

# Cartridge vocabulary

## This repo

| term | is |
| --- | --- |
| **cartridge** | A capability/state/lifecycle owner with a local development record |
| **memo** | An authored typed Markdown record owned by the memo system |
| **memory** | Durable learned knowledge and provenance owned by the memory engine |
| **landscape** | The graph and selected context derived from system sources |
| **board** | A Pearde-compatible development record explicitly rooted at .cartridge |
| **PRD** | One authoritative work item under its owning board's prds directory |
| **spec** | An implementable unit with acceptance checks and runnable proof, written after analysis |
| **tool document** | One owner-local Markdown source with metadata, prose and executable just recipes |
| **lens** | A commands, documentation or human projection of one source revision |
| **invocation mode** | Execution/result lifecycle such as run, sidecar or artifact; independent of lens |
| **source owner** | Canonical cartridge identity used to resolve documents and directories |
| **recursive development graph** | Root and descendant records connected by ownership and references without duplicated state |

## Words that collide

| the word | here | and here |
| --- | --- | --- |
| **state** | Pearde PRD lifecycle | Runtime/process or source availability |
| **graph** | Landscape system context | Memory engine's internal knowledge graph |
| **child** | A descendant cartridge/board | A refined PRD within a board |
| **tool** | An executable Markdown document | tools.ctg is existing development infrastructure |
