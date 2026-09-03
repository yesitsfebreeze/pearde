---
state: done
origin: requested
priority: 55
complexity: 12
blast-radius: low
workflow: probe-then-spec
actual: 0.68h
commit: 48540d3 ff74db9
---

# pearde vault without --wait

*Source: `docs/content/docs/improvements/obsidian-wait.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** obsidian · **Axis:** usability (4 → 6) · **Pulls the score up by
~6 points**

## Why now

The register is written only with Obsidian closed — Obsidian rewrites
`obsidian.json` from memory on quit, so an entry written under a running app
is unseen and dies on exit. Today the safe path is
`pearde vault --wait --open`: the command stops, tells you to quit the app,
waits for the process to go, writes, reopens. Without `--wait` it refuses
while the app runs. The dance is documented, which is the problem — a rule
you must *remember* is a rule you hit once a month and lose once a month.

## The change

`pearde vault` with no `--wait` and Obsidian running stops refusing: it
prints the quit instruction, then **waits for the same process exit the
`--wait` path waits for** — one code path, one prompt, no flag to remember.
`--wait` keeps its meaning (headless scripts, no prompt) and the
`--open`-less form keeps writing without reopening.

## Done when

- `pearde vault` with the app running prints one line and completes after
  the app quits — no flag named.
- `pearde vault --wait` in a harness (no TTY, `env -i`) behaves exactly as
  today: waits, writes, exits zero.
- A second `pearde vault` started while the first waits refuses with "the
  writer is already held", the way `claim` refuses a held claim.

## Fails when

- The process-wait races a *manual* quit that never comes: the command hangs
  forever instead of timing out. Guard: the wait carries the same timeout the
  `--wait` path has, and the timeout message names the process it waits on.

## What stays out

No detection of *which* vault Obsidian has open — the register readback
already answers that after the fact, and guessing a write ordering under a
running app is the outage this removes, not the feature it adds.

## Report

spec01: exit 0
probe: measuring /Users/feb/dev/infra/pearde/.pearde/.lanes/pearde-vault-without-wait
vault: seeded /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-6hen15k9/.obsidian — plugins: dataview, obsidian-local-rest-api
vault: waiting for Obsidian to quit — the register is only writable while it is closed. Quit it now (⌘Q)…
vault: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-6hen15k9 registered as vault-probe-6hen15k9 · obsidian://open?vault=a0ca1c4e71acec34
PASS: flagless run with Obsidian running does not raise Refused
PASS: flagless run actually polled (did not just refuse once)
PASS: flagless run wrote the register after the simulated quit
vault: seeded /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-63ra4ke_/.obsidian — plugins: dataview, obsidian-local-rest-api
vault: waiting for Obsidian to quit — the register is only writable while it is closed. Quit it now (⌘Q)…
vault: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-63ra4ke_ registered as vault-probe-63ra4ke_ · obsidian://open?vault=25e4e4be1acb7eea
PASS: `--wait` still waits, writes, exits zero
vault: seeded /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-skp__2k8/.obsidian — plugins: dataview, obsidian-local-rest-api
vault: waiting for Obsidian to quit — the register is only writable while it is closed. Quit it now (⌘Q)…
PASS: a second `pearde vault` while the first waits refuses
vault: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-skp__2k8 registered as vault-probe-skp__2k8 · obsidian://open?vault=34063505fd346f3d
PASS: first run was not itself refused by its own lock
vault: seeded /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/vault-probe-a4v_aue6/.obsidian — plugins: dataview, obsidian-local-rest-api
vault: waiting for Obsidian to quit — the register is only writable while it is closed. Quit it now (⌘Q)…
PASS: a wait that never sees the app quit times out (no hang)
PASS: the timeout message names the process it waited on

all passed
