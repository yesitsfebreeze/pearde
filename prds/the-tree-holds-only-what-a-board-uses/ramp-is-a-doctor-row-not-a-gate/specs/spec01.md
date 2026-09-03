---
complexity: 6
footprint:
  - resources/board/ramp.py
  - resources/board/init.py
---

# spec01 — the gate comes out of the code

`happiness:` is deleted, not defaulted: no reader, no writer, no verb. What is
left of `resources/board/ramp.py` is a measurement — `have`, `need`, `gap`,
`find`, and a bare `pearde ramp` that prints the gap and the candidates for
each unanswered job. `pearde init` stops seeding the key, so a fresh board
carries five knobs, not six.

**Stands** (built in the probe, uncommitted in the lane): `happiness()`,
`write_ask()`, `cmd_happy()` and `cmd_gate()` are gone; `cmd_measure()` replaces
the gate as the bare verb; the `happy` verb is out of the verb set; the unused
`edit as editlib` import is dropped; `DEFAULTS` in `init.py` loses its sixth
pair and its comment. `cmd_gap` returns 0 with a gap standing.

**Left to finish**: nothing but the checks below and the commit.

A gap exiting non-zero is the last place the gate can hide — it turns a
reading into a check, and `doctor` would go red because a field has no
published skill on this machine. Every verb in this module exits 0.

## Acceptance

- [ ] `grep -rl happiness resources/` matches no file.
- [ ] `ramp.py` defines no `happiness`, `write_ask`, `cmd_happy` or `cmd_gate`, and `"happy"` is not in its verb set.
- [ ] `python3 resources/pearde.py init <fresh repo>` writes a `settings.md` with no `happiness:` line; so does `init --example`.
- [ ] `ramp gap` on a board with an unanswered job prints its `GAP <job>` row and exits **0**.
- [ ] Bare `pearde ramp` prints the gap and, per unanswered job, the candidates with their `npx skills add` line, writes no file, and exits 0.
- [ ] No `.pearde/.state/ask.md` exists on a board that has only ever been `init`ed.
- [ ] `resources/invariants/a-master-need-is-the-union-of-its-members.sh` is green — `ask_subject` survives the removal, and a master's credit line with it.

## Verify and Proof

```sh
PEARDE_ROOT=$(pwd) bash .pearde/prds/the-tree-holds-only-what-a-board-uses/ramp-is-a-doctor-row-not-a-gate/probe/verify.sh
bash resources/invariants/a-master-need-is-the-union-of-its-members.sh
python3 -c 'import ast;ast.parse(open("resources/board/ramp.py").read())'
```
