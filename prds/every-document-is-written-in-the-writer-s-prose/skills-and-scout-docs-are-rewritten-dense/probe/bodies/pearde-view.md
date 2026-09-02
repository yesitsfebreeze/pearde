
Read @references/parts/view.md — the service and its singleton, the sections,
the axes, the writers, the deep links, and what the board keeps on disk.
@references/parts/order.md is why the sequence runs in the order given, and the
file to read before arguing with the order. `http://127.0.0.1:8443/board/all` renders every
watched board on one read-only page, and @references/parts/all.md says what
that merges and why a master board is a different thing. The scopes are
`@@view`, `@@order` and `@@all`.

```bash
python3 @resources/pearde.py view           # start it, register this board, print the URL
python3 @resources/pearde.py view status    # what it is watching
python3 @resources/pearde.py view stop      # end it
python3 @resources/pearde.py plan           # the frontier and the queue, no service
python3 @resources/pearde.py gantt --open   # .pearde/.state/view.html, self-contained
python3 @resources/pearde.py reconcile      # recompute after anything moved
```

The board plans and reads without any of the above. The view is how a person
looks at it.
