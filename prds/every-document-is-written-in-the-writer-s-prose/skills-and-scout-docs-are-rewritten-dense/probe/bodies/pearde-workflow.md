
Read @references/workflow.md for the format — the two file shapes, the closed
frontmatter set, the steps grammar, and the `## Workflow <slug>` section a run
returns. @references/parts/workflows.md is the mechanism: when one is written,
how one is attached, what a run may change, the table deciding whether each
returned edit is applied or refused, and how `runs` is counted. Loop step 6 is
where the collect happens. The scope is `@@workflows`.

```sh
python3 @resources/pearde.py workflow list  [board]        # slug · kind · runs · updated · subject
python3 @resources/pearde.py workflow show  <slug> [board] # the file
python3 @resources/pearde.py workflow brief <slug> [board] # the workflow as one page, atomics inlined
python3 @resources/pearde.py workflow check [board]        # what doctor reports for `workflows`
```

`workflow` forwards to @resources/workflows.py, the only reader of that
format. `brief` is what a worker is handed, and exits 1 on an atomic slug — an
atomic is shown, not briefed.

Workflows live at `.pearde/workflows/`, so reading one needs a board. With
none in scope, say where the library would be. Adding a file and attaching a
slug to a PRD are orchestrator writes, and neither happens uninvited.
