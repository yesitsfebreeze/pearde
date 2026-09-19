---
commit: 0b74bc37e7c075234bd22abfefbfe16d114b01b4
spec-digests: {"spec01.md":"3b5bc8f021a6fbf1ca542ff8de83c1e118bfbdc011a021752621b972596c9115"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-running-system-combines-asp-trace-jev-and-scope-with-live-proof/specs/spec01.md: exit 0

Command SHA-256: ec549d7b559f21ab00cd8bec49511d8909e6e476f9ce1d106f34fe12a87c8221

```text
toolchain: cargo cargo-nextest bun tmux
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/asp-system.test.ts:
{"decision_id":"8f415340-a3ac-4e09-8cea-2d5615aabaa8","verdict":"act","entities":[{"id":"memo:@jev/type/judgement.md","noul":0.96},{"id":"file:justfile","noul":0.8}],"withheld":[{"id":"file:justfile","why":"scheme"}],"passes":[{"latency_ms":314,"usage":{"input_tokens":454,"output_tokens":38}},{"latency_ms":303,"usage":{"input_tokens":458,"output_tokens":33}}],"activity_records":3,"trace_entity":"trace:raw/2026-09-19/1789834302111-22d33b0fc75eb9cd","trace_generation":"62215-1789833880883"}
(pass) the running composition connects ASP, trace, JEV and scope activity [33432.98ms]

 1 pass
 0 fail
 38 expect() calls
Ran 1 test across 1 file. [33.46s]
test      system     pass
toolchain: cargo cargo-nextest bun tmux
$ bun test ./.cartridge/tests/
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/slice.test.ts:
(pass) a search of 200 entities sends at most k of them in the second request and both requests stay under the token budget [12.02ms]
(pass) search cannot restore an explicitly stale or absent entity [1.32ms]
(pass) late ASP and ranking replies never start later requests [236.51ms]
(pass) invalid ranking probabilities never enter the second pass [2.21ms]
(pass) an oversized caller state fails open without an auth request [0.95ms]
(pass) a slice over the token budget drops entities from the tail and names them as withheld [47.02ms]
(pass) a file entity travels without its body by default and with it once file is allowed and the response names what was withheld [1.43ms]
(pass) a stale entity and an absent entity are dropped before the first pass [0.49ms]
(pass) an asp error returns escalate with a reason and asks auth.jev nothing [0.50ms]
(pass) no entity above the threshold returns escalate and skips the second request [0.29ms]
(pass) about on a judgement with no slice returns escalate and asks asp nothing [0.18ms]
(pass) jev.decided sums both usages and carries no entity and no state [0.69ms]
(pass) the shipped slice example is valid [0.42ms]
(pass) disallowed trace attributes cannot leak record content into either pass [0.74ms]

.cartridge/tests/integration/decide.test.ts:
(pass) a confidence above act returns act [0.77ms]
(pass) a confidence between the gates returns caution [0.32ms]
(pass) a confidence below escalate returns escalate [0.26ms]
(pass) the weakest answer decides the verdict and the confidence [0.87ms]
(pass) a noul confidence is p or one minus p whichever is larger [0.31ms]
(pass) an unavailable auth.jev returns escalate with its message as the reason and does not throw [0.25ms]
(pass) an auth.jev that answers after timeout_ms returns escalate with a timeout reason [324.58ms]
(pass) an auth.jev that answers null returns escalate with a reason [1.29ms]
(pass) a confidence outside zero to one returns escalate and never act [0.67ms]
(pass) an auth.jev answer missing a declared question returns escalate with a reason naming it [0.57ms]
(pass) an unknown point returns escalate with a reason and asks auth.jev nothing [0.27ms]
(pass) jev.decided is emitted for every decision and carries no state [0.95ms]
(pass) declare refuses a judgement with a question that has no gate [0.51ms]
(pass) declare refuses a judgement with no fallback [0.20ms]
(pass) a wrapped auth failure reads as one line that starts with its type word [0.49ms]
(pass) a judgement whose criteria the api would refuse is refused [0.19ms]
(pass) the documented criteria shapes are accepted [0.07ms]
(pass) the shipped example judgement is valid [1.12ms]

 32 pass
 0 fail
 190 expect() calls
Ran 32 tests across 2 files. [673.00ms]
test      jev        pass
toolchain: cargo cargo-nextest bun tmux
$ tsc --noEmit
Isolation passed for 21 cartridges.
check     jev        pass
isolation composition pass

```
