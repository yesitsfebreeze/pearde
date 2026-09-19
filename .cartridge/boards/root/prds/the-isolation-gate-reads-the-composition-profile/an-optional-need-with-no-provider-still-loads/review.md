# Fast-path eligibility — 2026-09-19

The current review workflow explicitly permits the trivial-PRD fast path when
one spec changes at most two files in one cartridge, no declared manifest
surface, setting, need or event changes, and a test block names the regression.
This fix changes only host dependency validation and its existing test file.
It preserves optional send permissions and restores the existing documented
exact-optional contract; it adds no need declarations. The spec above names two
real-host regressions and full owner proof. No numeric review score is claimed.
The author implements in the engine lane; a fresh independent verifier must
rerun every block and read the diff before collection. Any behavioral gap or
failure of these eligibility conditions moves this leaf into ordinary round 1.

## Independent implementation verification

Verifier /root/optional_needs_verifier passed candidate 54749f4309860bb39555570298f3e14957d7dfef and every fast-path condition. The complete diff was read. Both new real Host regressions independently fail on unchanged base and pass on the candidate; all seven plan tests, 186 library tests, 22 binary tests, formatting and strict Clippy pass. Full suite wall time was 108.82 seconds after prebuild, with contention risk explicitly retained. Report and logs: ../../../.state/loop/an-optional-need-with-no-provider-still-loads/verifier-codex-1.md. Coordinator checked all canonical input hashes before ticking the three PRD and three spec criteria. No plan requirement or command changed. Collection and current composition checks remain required.
