---
complexity: 4
footprint:
  - resources/doctor.sh
---

# spec03 — doctor's vault row reads `off` when no vault was asked for

The vault row's first arm reported a board named `.pearde/` as `broken` —
Obsidian skips a dot-segment, so nothing of the board shows in the project's
vault. That arm fired before the arm that answers "there is no vault at all",
so on every board `init` writes, doctor reported a viewer nobody asked for as
a fault. With the vault opt-in that is now the normal case, and a viewer
nobody asked for cannot be broken. The `no .obsidian/` arm moves first and
says why it is `off`; the dot-segment arm keeps its text and sits under it,
where it only speaks about a vault that actually exists.

**What stands** (built in this lane, uncommitted): the two arms are swapped,
the `off` line reads `the vault is an optional viewer (Obsidian + Dataview)
and none was asked for`, and the block comment above the row says the `off`
arm is first and why.

**What is left**: nothing in this file. **Read this before starting**: the
dot-segment arm's own `fix` — `pearde upgrade`, which would move the board
back to the undotted layout the invariant
`the-board-directory-is-pearde-and-the-compat-symlink-is-gone` forbids — is
wrong and is **not** this spec's to correct. It is spec03 of
`the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.
Leave that arm's text exactly as it is; only its position changes here.

## Acceptance

- [x] On a board whose project has no `.obsidian/`, `pearde doctor` prints `vault  off` and never `vault  broken`, whatever the board directory is called.
- [x] The `off` line says the vault is an optional viewer needing Obsidian and Dataview.
- [x] On a project that HAS `.obsidian/` and a board named .pearde, the dot-segment `broken` row still prints, with its wording unchanged.
- [x] `bash -n resources/doctor.sh` is clean and doctor still prints the same rows in the same order.

## Verify and Proof

```sh
bash -n /Users/feb/dev/infra/pearde/resources/doctor.sh
cd "$(mktemp -d)" && git init -q .
python3 /Users/feb/dev/infra/pearde/resources/pearde.py init "$PWD" >/dev/null
out=$(python3 /Users/feb/dev/infra/pearde/resources/pearde.py doctor "$PWD" 2>&1 || true)
printf '%s\n' "$out" | grep '^  vault' | grep -q ' off '
echo "PASS off"
mkdir -p "$PWD/.obsidian"
out=$(python3 /Users/feb/dev/infra/pearde/resources/pearde.py doctor "$PWD" 2>&1 || true)
printf '%s\n' "$out" | grep '^  vault' | grep -q ' broken '
echo "PASS dot-segment still speaks"
```
