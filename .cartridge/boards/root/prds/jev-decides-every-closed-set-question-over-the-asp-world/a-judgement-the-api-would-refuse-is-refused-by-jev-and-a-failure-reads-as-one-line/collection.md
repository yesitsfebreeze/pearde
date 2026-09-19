---
commit: bd7b7e0f11c18d350faee6f9fac8f1cd7197efbb
spec-digests: {"spec01.md":"bdc3910a118848024f7fffff9ca68d135472abf7e7d6cab3f189cbebfb8fd43c"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/a-judgement-the-api-would-refuse-is-refused-by-jev-and-a-failure-reads-as-one-line/specs/spec01.md: exit 0

Command SHA-256: e3288a45d6a1e7fa77d70ffba563a2c2abb905050be00ce1fdc927d16db90755

```text
bun install v1.3.14 (0d9b296a)

Checked 5 installs across 6 packages (no changes) [4.00ms]
$ tsc --noEmit

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/a-judgement-the-api-would-refuse-is-refused-by-jev-and-a-failure-reads-as-one-line/specs/spec01.md: exit 0

Command SHA-256: dcea1dfaca3d68fb2cee96760847fafaf1d941b54bebabcb59a8657dd40e5b93

```text
passed: a judgement whose criteria the api would refuse is refused, the documented criteria shapes are accepted, a wrapped auth failure reads as one line that starts with its type word, the shipped example judgement is valid, the weakest answer decides the verdict and the confidence
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/decide.test.ts:
(pass) a confidence above act returns act [3.73ms]
(pass) a confidence between the gates returns caution [0.27ms]
(pass) a confidence below escalate returns escalate [0.21ms]
(pass) the weakest answer decides the verdict and the confidence [0.57ms]
(pass) a noul confidence is p or one minus p whichever is larger [0.30ms]
(pass) an unavailable auth.jev returns escalate with its message as the reason and does not throw [0.43ms]
(pass) an auth.jev that answers after timeout_ms returns escalate with a timeout reason [322.92ms]
(pass) an auth.jev that answers null returns escalate with a reason [0.59ms]
(pass) a confidence outside zero to one returns escalate and never act [0.38ms]
(pass) an auth.jev answer missing a declared question returns escalate with a reason naming it [0.57ms]
(pass) an unknown point returns escalate with a reason and asks auth.jev nothing [0.23ms]
(pass) jev.decided is emitted for every decision and carries no state [0.98ms]
(pass) declare refuses a judgement with a question that has no gate [1.16ms]
(pass) declare refuses a judgement with no fallback [1.07ms]
(pass) a wrapped auth failure reads as one line that starts with its type word [1.11ms]
(pass) a judgement whose criteria the api would refuse is refused [0.24ms]
(pass) the documented criteria shapes are accepted [0.10ms]
(pass) the shipped example judgement is valid [0.37ms]

 18 pass
 0 fail
 86 expect() calls
Ran 18 tests across 1 file. [352.00ms]

```
