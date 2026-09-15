---
repo: /Users/feb/dev/cartridge
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
description: "Keep same-named Markdown documents from composed cartridges independently addressable and compose their system guidance"
---

# Cartridge memos keep their qualified identity

## Outcome

Every shipped Markdown memo retains its exact `@<cartridge>/<kind>/<name>.md` identity when cartridges compose. Same-named or identical documents from different cartridges coexist and remain readable; workspace shorthand does not erase qualified source documents. System messages include every enabled contribution in deterministic order and expose the shipped source path. Ambiguous unqualified external references never select an arbitrary cartridge.

The user explicitly requested this after the live error `@memory/system/type.md: also provided by cartridge memo`. It is a code prerequisite for robust composition, discovered while completing [restore-mcp-work-pass](../restore-mcp-work-pass/prd.md). The user delegates plan ratings to agents.

## Baseline and cause

The old merge in memo.ctg/src/record.rs compared file leaves across every source, discarded identical/workspace-shadowed shipped documents, and rejected differing text. Its later validation and usage/ref indexes also assumed globally unique leaves. Landscape's surface graph overwrote its leaf-to-path index, silently selecting a contributor. Isolated regressions reproduced both the exact duplicate-provider error and the wrong graph edge before changes.

A concurrent record relocation moved current root memos out of cartridge.ctg. The existing MCP profile's trusted cwd still selected the old record. The coordinator changed only `mcp.cwd` from "." to ".." in cartridge.ctg/.cartridge/mcp/config.lua; the existing connection hot-reloaded and successfully read routine/work-pass.md at its unchanged digest. This corrects record selection, independently of the namespace behavior.

## Approach

1. Implement in isolated sibling Git worktrees for memo.ctg and landscape.ctg under /tmp/cartridge-namespace-check, against explicit owner HEADs; keep the task workspace support outside delivered code.
2. Preserve every qualified shipped document in merge/read/list/types/system. Local record rules remain scoped to local ownership. Shipped legacy grammar must not invalidate unrelated reads.
3. Resolve exact qualified paths first; contextual relative references prefer their cartridge, then workspace, then a unique remaining candidate. Return explicit ambiguity for unresolved unqualified multi-candidate lookups; graph projection omits ambiguous edges. Usage identities and supersedes relations use canonical targets rather than overwrite-prone leaf maps.
4. Preserve all type declaration candidates in the derived index. Resolve shipped resource target files relative to their owning cartridge, never a same-relative-path workspace file; keep path containment checks.
5. Prefix shipped system template sections with their qualified source path while preserving source text and revision on read. Update applicable seed/reference docs without rewriting unrelated historical records.
6. Run original red-to-green regressions, full memo and Landscape test suites, formatting and Clippy. Independently review the diff. Integrate only owned paths after verifying live source bases; build only memo_cartridge and allow the existing watcher to reload it.
7. Reproduce live qualified reads, composed system provenance, resolver and graph queries through the existing MCP connection, then finish the work-pass record's completion readback.

## Review

Coordinator design review: 94/100 (value 20, ownership 19, dependencies 18, acceptance 19, recovery 18), no blocking design finding after the namespace/reference consumers were included. Independent reviewer /root/workflow_reviewer checks resulting code. One substantive plan round; five-round limit retained. No user number requested or invented.

## Acceptance
- [x] Differing and identical same-named shipped memos remain listed and independently readable by qualified path, including when a local same-leaf memo exists.
- [x] System composition contains both enabled contributions with qualified source attribution and deterministic ordering.
- [x] Contextual and explicit cross-cartridge references/uses resolve correctly; bare ambiguity never chooses by provider/input order.
- [x] Type-index candidates, supersedes, and resource/coverage behavior preserve source identity and target ownership.
- [x] Memo and Landscape regressions/suites, formatting and Clippy pass on the integrated revisions; independent review has no blocking findings.
- [x] Existing MCP reads/resolve/system/landscape succeed on the relocated root record after targeted build/reload; final evidence is read back.

## Verification commands

From /tmp/cartridge-namespace-check after integration and byte comparison against the live sources:

