---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `just kill` is `pkill -f memory`, which on this machine matches 14 processes — nine memory ones, `kernelmanagerd`, three Claude sessions and two tmux servers, all because their command line contains the repo path

## Do

`justfile:81-82`:

```
[unix]
kill:
    -pkill -f memory
```

`-f` matches the whole command line, and "memory" is a substring of both a system
binary and this repository's path. Measured 2026-09-06 09:32, the pattern
matches:

```
9   memory processes                     the intended targets
1   /usr/libexec/kernelmanagerd        a macOS system daemon
3   Claude sessions                    …/projects/-Users-feb-dev-memory…
2   tmux servers                       tmux new-session -c /Users/feb/dev/memory
```

`KernelEventAgent` escapes only because `pkill` is case-sensitive. Anyone
running `just kill` in this checkout kills their own editor session and a
system daemon along with the daemons they meant.

The information needed to do it properly is inside memory and not in the shell: a
daemon's socket is FNV-1a of the canonicalised root
([[socket-tag-is-canonicalized]]), the hub knows every node it adopted, and
`memory hub status` already lists them. Either narrow the pattern to the binary
path (`pkill -f "$(pwd)/target/.*/memory "` and the installed path) or give memory
the verb, which is the only version that knows which processes are actually
serving this root.

The sibling recipe has the same shape from the other side. `clean`
(`justfile:61-64`) hardcodes `.memory/bin .memory/intake .memory/data .memory/capture
.memory/*.log`, but memory computes those paths — `Config::default_in`,
`log_dir()`, `intake.dir` — and `MEMORY_DIR` relocates all of them
([[memory-dir-repoints-two-things]]). It names `.memory/capture`, residue of a
deleted surface ([[memory-dir-holds-two-dead-surfaces]]), and misses the socket,
which lives in `/tmp` or `$XDG_RUNTIME_DIR`
([[socket-lives-in-runtime-dir]]). A wipe that guesses at the paths is a wipe
that is wrong under any non-default config.

## Acceptance
`just kill` terminates only processes whose executable is a memory binary, and
`pgrep -af` shows no non-memory survivors of interest before and after. `just
check` green.

Done 2026-09-06: `justfile` kill is `pkill -x memory`. `pgrep -x memory` selected 8
processes, every one a memory binary, where `-f memory` selected 28 — the 20
extra were `kernelmanagerd`, `sccache`, `rustc`, `zsh`, `tmux` and two test
binaries. The kill itself was not fired: peers' daemons were live on the
machine, and the selector is what the Check is about.

Both recipes are gone as of 2026-09-06, replaced by the verb this Do named as
the only version that knows what is serving this root: `kill` by
[[stop-is-a-verb]], and the sibling shape by [[clean-is-a-verb]].
