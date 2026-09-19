---
commit: fa3490b6ed4229d09687e6183b6430870a854c84
spec-digests: {"spec01.md":"bfed7d7186e49ce37ae631587d9a1f9494962763bd889ae921f3432bf88830ee"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/auth/prds/auth-answers-a-jev-question-on-the-stored-typesafe-key/specs/spec01.md: exit 0

Command SHA-256: feb7df98bfdd1205b277fa4432d4b204fbbae4a729b68774309b1ea2ed572a7d

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/auth/prds/auth-answers-a-jev-question-on-the-stored-typesafe-key/specs/spec01.md: exit 0

Command SHA-256: c61572eecb7052781a5f2132525efe206f2f2d40492632cfd4e0f349b1ff761a

```text
bun install v1.3.14 (0d9b296a)

Checked 5 installs across 6 packages (no changes) [5.00ms]
$ tsc --noEmit

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/auth/prds/auth-answers-a-jev-question-on-the-stored-typesafe-key/specs/spec01.md: exit 0

Command SHA-256: b068a0c3dd99f424820542d8617557602ce5755318e8eece12c6938a404e99b9

```text
passed: auth.jev posts to the fixed path with the stored bearer and returns answers and usage unchanged, a request naming a url or a host or a key is refused and nothing is fetched, a 429 then a 200 succeeds after one backoff, a 529 on every attempt ends in a bounded overloaded failure, a 429 whose retry-after passes the deadline fails rate_limited after one request, a destination that refuses the connection fails unreachable, with no typesafe entry the call fails unavailable and nothing is fetched, a stored value that is not a usable bearer fails unavailable and nothing is fetched, an upstream error body that echoes the key never reaches the caller or the log, a read on a home with no store reports a missing entry and creates nothing, the insert door round-trips a value that status reports as source pass without the value, a WebSocket session relays, forwards and ends over the wire without disclosing the key, failed upstream authorization is useful without echoing the upstream body, shared credentials are discovered without leaking them into status
bun test v1.3.14 (0d9b296a)
{"t":1789829393584,"src":"wire","msg":"auth.jev failed: upstream: TypeSafe refused the request (HTTP 401)."}
{"t":1789829402202,"src":"wire","msg":"auth failed: Supported requests: status {provider, field?} and list"}
{"t":1789829403930,"src":"wire","msg":"auth.live failed: Voice session is not attached"}

 32 pass
 0 fail
 170 expect() calls
Ran 32 tests across 5 files. [11.01s]

```
