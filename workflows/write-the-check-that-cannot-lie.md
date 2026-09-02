---
atomic: write-the-check-that-cannot-lie
subject: Turned the correct measurement into a command, and made it fail on an injected bogus id and refuse an absent store — it reported 13 false danglers before that
date: 2026-09-02
runs: 1
---

## Do

1. Write the correct measurement as a script with distinct exit codes for pass, fail and cannot-run.
2. Resolve and test for the target before invoking the tool, so an absent target is never manufactured.
3. Inject a known-bad item and confirm the script fails on it; restore the file.
4. Run it three times and confirm the exit status is stable.

## Done when

- The script passes on the real data, fails on an injected bad item, returns a distinct code when the target is absent, and creates nothing.

## Fails when
