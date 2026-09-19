---
commit: 78b7fe480b0f7f7a1cd6f430aaec1cc1bee48ed2
spec-digests: {"spec01.md":"17d3efe5e641cda4727f46a4f6a40a0b2fbc9e97c40a680feac6c3a8daa562f4"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open/specs/spec01.md: exit 0

Command SHA-256: 8e92d4944e92fe05c600c5a2739886c78c791d9429623a7d9f3b0586eb2e7653

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open/specs/spec01.md: exit 0

Command SHA-256: 60c9529928368a10b1a9532c751da5fd25057879c8a20566d6a44d9c34a37845

```text
passed: a confidence above act returns act, a confidence between the gates returns caution, a confidence below escalate returns escalate, the weakest answer decides the verdict and the confidence, a noul confidence is p or one minus p whichever is larger, an unavailable auth.jev returns escalate with its message as the reason and does not throw, an auth.jev that answers after timeout_ms returns escalate with a timeout reason, an auth.jev that answers null returns escalate with a reason, an auth.jev answer missing a declared question returns escalate with a reason naming it, an unknown point returns escalate with a reason and asks auth.jev nothing, jev.decided is emitted for every decision and carries no state, declare refuses a judgement with a question that has no gate, declare refuses a judgement with no fallback, the shipped example judgement is valid
bun test v1.3.14 (0d9b296a)

 15 pass
 0 fail
 65 expect() calls
Ran 15 tests across 1 file. [352.00ms]

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open/specs/spec01.md: exit 0

Command SHA-256: ed6ef4963122535e5f817e5455c77274871b27361b2dde7df90c5e7921d44c4f

```text
bun install v1.3.14 (0d9b296a)

+ @types/bun@1.3.10
+ typescript@5.9.3

5 packages installed [10.00ms]
$ tsc --noEmit

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open/specs/spec01.md: exit 0

Command SHA-256: bdcad60fdb640bebe0ac9a848c83525cb317a7b40d610751df0366ace1b70c70

```text
bun test v1.3.14 (0d9b296a)

 1 pass
 14 filtered out
 0 fail
 4 expect() calls
Ran 1 test across 1 file. [37.00ms]
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/decide.test.ts:
90 | 		{ weak: QUESTION, strong: QUESTION },
91 | 	]) {
92 | 		const h = harness({ judgement: judgement(questions, gates), auth: () => ({ answers, usage: null }) });
93 | 		await h.call("apply", { timeout_ms: 1000 });
94 | 		const out = await decide(h);
95 | 		expect(out.verdict).toBe("caution");
                           ^
error: expect(received).toBe(expected)

Expected: "caution"
Received: "act"

      at <anonymous> (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/jevmut.tEcLbZ/jev/.cartridge/tests/integration/decide.test.ts:95:23)
(fail) the weakest answer decides the verdict and the confidence [6.16ms]

 0 pass
 14 filtered out
 1 fail
 1 expect() calls
Ran 1 test across 1 file. [30.00ms]

```
