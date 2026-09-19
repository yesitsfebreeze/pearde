---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge"
---

# The program is ackin and a cartridge is a kin

## Outcome

The program is called `ackin`, read as "acknowledged kin" and a play on "akin":
it composes related units into one relational tree and acknowledges every
connection between them. Each unit that was a cartridge is now a kin. Every
live name follows: the binary, the crates, the manifests, the project folder,
the submodule suffix, the GitHub repositories, the environment variables, the
socket, the docs, the help pages and the live memos. A fresh checkout builds,
launches and passes its gates under the new names only.

## Acceptance

- [ ] The host binary and its crate are named `ackin`; `ackin help`, `ackin run`,
      `ackin mcp`, `ackin daemon` and `ackin stop` behave as the `cartridge`
      subcommands did, and no `cartridge` binary is installed or invoked by
      any recipe, hook or `.mcp.json` entry.
- [ ] Every project folder `.cartridge/` is `.ackin/`, in the superproject and in
      every submodule, and the host, memo, prd and docs tools resolve records
      only from `.ackin/`.
- [ ] Every manifest `cartridge.json` is `kin.json`, and the host loads,
      trusts and reports kins by that file alone.
- [ ] Every submodule directory `<id>.ctg` is `<id>.kin`, and the host's own
      repository `cartridge.ctg` is `ackin`; `.gitmodules` points at the renamed
      GitHub repositories under `yesitsfebreeze/`.
- [ ] Every environment variable `CARTRIDGE_*` is `ACKIN_*`, and the socket base
      is `/tmp/ackin-<uid>` (or the same name under `XDG_RUNTIME_DIR`).
- [ ] Code, docs, help pages, READMEs, `CLAUDE.md`, `AGENTS.md`, open PRDs and
      live memos say "kin" where they said "cartridge" and "ackin" where they
      named the program. Done PRDs, receipts and evidence notes keep their
      original wording as historical record.
- [ ] Board `repo:` paths in every `settings.md` and open `prd.md` point at the
      renamed directories.
- [ ] After a rebuild, re-trust of each kin and a daemon restart, every kin
      reports active, and `just audit`, `just isolation` and each owner gate
      pass.

## Constraints

- This PRD declares no footprint on purpose: it reserves the whole repository
  and must dispatch only once no other claim is live, because it moves the
  boards, manifests and socket that running sessions depend on.
- Renaming the GitHub repositories is outward-facing; the implementer confirms
  with the user immediately before running it.
- A decision memo records the rename so later readers can map old names in
  history to new ones.
