# Scope owner baseline handoff

The requested scoped baseline is committed locally and available to checked lanes starting at HEAD.

- Base: `b4345b6dc5d03d33900ff7fb793f7dd752f5757d` (`feat(scope): move the ASP browser and composable finder into base`).
- Root: `a5b2719369a965b93301e441a04d8642289e087e` (`feat(scope): retire the legacy UI and pin the base browser baseline`).
- Root pins memory's existing owner baseline: `d9161cd2f3a363915c7a7d642a4955e7a3836065`.
- Verified base tree: `987a5cd781046327fbfdfff23f54b4924751be8b`. The independently built checkout's staged tree equals the committed tree exactly. File hashes and selected patch are in owner-base-files.json and owner-base-selection.patch.

## Included scope

The complete embedded Python UI and its 30 tests, Scope CLI registration, ASP root/event graph and declared schema support, bounded expansion, retained activity and observe:false monitoring, ASP tests, and Scope/ASP documentation are included. The root launcher now invokes the base UI; all seven legacy UI source/test files were deleted. Root gitlinks identify the base and existing memory baseline above.

Shared README/help changes were selected by content against HEAD. Scope and required ASP documentation were included. Bootstrap, passthrough and prompt-recall changes were excluded. The runtime PRD a-listener-subscribes-to-event-types was directly re-read before committing: it records failed and has no claim. No claim was released, taken over or collected here. Unrelated dirty work remains preserved.

## Verification

- `cargo check --locked` passes in /tmp/scope-owner-baseline-20260919 with CARGO_TARGET_DIR=/tmp/scope-owner-baseline-target.
- All 17 ASP tests pass against that selection (base-asp-tests.log). The tree fixture checks roots, event schemas, dispatch observation and provider removal. Durable trace sender tests remain with their runtime owner, outside this baseline.
- All 30 UI tests pass from the isolated source checkout (ui-tests.log).
- The exact isolated binary passes embedded `scope --once` and real PTY launch, file filtering and Ctrl-Q exit against a temporary composition. The source client/engine additionally passes actual ASP > Grep and Files > Grep against that host (probe_baseline.py, pty-output.bin).
- Three real plugin renderer cases pass through the isolated binary (renderers.log). These exercise current provider working-tree scripts, not a claim that those provider edits are committed. The root test now accepts CARTRIDGE_TEST_BINARY; that untracked integration fixture remains outside the baseline pending provider collection.
- The launcher command and quoting pass through a separate temporary host. No existing tmux pane was opened.
- Scope audit hard checks and composition isolation pass (audit-scope.log, isolation.log). Audit still reports unrelated repository churn. `audit runtime` is not a valid target and was not counted as a passing gate.

## Boundaries and incident

Memory-owned detail declaration/wiring and new status semantics remain for the memory owner to select and verify. No memory working-tree content was committed here. The base works with generic details without these extensions. Other provider renderer changes and runtime durable trace plumbing are also excluded.

The first host probe mistakenly used --dir without setting subprocess cwd. Host descriptors resolve from cwd, so its calls and cleanup could reach the shared composition. This was corrected before the passing isolated proof; all subprocesses now explicitly use the temporary project cwd. A subsequent read-only status check showed all 21 shared cartridges active. The live executable was never rebuilt or replaced. This initial attempt is not isolation evidence.

This is a migration prerequisite handoff, not PRD collection or completion of the active finder goal. The latest layout is preview above, centered command input, results below; F4 selects waterfall/detail. Future memory integration must target this implementation and the pinned baseline, not the removed scope.ctg/src files.
