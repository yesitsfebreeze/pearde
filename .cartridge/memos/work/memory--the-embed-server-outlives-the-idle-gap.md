---
kind: work
level: 10
status: done
description: the embedding model unloads after minutes of idle and the next read pays the reload, so the machine's model server is configured once, in the record, not per session
read_when: "setting up a machine, or asking why the first read of the day is slow"
---

# the-embed-server-outlives-the-idle-gap

## Do

`ollama ps` on 2026-09-06 answered `qwen3-embedding:0.6b … UNTIL 9 minutes from
now`: the model unloads on the default keep-alive, and the first read after a
quiet stretch pays a reload before it pays its embed. memory already knows this —
`lib.rs:1354` embeds `memory-keepalive` to hold the model — which is a workaround
for a setting, and one that costs a slot on a one-slot server
([[@prd/work/memory--embeds-go-through-one-lane.md]]) every time it fires.

The Ollama menu-bar app cannot carry the setting: it passes its own fixed
environment to `ollama serve` (`OLLAMA_MODELS`, `OLLAMA_CONTEXT_LENGTH`,
`OLLAMA_NO_CLOUD` and nothing else), so `launchctl setenv` does not reach the
server and the app respawns itself through a login item when stopped. The
settings that do land need the server run as its own agent. On this machine
that is `~/Library/LaunchAgents/com.ollama.serve.plist`, running
`/Applications/Ollama.app/Contents/Resources/ollama serve` with
`OLLAMA_KEEP_ALIVE=24h`, `OLLAMA_MAX_QUEUE=2048`, `OLLAMA_FLASH_ATTENTION=1`,
`OLLAMA_MAX_LOADED_MODELS=3` — verified in the server's own config line — with
the app's login item disabled (`launchctl disable gui/$UID/com.ollama.ollama`).
Reverting is the reverse pair: unload and delete that plist, `launchctl enable`
the login item, open the app.

`OLLAMA_NUM_PARALLEL` is deliberately not in that list: the server reads it and
still launches the embedding model with `-np 1`, which is what
[[@prd/work/memory--embeds-go-through-one-lane.md]] measures and works around.

Write the setup into the record so a second machine is not re-derived from a
hung read, and delete the keepalive embed once the setting holds it.

## Check

`ollama ps` shows the embedding model with a keep-alive over an hour after the
last request, the daemon's first `query` of the day answers in under 3 s
without a preceding warm call, and `grep -rn "memory-keepalive" src/` finds
nothing.

**Check read 2026-09-07 08:06, false on both readable clauses — and the reason
the first one fails is not the one this part assumes.**

The launch agent is in place and running: `~/Library/LaunchAgents/com.ollama.serve.plist`
exists, `launchctl print gui/$UID/com.ollama.serve` reads `state = running`,
`pid = 58249`, and that pid is the `ollama serve` in `ps`. Its environment
carries `OLLAMA_KEEP_ALIVE => 24h` exactly as this part specifies. And
`ollama ps` still answers `qwen3-embedding:0.6b … UNTIL 6 minutes from now`.

The server setting cannot win, because memory overrides it per request:
`llm::EMBED_KEEP_ALIVE` is `"10m"` (`src/llm/src/llm.rs:726`), the default of
`embed.keep_alive` in the config, sent on every embed. A per-request
`keep_alive` beats `OLLAMA_KEEP_ALIVE`, so the model unloads ten minutes after
the last read no matter what the agent's environment says. Deleting the
keepalive embed alone would therefore make the first read of the day slower,
not faster — the config knob has to move with it.

Two other things the reading shows against this part's own text. The agent's
environment carries `OLLAMA_NUM_PARALLEL => 8`, which the `Do` says is
deliberately not in the list; the running `llama-server` is launched
`-np 1` regardless, so the measurement in [[@prd/work/memory--embeds-go-through-one-lane.md]] stands
and the variable is inert rather than harmful. And the workaround the part
exists to delete is still there: `rg -n 'memory-keepalive' src/` finds
`src/commands/src/commands_serve.rs:514`,
`let _ = warm.embed("memory-keepalive").await;`.

The third clause — a first `query` of the day under 3 s with no warm call —
cannot be read while the warm call is in the tree. The part is open correctly
([[the-eight-unread-work-checks]]).

**Check read 2026-09-07 09:50, after the fix: the two readable clauses are
green, and the third is now readable at all.**

The override the last read found is gone: `llm::EMBED_KEEP_ALIVE` is `"24h"`
(`src/llm/src/llm.rs:797`), so `embed_body` (`:382`) sends `keep_alive: "24h"`
on every embed and the config default at `config.rs:554` follows the const. The
body memory now sends, posted once to `/api/embed`, moves `ollama ps` from
`UNTIL About a minute from now` to `UNTIL 24 hours from now` — the per-request
value the server obeys, no longer fighting `OLLAMA_KEEP_ALIVE=24h` but agreeing
with it. `rg -n 'memory-keepalive' src/` finds nothing: `spawn_keepalive` and its
call in `commands_serve.rs` are deleted, and with them the embed that took the
one-slot server every 240 s ([[@prd/work/memory--embeds-go-through-one-lane.md]]).

The third clause — the daemon's first `query` of the day under 3 s with no warm
call — has no warm call left to invalidate it, and the model it needs is now
held resident by the setting rather than by the ping. It is a next-morning
reading against an installed binary (`cargo install`), not one this session
could take: the fix is what makes it takeable.

Two comments went with the code, both stale: `/v1 ignores keep_alive` on the
const (the reason the const exists is the opposite — the native path honours it,
and a per-request value beats the environment) and the same claim on
`spawn_keepalive`. `src/main.rs:51` still names the keepalive as one of the
three blocking bridges behind the worker floor of 4; that file belongs to a
sibling lane and the count is now two.
