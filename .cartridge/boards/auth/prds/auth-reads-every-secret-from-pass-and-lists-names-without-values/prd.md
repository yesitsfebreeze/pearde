---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/auth.ctg"
work-kind: leaf
footprint:
  - 'src/**'
  - 'cartridge.json'
  - 'README.md'
  - '.cartridge/help.md'
  - '.cartridge/docs/README.md'
  - '.cartridge/tests/**'
commit: "c5e88719f0e5417abf6bc02aa35a4cc3d16a791c"
---

# auth reads every secret from pass and lists names without values

## Outcome

auth keeps every secret in a `pass` store it owns, under
`cartridge/<provider>/<field>`, encrypted with a gpg key it creates itself.
Nobody sets up gpg or pass by hand; a person only supplies a secret's value
once. Any agent or cartridge can ask auth which secrets exist and gets
names, providers and availability, never a value.

## Direction (2026-09-19, user)

"auth should be responsible of every key, we can use something like `pass`
to manage them so we can decode them and put them somewhere but its safe for
us to read pass keys and links." Then, after four manual gpg and pass steps
were proposed: "For point one can't we use the pass system for the harness
so we don't have to set anything up manually? The harness or the agent itself
(like the cartridge we create) can hold its own settings and its own pass
integration rather than tying it to the user". Recorded as the note memo
`user-correction-auth-owns-its-pass-store`.

## Decision (2026-09-19, coordinator)

- State lives in `~/.cartridge/auth`, mode 0700, outside any checkout:
  `store/` in the pass layout and a gpg home gpg creates itself.
- A value enters only through `bun src/insert.ts <provider> [field]`, run by
  a person outside the daemon. It reads stdin and creates the key and store on
  first use. No event carries a value, in or out: auth either makes the
  authenticated call itself or writes a derived file for a consumer that
  must hold the key (@auth/auth-writes-the-router-s-credential-file-from-pass).
- The node's grant gains `exec: ["gpg"]` and write on the gpg home only.
- A passphrase-less key beside its ciphertext protects no better than a
  mode-0600 file, and other cartridges with `read: ["/"]` can read it. The
  person's own store is not an option; nobody asked for it.

The rationale, probes and superseded first design are in `specs/spec01.md`
and `review.md`.

## Acceptance

- [x] A named test decrypts an entry in a temporary gpg home reached
      through `HOME`, and the value reaches only auth's own authenticated
      call.
- [x] `auth {op:"status", provider}` answers for any provider with
      `source: "pass"` and the entry name, never the value.
- [x] `auth {op:"list"}` returns every valid `cartridge/**` entry as
      `{name, provider, field, available}`; a named test asserts no response
      or envelope contains a fixture value.
- [x] First use creates the store and gpg home with mode 0700; a missing
      entry and each gpg failure (not installed, no answer in time, refused)
      are distinct bounded diagnostics.
- [x] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md`
      describe the layout, the insert door and the two delivery rules.
