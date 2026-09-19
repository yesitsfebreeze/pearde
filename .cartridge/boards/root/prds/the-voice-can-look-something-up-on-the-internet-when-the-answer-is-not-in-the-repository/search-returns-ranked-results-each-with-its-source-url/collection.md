---
commit: "0ba925860f88089792bb03dce1cba756b73d9a7e"
verification-target: "committed"
original-commit: "73540349688b52d82caa7342037ace7a3c07029e"
previous-receipt: "4c065443ec36310195a792da9b64284aa5aecbf80f5ac810c167b6a8f93da651"
spec-digests: {"spec01.md":"b148234c18f775acac901e21df8131ac6a58470a59536827974ea761b749ff4a"}
child-contracts: {}
workspace-verified: true
workspace-drift: []
---

# Collection

Verified committed snapshot 0ba925860f88089792bb03dce1cba756b73d9a7e in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-13QQGb/source.

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url/specs/spec01.md: exit 0

Command SHA-256: 8b37ed5e84de5c706131376f20a4892734f3d672d8bf2e9247acd23ee7f41cda

```text

web.ctg  pass  327 source lines in 4 file(s), largest src/web.ts at 139, 8% comment, 15 tracked

audit: 1 of 1 cartridges pass the hard checks
toolchain: cargo cargo-nextest bun tmux
Isolation passed for 20 cartridges.
isolation composition pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url/specs/spec01.md: exit 0

Command SHA-256: 220cb717ff8ef11b633762ada78a6ab56e9e8e34c5cdf6048ae2c98c9d9d2c3b

```text
web search: ranked results, source URLs, and every credential path behave as specified

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url/specs/spec01.md: exit 0

Command SHA-256: 21457019d95d61e4a68191ddc1ac1d63ee96b4c9578cfa6821aaf8b874f7e726

```text
bun test v1.3.14 (0d9b296a)

web.ctg/.cartridge/tests/integration/fetch.test.ts:
(pass) a page from an allowed host comes back as readable text [12.63ms]
(pass) a host outside the allowlist is refused before any request is made [0.68ms]
(pass) a scheme that is not http or https is refused before any request is made [0.37ms]
(pass) an empty allowlist reaches nothing at all [0.11ms]
(pass) an upstream status is reported, and a long page is cut and says so [3.41ms]
(pass) the tool envelope returns a refusal to the caller instead of throwing it away [3.79ms]

web.ctg/.cartridge/tests/integration/search.test.ts:
(pass) search returns ranked results, each carrying its source URL [6.05ms]
(pass) the result count sent to Brave is clamped to 20, and omitted when no limit is given [2.12ms]
(pass) no key configured is refused before any request is made [1.75ms]
(pass) a variable name outside the WEB_ prefix is refused with a sharper reason [1.71ms]
(pass) a rejected key is reported by name, and never as an empty result pretending success [3.06ms]
(pass) the tool envelope carries a search result and a search refusal the same way it carries fetch's [2.53ms]

 12 pass
 0 fail
 81 expect() calls
Ran 12 tests across 2 files. [60.00ms]

```
