# Actual router decision verification

The measured baseline selected fixture@last but exposed no decision ID. The
implementation passes 29 router tests (6 protocol and 23 executable), public
router check, 21 existing proxy tests and 15 MCP tests including real headless
policy inspection (27 assertions). Logs are retained beside this record.

Actual loopback fallback tests distinguish capability/context rejection, health
backoff and failed attempts; selected route matches headers. A controlled policy
reload during first-attempt suspension proves fallback uses the captured effort
and attribution revision. Equivalent config order and token rotation preserve
revisions; policy change/rollback changes/restores them without editing archives.

Opt-in/default response shapes, unknown/evicted IDs, bounded retention, cancellation,
stream_started state and synthetic credential/OAuth/body/error redaction pass.
Streaming receipts describe selection at handoff, not completed delivery. Health
observations are dynamic; preflight is not an execution promise. Context estimation
remains the documented heuristic from capability admission.

Runtime dependency integration: fb5734a (only the router sha2 lockfile entry).
Proxy compatibility gate was launched from clean480a before independent continuation
source work began; that worker will also verify its final revision against this
router. MCP source is f5a740517bc2668b50cf4f61fe81a1e37bb4cfad.
