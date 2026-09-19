---
complexity: small
footprint:
  - cartridge.json
---

# spec01 — `tools.selftest` declares the empty payload it takes, so the host turns back anything else

Base: `tools.ctg` at `024f5dd37e7cff0f940a4e5e1858c362c8959867`
(`Treat a host's own run logs in a lane as build artefacts`).

## What the code says

The PRD's evidence is a day older than the tree. Commit `8d0dbe6` (`Ship a
README, and declare the schema of the event that had none`) already added
`"schema": {}` at `cartridge.json:49`, and `just audit tools` passes today: the
audit's rule is `if (!event.schema)` in
`.cartridge/memos/routine/audit-cartridges.md`, and `{}` is truthy there. So
acceptance (c) is already met, and by the weakest possible means — an empty
schema is a JSON Schema that accepts every payload, so nothing is ever refused
against the declaration. Acceptance (a) and (b) are the open work, and both are
one edit to this one file.

What the handler accepts:

- `init.lua:3` binds the event with `function() return tools.selftest() end` —
  the request value is dropped on the floor, never passed on.
- `src/lib.rs:15`, `fn selftest(lua: &Lua, _: LuaValue)` — the payload argument
  is bound to `_`.
- `src/service.rs:335`, `pub fn selftest() -> Result<serde_json::Value>` — takes
  no argument at all; it reads `current_dir` and the manifests under it.

So the event takes no payload. It has no optional fields because it has no
fields.

What the host does with a declared schema (all in `cartridge.ctg`, outside this
footprint, already working — no host change is needed):

- `src/transport/cartridge.rs:239-278`, `Ctx::validate` compiles the declared
  schema and answers ``` `<name>` payload rejected by its schema: … ```.
- `src/host/mod.rs:811` calls it on the **sender** side, before any listener is
  chosen; `src/transport/cartridge.rs:973` calls it again on the receiving node
  before the Lua listener runs. Either way the refusal is against the
  declaration, never inside the handler.
- `src/loader/document.rs:184-186` refuses a `schema` that is not a JSON Schema,
  so a malformed declaration fails at load rather than at call time.

The one constraint the code forces: `src/host/run.rs:173` sends every key in
`contracts` with `serde_json::Value::Null`, and `tools.selftest` is in
`contracts` (`cartridge.json:7`). A schema that refuses `null` would break
`cartridge verify tools`. `cartridge call`/`run`/`send` default their payload to
`null` as well (`src/cli/args.rs:79`). `null` is therefore not negotiable.

Accepting `{}` alongside it is **this spec's decision, not the code's**. Nothing
in this composition sends `{}` to this event — nothing sends it anything but
null — so a null-only declaration would break no caller today. The reason to
take `{}` anyway is that it is the same statement as `null`: a payload carrying
no field, from an event that reads no field. A person at a terminal and a
generated client both reach for `{}` when an event takes nothing, the sibling
`doctor` convention in this same host spells "no payload" that way
(`cartridge.ctg/docs/creating-cartridges.txt:181`), and refusing it would make
the declaration pickier than the thing it describes without protecting anything.
Everything that carries data is turned back. A coordinator who prefers the
narrower reading can drop `{}` from the accepted set in step 1 and move the two
`'{}'` entries in the Verify block from the accepting loop to the refusing one;
nothing else in this spec changes.

Observed on the live host, 2026-09-19:

```
$ cartridge call tools '{"op":"nope"}'
invalid argument: `tools` payload rejected by its schema: {"op":"nope"} is not
valid under any of the schemas listed in the 'anyOf' keyword at
$ cartridge call tools.selftest '{"bogus":1}'
tools: runtime error: … cargo metadata … could not find `Cargo.toml` …
```

The sibling event in the same manifest refuses a bad payload against its
declaration; `tools.selftest` carries the caller straight into the handler and
fails there. That contrast is the whole PRD.

## Steps

1. In `cartridge.json`, replace the empty `schema` of the `tools.selftest` event
   (`cartridge.json:47-50`) with a JSON Schema that accepts the two empty
   payloads — `null`, which `run_contracts` forces
   (`cartridge.ctg/src/host/run.rs:173`), and `{}`, which this spec admits for
   the reason given above — and accepts nothing else: no object with a property,
   no string, no array, no number, no boolean. An `anyOf` of the null type and
   an object type that admits no additional properties says exactly that, and
   is the same dialect the
   `tools` event beside it already uses (`cartridge.json:12-38`), which is what
   `jsonschema::validator_for` compiles.
2. Rewrite the event's `description` (`cartridge.json:48`) so it says the event
   takes no payload. Today it reads "Proves every cartridge manifest under the
   composition reads as the bundler reads it" — true about what the event does,
   silent about what to send it, which is the half of the surface this PRD is
   about. A reader of the manifest alone should learn both. Nothing else in the
   file changes.

Step 2 is read in the diff, not gated: a check that the description contains
particular words would be a text gate naming its own cure.

Nothing outside `cartridge.json` changes. `README.md` and `.cartridge/help.md`
already describe `tools.selftest` as "the check the runtime runs against it" and
name no payload, so the standing memo that a behaviour or surface change updates
both is satisfied by leaving them as they are.

## Acceptance

- [x] `tools.ctg/cartridge.json` declares a schema for `tools.selftest` that
      matches what the handler really accepts: no payload, and therefore no
      fields, optional or otherwise.
- [x] A call carrying anything — an object with a property, a string, an array,
      a number, a boolean — is refused against the declaration and never reaches
      the listener, while the empty payloads still reach it: `null`, which
      `cartridge verify` and a bare `cartridge call` send, and `{}`, which this
      spec chooses to keep accepting.
- [x] `just audit` reports no schema finding for `tools.selftest`. A schema that
      turns back `{"unread":1}` is necessarily present and non-empty, so the
      audit's `!event.schema` rule cannot fire on it; the Verify block below
      fails if the declaration ever stops refusing.

## Verify and Proof

<!--
The block stands up a throwaway project holding a copy of the manifest under
test and a three-line Lua entry that only answers, so the real host validates
the real declaration with no dylib to build and no cargo at all. `cd` goes to
that scratch project and never to a checkout: the manifest path is captured
from $PWD first, so pass 1 reads the lane's file and pass 2 the live one.
Running from the lane without that `cd` would find the superproject and test
the live manifest instead — the host locates its project from the cwd.

`mktemp -d` rather than a name under `$TMPDIR`: the block gets no injected
environment, so `$TMPDIR` may be unset (mktemp falls back to /tmp on its own),
and a fixed name collides when two sessions on this machine run a pass at the
same time.

The trap stops the probe host **from inside `$probe`, in a subshell**, and that
is not a flourish. `cartridge` resolves its project from the cwd
(`cartridge.ctg/src/cli/mod.rs:90` and `:142`), and from either the lane or
`tools.ctg` that resolution walks up into the superproject: measured on
2026-09-19, `cartridge socket` prints the same `/tmp/cartridge-501/…/host.sock`
in `tools.ctg` as it does at the composition root. A bare `cartridge stop` in
the trap would therefore stop the shared daemon every other session is using,
whenever `set -e` aborts the block in the window between arming the trap and
`cd "$probe"`. The subshell pins the stop to the throwaway project, and because
`cd "$probe"` fails when the directory was never created, an abort before that
point sends no stop at all. Round 2 of review found this; the block had the bug.

An `exit 1` inside either loop leaves by the same path as success, so no run
leaves a scratch project or a probe host behind. It does leave two run
directories under `/tmp/cartridge-<uid>` per run, which is the host's own
bookkeeping for a project that no longer exists; `cartridge sweep` owns those
and removes them, and the block does not call it because sweeping is
machine-wide and not this block's to do.

The refusing set covers one representative of every JSON type a caller could
send: an object with a property, a string, an array, a number and a boolean.
Round 1 of review defeated a set that stopped at the first three — a schema
admitting `42` and `true` passed it — so every type the handler would ignore is
named here.

The ceiling of that census, recorded rather than closed: a schema can pass this
block and still admit a *value* inside a type it does not refuse wholesale —
round 2 built an `anyOf` of the null type and an object type that declares one
boolean property and forbids the rest, which exits 0 while letting
`{"verbose":true}` reach the listener. No
enumeration of payloads closes that, because the shape that would is a text gate
on the manifest, and a gate that names the tokens to delete is a paste-in bypass.
The diff reading is the backstop: the reviewer checks that the declared schema
names no property, since step 1 says the event has none.

Measured on 2026-09-19 against the daemon replaced at 13:02Z (`cartridge.ctg`
at `324f36e`), run as `env -u CARTRIDGE_YOLO sh -eu -c …`: against the tree at
base the block exits 1 on the `{"unread":1}` payload; against the same tree
carrying the schema of step 1 it exits 0; against a schema that also admits a
number and a boolean it exits 1. Whole run under two seconds.
-->

```sh
manifest="$PWD/cartridge.json"
probe=$(mktemp -d)
trap '(cd "$probe" && "${CARTRIDGE_BIN:-cartridge}" stop) >/dev/null 2>&1 || true; rm -rf "$probe"' EXIT INT TERM
mkdir -p "$probe/.cartridge" "$probe/tools.ctg"
cp "$manifest" "$probe/tools.ctg/cartridge.json"
cat > "$probe/tools.ctg/init.lua" <<'LUA'
local function reached() return "the listener ran" end
cartridge.listen("tools", reached)
cartridge.listen("tools.selftest", reached)
LUA
printf 'return {\n\t{ id = "tools", path = "tools.ctg" },\n}\n' > "$probe/.cartridge/init.lua"

cartridge="${CARTRIDGE_BIN:-cartridge}"
cd "$probe"
ask() { "$cartridge" --yolo run tools.selftest "$1" 2>&1 || true; }

for empty in 'null' '{}'; do
	answer=$(ask "$empty")
	case "$answer" in
	*"the listener ran"*) ;;
	*)
		printf 'the declaration turns back %s, an empty payload the event has to keep taking: %s\n' "$empty" "$answer" >&2
		exit 1
		;;
	esac
done

for carried in '{"unread":1}' '"a string"' '[1]' '42' 'true'; do
	answer=$(ask "$carried")
	case "$answer" in
	*"the listener ran"*)
		printf 'the declaration let %s reach the listener; the handler reads no payload at all, so the manifest, not the handler, is where every payload that carries something has to stop\n' "$carried" >&2
		exit 1
		;;
	*) ;;
	esac
done

echo 'tools.selftest: the declaration accepts an empty payload and turns back one that carries anything'
```
