---
kind: work
level: 10
status: done
estimate: 2h
actual: 30m
description: Every `just` build in this repo runs uncached — kache reports its index cannot be opened (SQLite code 14) and disables caching — while its store sits at 174% of the configured limit and gc has been unable to evict since 2026-09-07.
read_when: approving or running the bounded investigation into the disabled kache index and its over-limit store
---

# the-build-cache-is-off-while-its-store-sits-over-limit

## Do

Approved 2026-09-08 as "Approve + allow the fix" [[approve-kache-index-open-investigation]]. The measurement below is authorized, and so is the remedy it points to — `kache gc`, `kache purge`, installing the daemon service, or a config edit — in the same run, without a second approval.

Observed defect, measured 2026-09-08 in `/Users/feb/dev/memory` on macOS 25.2.0, kache v0.16.0 at `/Users/feb/.cargo/bin/kache`, code revision `36d6def6`. Two `just memos-check` runs, at 10:11 and 10:33, each printed `[kache] the cache index could not be opened after retries (opening index database /Users/feb/Library/Caches/kache/index.db: unable to open database file: Error code 14: unable to open database file).` followed by `[kache] Caching is disabled for this build`. The file is present and 271,831,040 bytes, last written 09:31, and `KACHE_CACHE_DIR` is unset. `kache stats` opened the same database from the same shell moments later, so the failure is specific to the build, not to the store being unreadable.

Two conditions sit beside it, both measured and neither established as the cause. `kache stats` reports `Store: 26.0 GiB / 15.0 GiB (4574 entries, 174%)` — the store is 74% over its configured limit — and `Users/feb/Library/Caches/kache/auto-gc.log` has been repeating `gc: skipping eviction of <hash>: database is locked: Error code 5` since 2026-09-07T21:28, so nothing has been evicted for a day. `kache daemon` reports `Service: not installed` and `Daemon: not running`, and `kache stats` announced `no daemon reachable ...; starting one inheriting this process's environment` — that read started a daemon, which is a side effect of this assessment worth naming.

Proposed scope: measure, then remedy. Reproduce the warning with one `just memos-check`, run `kache doctor` and read its report, and establish whether the index open fails because of the over-limit store, a stale lock from the absent daemon service, or concurrent wrapper processes. Land the finding as one memo, naming the condition found. Then apply the remedy that condition calls for — installing the daemon service, raising the limit, `kache gc`, or `kache purge` — stating what it writes or removes before it does. Every one of those touches a 26 GiB store shared by every project on this machine, which is why the measurement is written down first.

Benefit: [[@prd/routine/run-board.md]] states that a lane's first build is seconds "because kache already holds every crate a sibling lane compiled", and [[lanes-not-a-shared-tree]] rests on the same property; with caching disabled that property is false for every lane opened today, and `kache stats` already shows 87.4% of wrapper time going to misses. Tradeoff: the remedy is authorized before the cause is known, and it writes to a store other projects share. Preserve what works: `kache stats`, `kache daemon` and the cache directory itself all read fine, and builds still succeed uncached — no remedy may trade a working build for a faster one. `KACHE_CACHE_DIR` stays unset unless the measurement names it as the cause.

## Check

Already run, 2026-09-08: `just memos-check` printed the index-open warning and `Caching is disabled for this build` on both runs while its three tests passed; `kache stats` printed `26.0 GiB / 15.0 GiB (4574 entries, 174%)`; `kache daemon` printed `Service: not installed` and `Daemon: not running`; `tail -5` of `auto-gc.log` showed five consecutive `database is locked` eviction skips dated 2026-09-07T21:28 and T21:52.

Unrun: `kache doctor` output, and a statement of which of the three candidate conditions the index-open failure actually follows from. Then, after the remedy: `just memos-check` runs without the `Caching is disabled for this build` line, `kache stats` reports the store at or under its limit, and the build still succeeds.

Run `just memos-check` once after the finding memo lands and require success. Its own kache warning is the reproduction, not a gate failure to fix.

Done 2026-09-08. The finding is [[no-daemon-is-what-turns-the-build-cache-off]]: the index-open failure follows from the absent daemon, not the store — `kache.log` records the daemon auto-starting at 08:46:25Z, after both 10:11 and 10:33 local failures, and no build has printed the warning since. Remedy applied: `kache daemon install` (service installed and running, `kache doctor` all green) and `kache gc` (59 entries, 3.1 GB freed).

Two of this memo's own numbers did not survive the measurement. `kache doctor` reports no fault at all, so it named no condition; the timestamps in `kache.log` did. And the Check's "`kache stats` reports the store at or under its limit" cannot pass as written: `kache stats` prints the logical entry sum against a cap `kache gc` enforces on physical bytes, so it reads `25.0 GiB / 15.0 GiB (166%)` while the store is 13.4 GiB on disk and a second `kache gc` frees `0 B` — gc is at its floor and the store is bounded. The rest of the Check passed literally: a cold `just memos-check` in the lane built in 14.90 s with three tests green and no `Caching is disabled for this build` line.
