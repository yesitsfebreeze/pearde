---
commit: 215007548e4d26907ba51893b8084aa63d662c90
spec-digests: {"spec01.md":"4604d9b99bb88f42529e434555219475bbfb1c39a4717840d13f185a184567ce"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/jev-pulls-asp-slices-narrows-them-in-two-passes-and-sends-only-allowed-schemes/specs/spec01.md: exit 0

Command SHA-256: d04ba3af97303fb7caef50b807b7db48fcd742b17b7eb418c7b39862287e8980

```text
bun install v1.3.14 (0d9b296a)

Checked 5 installs across 6 packages (no changes) [9.00ms]
$ tsc --noEmit
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/slice.test.ts:
(pass) a search of 200 entities sends at most k of them in the second request and both requests stay under the token budget [10.85ms]
(pass) search cannot restore an explicitly stale or absent entity [1.03ms]
(pass) late ASP and ranking replies never start later requests [235.93ms]
(pass) invalid ranking probabilities never enter the second pass [1.41ms]
(pass) an oversized caller state fails open without an auth request [0.70ms]
(pass) a slice over the token budget drops entities from the tail and names them as withheld [29.93ms]
(pass) a file entity travels without its body by default and with it once file is allowed and the response names what was withheld [0.94ms]
(pass) a stale entity and an absent entity are dropped before the first pass [0.35ms]
(pass) an asp error returns escalate with a reason and asks auth.jev nothing [0.36ms]
(pass) no entity above the threshold returns escalate and skips the second request [0.21ms]
(pass) about on a judgement with no slice returns escalate and asks asp nothing [0.10ms]
(pass) jev.decided sums both usages and carries no entity and no state [0.47ms]
(pass) the shipped slice example is valid [2.40ms]
(pass) disallowed trace attributes cannot leak record content into either pass [0.45ms]

.cartridge/tests/integration/decide.test.ts:
(pass) a confidence above act returns act [0.25ms]
(pass) a confidence between the gates returns caution [0.11ms]
(pass) a confidence below escalate returns escalate [0.09ms]
(pass) the weakest answer decides the verdict and the confidence [0.20ms]
(pass) a noul confidence is p or one minus p whichever is larger [0.10ms]
(pass) an unavailable auth.jev returns escalate with its message as the reason and does not throw [0.11ms]
(pass) an auth.jev that answers after timeout_ms returns escalate with a timeout reason [322.28ms]
(pass) an auth.jev that answers null returns escalate with a reason [0.55ms]
(pass) a confidence outside zero to one returns escalate and never act [0.27ms]
(pass) an auth.jev answer missing a declared question returns escalate with a reason naming it [0.27ms]
(pass) an unknown point returns escalate with a reason and asks auth.jev nothing [0.17ms]
(pass) jev.decided is emitted for every decision and carries no state [0.47ms]
(pass) declare refuses a judgement with a question that has no gate [0.24ms]
(pass) declare refuses a judgement with no fallback [0.08ms]
(pass) a wrapped auth failure reads as one line that starts with its type word [0.20ms]
(pass) a judgement whose criteria the api would refuse is refused [0.10ms]
(pass) the documented criteria shapes are accepted [0.04ms]
(pass) the shipped example judgement is valid [2.37ms]

 32 pass
 0 fail
 190 expect() calls
Ran 32 tests across 2 files. [636.00ms]

```
