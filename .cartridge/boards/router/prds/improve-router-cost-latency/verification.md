# Cost and latency verification

Source0a216cb supplies 35 passing router tests (6 protocol +29 binary), public
router check, and 15 MCP tests including27 real policy assertions. Exact logs
are retained. Current proxy continuation collection runs25 tests/check against
this source; it is a separate owner change, without live model calls.

Loopback failed-first/successful-last responses retain2/1 and12/3 actual token
snapshots respectively. At synthetic2/4 USD per million rates, subtotal0.000044
counts each attempt once; total remains unknown because first attempt is partial.
Explicit request budget produces a distinct preflight estimate. Buffered usage
2/1 then12/3 does not become a decreasing or duplicated observation on replay.

Unit fixtures cover missing versus zero, malformed/decreasing counters, all three
wire schemas, stale/future/invalid/missing prices, overflow, cancelled/omitted
attempts and subtotal versus total. Monotonic elapsed time bounds first-output
time. Price change/rollback preserves immutable old reports. Native preflight
has no measured latency. Stream_started remains an immutable partial handoff
record, not a delivery or billing receipt. Synthetic fixtures only.
