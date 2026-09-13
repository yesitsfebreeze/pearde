# Durable scoped channel proof

Source `423ecd329a98d0e0702a71c9ccb0a33a16cedae6`. [Exact source/binary/log digests and commands](proof-inputs.json). Independent coordinator review remains round 1, **96/100**; no acceptance was weakened. Historical active source and claim are unchanged, verified against the baseline hash.

- Public sessions test/check/build pass: **70 native tests**, retaining all 60 previous tests plus 10 channel tests.
- Final actual SDK compatibility passes **16 tests / 368 assertions**, covering channels, mailbox, retention/harness, mapping and runtime observations.
- Two same-scope actors post concurrently with unique monotonic sequences; same-ID retries return one line and mismatched payloads fail. Restart preserves channel lines, catalogue and sequence. Separate scopes retain independent state.
- Direct aliases read true legacy rows without rewriting snapshot bytes, and posts through aliases appear in the existing mailbox with one buffer. Existing mailbox acknowledgements and legacy512-byte send cap remain intact.
- Bounded continuous catch-up and catalogue pagination preserve every delivered prefix. Beyond-end reads return empty; unsafe names, forged senders/scopes, unauthorized direct reads and oversized text are refused.
- Write/file-sync/rename failure preserves accepted bytes; directory-sync uncertainty is explicit and retry reconciles the visible record without a duplicate notification. A replaced pre-commit target conflicts. Corrupt/truncated/unknown-field/symlink evidence is preserved.
- Real serialized8MiB,10000-line and128-channel capacities refuse new posts without eviction; simultaneous initial creation across scopes succeeds. Catalogue labels an unavailable mailbox contributor partial.

All mutation/failure fixtures use disposable data and synthetic credentials. The coordinator must refresh the stale mailbox dependency and other shared sessions receipts before collecting this leaf. No collection or historical claim update was performed by the implementer.
