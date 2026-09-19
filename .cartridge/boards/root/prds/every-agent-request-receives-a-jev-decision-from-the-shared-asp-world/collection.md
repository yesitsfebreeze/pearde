---
commit: 0ba925860f88089792bb03dce1cba756b73d9a7e
spec-digests: {"spec01.md":"23f23a9ac5a5eba83bf559ee54ff77aa502683fed081efef94399d97274f91a6"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/every-agent-request-receives-a-jev-decision-from-the-shared-asp-world/specs/spec01.md: exit 0

Command SHA-256: 93510d240b6368e92bd9f4b2c0bcdc141b603f2f1c92b785abb73dd78a808d18

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/jev-request-hook.test.ts:
(pass) a prompt registers distinct external work before JEV sees the question [1.37ms]
(pass) stopping marks only the mapped agent completed and does not ask JEV [0.07ms]
(pass) missing identity cannot collapse unrelated agents into one connection [0.09ms]
(pass) bad input and unavailable services fail open without claiming approval [0.27ms]

 4 pass
 0 fail
 16 expect() calls
Ran 4 tests across 1 file. [30.00ms]
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/jev-workflow.test.ts:
{"native_decision":"903d3081-d48d-434b-a28c-7a972e90f01f","proxy_context_decision":"0b78df52-6e69-4557-b0d8-45ef1c44c363","voice_decision":"996a6b41-1bf4-4f4c-8900-4f5bd292147e","hook_decision":"b4dc903f-9a76-4e6e-93c3-6cb9d4579493","peer":"18d6c744f44c3368-48"}
(pass) connected request paths consult real JEV, see peer work, and retain inspectable decisions [26467.53ms]

 1 pass
 0 fail
 60 expect() calls
Ran 1 test across 1 file. [26.50s]
toolchain: cargo cargo-nextest bun tmux
Isolation passed for 21 cartridges.
isolation composition pass

```
