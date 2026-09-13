# Native tool observation proof

Source `a6cbab2d78fe1c45ff6545518a558051fcafad2e`; independent /root round 3 95/100 PASS. [Inputs and hashes](proof-inputs.json).

- Public `just test runtime`: 162 library and 2 binary tests; existing memo-run suite 4 tests/47 assertions ([log](proof-test.log)).
- Public `just check runtime`: formatting/Clippy pass ([log](proof-check.log)).
- Actual runtime binary built through composed Cargo manifest ([log](proof-build.log)); native subprocess integration 3 tests/38 assertions ([log](proof-integration.log)).

Real fixtures cover host-configured agent/UI/polling and unknown sources, intrinsic discovery, copied request attribution, actual same-generation descriptor changes, generation isolation, success/tool-error/transport/malformed/interrupted/cancel outcomes, response byte counts, disabled/failed/rotated sinks and native partial-reply exit. Unit checks additionally abort a live guard, poison the descriptor cache, and prove intended-Service binding ignores nested services and clears generation on explicit resume.

The first CLI baseline lacked --dir and failed before dispatch; the corrected captured baseline succeeds with zero tool diagnostics. Initial integration exposed the broad legacy redactor hiding completion_known; it now exempts only boolean/null metadata, retaining string redaction. Actual source naming uses wrapper source names, not arbitrary profile IDs. An abrupt native-provider failure can tear down the host before a completion record; the test accepts an orphan attempt as unknown and refuses any known-success claim. No result is fabricated.

Metadata source coverage and limitations are documented in runtime .cartridge/docs/tool-observations.md. Existing generic fault diagnostics are separate; the new tool observations omit arguments, bodies and error text. All fixtures disposable; no profile settings or user data changed. Runtime source is stable for coordinator collection.

Collection handling: verification commands explicitly use the actual composed runtime checkout. A detached lane at the exact committed runtime HEAD provides the collector clean-tree integration boundary; unrelated dirty files remain in place. No tests were removed or weakened and no source was moved/stashed. See [cwd binding](collection-cwd-binding.json) for exact before/after digests; collector still validates the declared source footprint.
