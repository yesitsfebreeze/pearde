---
commit: 6d1f9569296d9ce7dd310eed23236b035adeaefc
spec-digests: {"spec01.md":"07a8328ed9148101ce9591b7d066aaa5a63c7266e8a3148b405d693e56546342"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/runtime/prds/a-lanes-build-can-hand-back-a-siblings-binary/specs/spec01.md: exit 0

Command SHA-256: d58615d7c11060ae3d7d26c85faf607673ed0a5c35c90d96b694a90ae3085ba0

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/memo-run.test.ts:
(pass) memo recipes preserve argument boundaries and propagate failure [153.68ms]
(pass) memo runner refuses missing, repeated and unterminated executable blocks [22.45ms]
(pass) nested PRD lanes resolve their own memo owner [13.81ms]
lane-build-evidence [{"lane":"alpha","mode":"safe","temperature":"cold","ms":549.267458,"source":{"commit":"91d55db06139c84900d0f496cfe52cb5d7dc4681","tree":"9a08268bb20ac8730ac543ea7d92cc6e8d3bf9f9","digest":"d12a11572ff645ddd6ef8218e56d6a7f0424bb428b02cf77089b7be92751f0f2"},"binary_sha256":"621c63cda4141929dcc27bacc90bf3ef4c9d9819e41b3f3222381c4bdb1e3471","expected":"alpha","observed":"alpha","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"},{"lane":"alpha","mode":"safe","temperature":"warm","ms":356.5570839999999,"source":{"commit":"91d55db06139c84900d0f496cfe52cb5d7dc4681","tree":"9a08268bb20ac8730ac543ea7d92cc6e8d3bf9f9","digest":"d12a11572ff645ddd6ef8218e56d6a7f0424bb428b02cf77089b7be92751f0f2"},"binary_sha256":"621c63cda4141929dcc27bacc90bf3ef4c9d9819e41b3f3222381c4bdb1e3471","expected":"alpha","observed":"alpha","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"},{"lane":"bravo","mode":"safe","temperature":"cold","ms":659.056875,"source":{"commit":"72cd052c5ce6ba7310a2080541610640f23df75f","tree":"f6ae5de5148108d3fb163edb0b16f3b83e9b7e84","digest":"101fc091b5b3c98b8c6c6948f7c20f06809f26890f2ff7a0bd65d1caca571ba9"},"binary_sha256":"febb286887708a068c11f7fead75a49e73f7d2ee84646d9029e7e0109abf4166","expected":"bravo","observed":"bravo","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"},{"lane":"bravo","mode":"safe","temperature":"warm","ms":390.1384580000001,"source":{"commit":"72cd052c5ce6ba7310a2080541610640f23df75f","tree":"f6ae5de5148108d3fb163edb0b16f3b83e9b7e84","digest":"101fc091b5b3c98b8c6c6948f7c20f06809f26890f2ff7a0bd65d1caca571ba9"},"binary_sha256":"febb286887708a068c11f7fead75a49e73f7d2ee84646d9029e7e0109abf4166","expected":"bravo","observed":"bravo","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"}]
(pass) divergent lanes execute their own cold and warm builds without inherited caches [2121.17ms]

 4 pass
 0 fail
 47 expect() calls
Ran 4 tests across 1 file. [2.32s]

```
