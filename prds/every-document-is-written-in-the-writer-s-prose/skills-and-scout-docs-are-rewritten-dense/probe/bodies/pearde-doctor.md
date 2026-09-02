
Read @references/parts/doctor.md — the part table: what each row's `off` and
`broken` mean, which of them `--fix` touches, and why no agent is named
anywhere in the check. None of that table is repeated here. The scope is
`@@doctor`.

```bash
python3 @resources/pearde.py doctor [board]              # report; exit 1 when a part is broken
python3 @resources/pearde.py doctor --fix [board]        # report, then repair
python3 @resources/pearde.py doctor --harnesses [board]  # …and run the board's harnesses
```

Print every line returned. A part reading `off` is a problem only where the
user wanted that part.
