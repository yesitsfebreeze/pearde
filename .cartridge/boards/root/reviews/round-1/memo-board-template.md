---
state: open
origin: requested
priority: 100
blast-radius: high
workflow: develop-one-cartridge
footprint:
  - /Users/feb/dev/cartridge/memo.ctg/seeds
  - /Users/feb/dev/cartridge/memo.ctg/src/record.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/service.rs
  - /Users/feb/dev/cartridge/memo.ctg/tests
  - /Users/feb/dev/cartridge/cartridge.ctg/scripts/workspace.py
---

# The memo cartridge supplies a Pearde-compatible project template

A new project gets a .cartridge board with the same PRD, workflow, evidence, and transition semantics as Pearde. The root coordinates owner-local child boards recursively; installing this reusable template must become a supported memo operation.

## Ownership and scope

Owner: `memo`. Participating repositories: `memo.ctg`, `cartridge.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Probe the current root board with real Pearde scan, memo check, workflow check, and a temporary nine-state fixture. Capture the explicit-board requirement; never rely on discovery selecting .cartridge instead of an existing .pearde.
2. Package the template with memo. Add an explicit initialization operation that previews files, fills project identity/paths, and installs missing files without replacing existing settings, profiles, records, or stores. Repeating initialization must be idempotent.
3. Expose board PRDs/specs/workflows to memo and landscape as source references, not duplicate work records. Keep PRD state authoritative and preserve unknown Pearde metadata.
4. Route transition commands through the existing Pearde engine initially. Name the engine dependency and supported revision; any later native implementation must pass differential fixtures before replacing it.
5. Resolve the observed CLI gap: this installed revision treats `plan <path>` as a group and implicit discovery skips `.cartridge`. Keep the working explicit-board scan while adding a supported full-planner/transition adapter. Cover root and child boards coexisting with the runtime's older `.pearde` record; do not rename either implicitly.

## Acceptance contract

- Initializing an empty temporary project creates only the documented .cartridge layout; a second initialization has an empty diff.
- An existing profile, edited decision, and memory-store sentinel survive initialization byte-for-byte; a conflicting template file is reported by path.
- Pearde scans the generated board, resolves needs, refuses an invalid transition and an overlapping claim, and re-runs a failing verification instead of marking done.
- Memo can find and read a PRD and its decision without inventing a second status; template-generated paths contain no developer home directory.
- The template's workflows and memo view pass Pearde's validators.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test memo
just check memo
just board-check
```

## Failure and recovery

A template upgrade silently overwrites active work, or nested directory discovery picks the old runtime board. Refuse collisions and always pass the shared board path.

Rollback: Remove only files recorded as newly installed by the initializer; never remove or rewrite a pre-existing .cartridge. Retain external Pearde execution until native parity is proven.

## Prior context

Related existing runtime memo leaf names: `a-tool-is-declared-by-its-memo`, `every-tool-is-one-command`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