```sh
cargo test --manifest-path cartridge.ctg/workspace/Cargo.toml -p memo_cartridge -p landscape
cargo fmt --manifest-path cartridge.ctg/workspace/Cargo.toml -p memo_cartridge -p landscape -- --check
cargo clippy --manifest-path cartridge.ctg/workspace/Cargo.toml -p memo_cartridge -p landscape --all-targets -- -D warnings
```

The task-only workspace is used because concurrent migration removed the live cartridge.ctg/workspace/Cargo.toml. The attempted original live test command failed with manifest-not-found (exit 101); no source test failed. All source/test/seed files and Cargo.toml were byte-compared between integrated and isolated copies: memo 31 files, Landscape 3, runtime 45, excluding .DS_Store metadata. Live MCP probes read two exact same-leaf qualified documents, request system composition, and resolve/read routine/work-pass.md from the relocated root. Record actual revisions and commands, including failures.

## Failure and integration

Preserve isolated attempts and original errors. Do not fix duplicates by deleting source documents, changing unrelated claims, weakening path containment or expanding tool grants. Reconcile concurrent code changes rather than overwrite them. A failed live reload or acceptance check remains explicit; earlier fixture passes do not establish current completion. Routine restoration and the namespace fix retain distinct evidence.

## Result

Code integrated locally: memo.ctg `604f47e4bd1f6da661490918bc302f4e33443e6d`, landscape.ctg `361374c6b1e2a6d0736e57904a004d7ae5a79dad`; superproject pins `b8d6f4e`. MCP cwd correction is runtime commit `8379190`. No push or deployment was performed.

Original failing regressions now pass. Combined validation: 35 memo tests and 15 Landscape tests passed, formatting check passed, Clippy all targets with warnings denied passed, source diff checks passed. Independent code review by /root/workflow_reviewer found two issues (qualified-reference resource fallback and shipped coverage paths); both fixed and regression-tested before approval. Full implementation report: /tmp/cartridge-namespace-fix-report.md.

Concurrent cleanup also removed the live target directory. The coordinator built only the memo executable from verified identical sources, atomically installed it at the existing canonical binary path and touched the existing memo init.lua mtime to notify its surviving watcher. No tracked wrapper content changed. Live memo PID changed from 89088 to 70090; MCP PID34519 remained connected. Other removed build scripts/artifacts were outside this fix and were not recreated.

Executed existing-connection MCP checks: `@memo/type/type.md` revision `71f82003eaa30155dc564fd89bfc3aca6ef39ab8342e762d0ec7524c8dd56cf0` and `@memory/system/type.md` revision `b7ed13f34630069eb4307c8a3ad174e56cf895c0fdbe912fe08385b126b42cb4` are independently readable despite their shared leaf. The latter lives in a legacy system folder but declares kind:type. Same-kind enabled system duplicates are covered by executable fixture tests; the live profile currently has 11 enabled system memos, with qualified headings for @memo/system/resolver-guidance.md and @memo/system/program-entry.md. System, resolve and landscape all succeed; Landscape reports the new memo generation active and current sources unchanged. Resolve ranks routine/work-pass.md first at score30.5.

The root type/type, type/system and type/usage instructions now match the namespace contract. The restored coordinator's creation rule requires workspace-local leaf uniqueness and preserves shipped qualified identities. These are validated MCP writes with exact readback; published work-pass revision is `88d0495361e5093b4cc0ac922273065ba67ee11226f2273b693b099797345f6a`. Workflow continuation remains tracked in [restore-mcp-work-pass](../restore-mcp-work-pass/prd.md).

Final independent local/doc verification by /root/workflow_reviewer: PASS, no blocker. Report: /tmp/cartridge-namespace-live-verification.md; reviewer lacked MCP tool exposure in the resumed turn, so live transport probes remain coordinator-executed evidence independently inspected. Final root MCP resolve confirms work-pass revision88d0495361e5093b4cc0ac922273065ba67ee11226f2273b693b099797345f6a; saved in /tmp/cartridge-namespace-final-resolve.json. Result was read back before completion.
