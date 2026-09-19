---
state: open
origin: derived
priority: 65
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
  - "src/cli/host.rs"
  - "src/host/socket.rs"
  - ".cartridge/tests"
---

# cartridge stop resolves its socket from the working directory, not from --dir

## Outcome

`cartridge --dir <profile> stop` stops the host that `<profile>` names, from
any working directory. Stopping a foreign profile from inside another project
never touches that project's daemon.

## Acceptance

- [ ] With a daemon running for profile A and another for profile B, running
      `cartridge --dir <B> stop` with the working directory inside A leaves A
      running and stops B.
- [ ] The socket path the command resolves is derived from `--dir` when `--dir`
      is given, and from the working directory only when it is not. One named
      test proves both branches.
- [ ] `--dir` behaves the same way for every subcommand that reaches a running
      host, not only `stop`; the test names each one it covers.

## Evidence

Observed on 2026-09-19 by the verifier of
`@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`,
recorded in
`prd.ctg/.cartridge/boards/root/.state/loop/composed-acceptance/verifier-1.md`.

The verifier found nine orphaned `mcp-cancel` daemons left by the live host
suite, eight of them older than its own session. Following the project rule that
a host is never killed by process name, it ran `cartridge --dir <profile> stop`
for one of them from a shell whose working directory was
`/Users/feb/dev/cartridge`. The command resolved its socket from the working
directory rather than from `--dir` and stopped the project daemon. That daemon
restarted and came back healthy with eighteen cartridges active, so nothing was
lost, but every other session on this machine was running gates against it.

This matters more than a single mis-stopped daemon. `--dir` is the documented
alternative to killing by process name, so an agent that follows the rule
correctly can take down the shared host, and the failure is silent: the command
reports success, because it did stop *a* daemon.

The orphaned daemons themselves are a separate matter and belong to whatever
leaves them behind in the host suite; this PRD is only about `--dir` being
ignored.
