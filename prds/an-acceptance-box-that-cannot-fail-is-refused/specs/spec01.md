---
complexity: 14
footprint:
  - resources/board/specs.py
---

# spec01 — the walker refuses a verify block that cannot fail

`check_spec` in `resources/board/specs.py` now refuses a spec whose
`## Verify and Proof` block cannot exit non-zero under the exact runner
`collect` uses (`bash -e -o pipefail`, cwd the code repo, last command's
exit read). `_cannot_fail_why(script)` already stands, in the tree,
uncommitted, in the section `# ── can a verify block fail? ─`: it models
and-or lists, `||` fallbacks, `!` inversions exempt from `set -e`,
`exit`/`exec`, always-0 builtins, bare assignments, `pipefail` across every
pipeline member, heredocs, function bodies, comments, continuations, and
quote/`$( )` nesting — and the refusal call inside `check_spec`'s verify
branch appends `verify block <N> cannot fail — <why>` to the same refusals
list every other `specced` gate rides, exit 1, nothing written. This spec
records that the mechanism is complete and pins it against the fixtures and
the differential the probe already ran; nothing further is to be built.

## Acceptance

- [x] a spec whose only `sh` block is guarded to always exit 0 (e.g. ends on
  a bare `true`, or every statement is behind `|| true`) is refused by
  `check_spec`, with a message naming the block number and containing
  `cannot fail`
- [x] the four mechanical shapes the probe's case suite and the collect
  runner surfaced — a trailing always-0 command, a `!` inversion, a `||`
  fallback resetting status, a bare `true`/`:` — are all refused
- [x] a live block (one whose last statement can exit non-zero under
  `bash -e -o pipefail`, e.g. `python3 -c 'import sys; sys.exit(1)'; echo
  done`) is accepted — `check_spec` returns no `cannot fail` message for it
- [x] the differential against real `bash -e -o pipefail` records zero false
  refusals — no script the analyzer refuses is one bash actually exits 0 on
- [x] an unanalysable shape (a loop, a conditional body, a `set +e` block)
  is accepted rather than refused — the walker only refuses what it can
  prove, never guesses

## Verify and Proof

```sh
bash .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/verify.sh
python3 - resources/board/specs.py <<'PYEND'
import importlib.util, sys
s = importlib.util.spec_from_file_location("specs", sys.argv[1])
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
REFUSE = [("everything guarded, a closing always-0 command",
           "python3 check.py || true\necho done\n"),
          ("a `!` inversion", "! test -f x\necho ok\n"),
          ("a `||` fallback resetting status",
           "x=$(false) || echo no\necho ok\n"),
          ("a body in a condition", "[ -f f ] || echo missing\necho done\n"),
          ("a bare `true`", "true\n"), ("a bare `:`", ":\n")]
ACCEPT = [("a live last statement",
           "python3 -c 'import sys; sys.exit(1)'\necho done\n"),
          ("a `set +e` block", "set +e\nfalse\necho ok\n"),
          ("a conditional body", "if test -f f; then grep -q p f; fi\n"),
          ("a loop body", "while read -r l; do grep -q p f; done < f\n"),
          ("a bare fallible command", "grep -q foo f\necho ok\n")]
wrong = []
for name, sc in REFUSE:
    if m._cannot_fail_why(sc) is None:
        wrong.append("not refused: " + name)
for name, sc in ACCEPT:
    if m._cannot_fail_why(sc) is not None:
        wrong.append("wrongly refused: " + name)
print("spec01: %d dead shapes refused, %d live shapes accepted, %d wrong"
      % (len(REFUSE), len(ACCEPT), len(wrong)))
for w in wrong:
    print("  " + w)
raise SystemExit(1 if wrong else 0)
PYEND
```
