# Verified durable channel delivery progress

Source `c2693a7ca3e23c295b8fe52a664720dde137eedc`. [Exact source, binary, command and log digests](proof-inputs.json). Independent root review remains round3, **96/100**; no acceptance changed.

- Public sessions test/check/build pass: **78 native tests**, including all70 previous tests and8 cursor tests.
- Reviewed SDK subset passes **9 tests /310 assertions**; full earlier-feature compatibility passes **19 tests /448 assertions**, with real sessions, harness and runtime processes.
- Watches and pending receipts survive restart. An acknowledged batch advances only its authenticated actor and delivered boundary; later posts stay unread. Concurrent reads retain one current receipt and stale/cross-actor acknowledgement fails.
- All four write/file-sync/rename/directory-sync failure stages are exercised across watch, read, ack and unwatch. Accepted lines remain identical; pre-publication state is preserved and uncertain visible progress reconciles explicitly.
- Empty or unfit reads do not write state; byte/row caps include actor/channel metadata. Unwatch removes only its owner cursor; rewatch deliberately redelivers.
-16-watch/256-actor caps, malformed/duplicate/out-of-range registry states and generic metadata forgery are refused or unable to alter the separate owner registry. Existing legacy channel and direct mailbox tests remain unchanged.

Fixtures use disposable data and synthetic credentials. The child does not implement the held roster projection or harness adapter. Coordinator collection waits for refreshed shared dependency receipts; no shared PRD collection or unrelated source change was performed here.
