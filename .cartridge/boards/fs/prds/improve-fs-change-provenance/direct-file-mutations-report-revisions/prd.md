---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
workflow: develop-one-cartridge
capability-owner: fs
work-kind: leaf
review-round: 3
review-status: "passed"
needs:
- '@sessions/file-change-records-retain-reported-revisions'
- '@fs/improve-fs-revision-guards'
commit: "3a79023311b1a9b30c383ec8c71cf31c20a69ee7"
---

# Report the bytes each direct filesystem mutation published

Replace FS's path-only touch callback with the Sessions-owned evidence request.
Capture the exact guarded preimage, prepared postimage and host invocation
coordinates at publication; a later read cannot establish what this call wrote.
Preserve direct file semantics, guards, confinement, permissions and explicit
partial failures. Records never create GitFS overlay ownership.

## Acceptance

- [x] Successful create/write/edit records the actual storage target, actor coordinates and before/after SHA256 once, after publication.
- [x] Read/search/glob/grep/fs.context, refused writes and prepublication cancellation emit no change record; external and unrelated files remain unowned.
- [x] Known publication followed by observation, cleanup or recording failure reports partial success without replay; attribution never claims current disk freshness.
- [x] Existing FS tests/check/context SDK fixtures and real Sessions producer integration pass; legacy path tracking remains visible.

Use the current per-target lock and observations. Reuse the shared Sessions DTO
and its existing injected service, retaining old sessions data on errors. No new
observer, journal, ownership service or automatic retry. Inherit two review rounds.
