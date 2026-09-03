---
state: done
origin: requested
priority: 90
complexity: 29
blast-radius:
needs:
  - a-session-ledger-names-who-holds-what-and-reaps-what-is-gone
workflow: probe-then-spec
actual: 9.98h
commit: 4e311b8
---

# board-commands-run-in-the-session-s-tree-not-the-checkout — every board command resolves the running session's worktree as the code repo instead of the board's parent, and a session's commits reach the branch a person reads

every board command resolves the running session's worktree as the code repo instead of the board's parent, and a session's commits reach the branch a person reads

## Report

spec01: exit 0
== session take ==
{
  "id": "s43276",
  "pid": 43276,
  "started": "Thu Sep  3 09:14:54 2026",
  "cmd": "sleep 900",
  "worktree": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde/.sessions/s43276",
  "branch": "session/s43276",
  "repo": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code",
  "taken": "2026-09-03 09:14:54",
  "host": "mac.local"
}
== resolvers ==
{
  "plan.repo_root(board)": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde",
  "plan.prd_repo(prd)": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde/.sessions/s43276",
  "collect.repo_of(prd)": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde/.sessions/s43276",
  "brief.repo_of(prd)": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde/.sessions/s43276",
  "session.repo_of(board)": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code",
  "session tree on the ledger": "/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde/.sessions/s43276"
}

== verdict ==
  plan.repo_root(board)        /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.bnn0agSXhr/code/.pearde
  plan.prd_repo(prd)           SESSION TREE
  collect.repo_of(prd)         SESSION TREE
  brief.repo_of(prd)           SESSION TREE
  session.repo_of(board)       checkout

=== nosession — no ledger, old behaviour ===
  ok   repo_of is the checkout: '/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.gMxNv29uwc/nosession/code'
  ok   prd_repo is the checkout: '/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.gMxNv29uwc/nosession/code'
$ pearde claim p1 → 0
$ pearde collect p1 → 0
  ok   checkout main moved: '1'
  ok   checkout src/app.py: "print('two')\n"

=== two — two sessions, two lands ===
  ok   two trees on the ledger: True
$ pearde claim p1 → 0
$ pearde claim p2 → 0
  ok   lane A off session A: 'd0a9c36a8a71abd97a231b88bcaea16dbac5d40b'
  ok   lane B off session B: 'd0a9c36a8a71abd97a231b88bcaea16dbac5d40b'
$ pearde collect p1 → 0
$ pearde collect p2 → 0
  ok   both collects landed on main themselves: '0'
  ok   checkout holds A's file after the collects: "print('two')\n"
  ok   checkout holds B's file after the collects: True
$ pearde session land → 0
  ok   A lands: 0
$ pearde session land → 0
  ok   B lands after A: 0
  ok   A's commit still on main: '0'
  ok   checkout holds A's file: "print('two')\n"
  ok   checkout holds B's file: True
  ok   linear history: '0'

=== dirty — the checkout has uncommitted work of its own ===
$ pearde claim p1 → 0
$ pearde collect p1 → 0
  ok   collect still succeeds: 0
  ok   collect says the land was refused: True
  ok   the person's uncommitted work is untouched: "print('a person was here')\n"
  ok   the work is on the session branch: '1'

=== units — the resolver's own answers ===
  ok   held with no ledger: None
  ok   instead_of with no ledger is the repo it was handed: True
  ok   held when the ledger's worktree is not on disk: None
  ok   held is the session's tree: True
  ok   held for a row whose repo is another repo: None
  ok   held with no session process: None
  ok   instead_of with no session process: True
  ok   instead_of on a malformed ledger: True
  ok   my_id walks the process tree once for five asks: 1
  ok   held through a symlinked board: True
  ok   under() is a real-path test: True
  ok   checkout_of for a board that is its own repo: True
  ok   checkout_of for a board that is a plain dir in a repo: True
  ok   spelling_root for a repo the board hosts: True
  ok   spelling_root for a repo outside the board: True
  ok   a footprint under the board still routes to the board's repo: ('/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.gMxNv29uwc/units/code/.pearde', '.gitignore')
  ok   ordinary code routes to the session's tree: ('/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.gMxNv29uwc/units/code/.pearde/.sessions/s43288', 'src/app.py')
  ok   repo_of with a repo: key the ledger does not name: True
  ok   repo_of with a repo: key the ledger does name: True
  ok   plan.prd_repo with session.py absent: (0, True)
  ok   land_session with session.py absent: (0, "''")
  ok   land_session with no ledger: ''
  ok   land_session when land raises: True

=== edges — what land refuses, and the branch it aims at ===
$ pearde session land → 0
  ok   land on a trunk that is not called main: 0
  ok   the trunk carries the session's commit: '0'
  ok   no merge commit on the trunk: '0'
  ok   the checkout's own file moved: "print('two')\n"
$ pearde session land → 1
    session land: the checkout is on trunk itself — it is already the branch a person reads
  ok   land refuses the branch the checkout is already on: 1
  ok   and says why: True
$ pearde session land → 1
    session land: main would not fast-forward to session/s43914 in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.gMxNv29uwc/dirtyland/code — error: Your local changes to the following files would be overwritten by merge:
  ok   land into a dirty checkout exits 1: 1
  ok   the person's uncommitted work is byte-identical: "print('a person was here')\n"
  ok   the commit is still on the session branch: '1'
  ok   pearde help names the verb: True

all checks pass
pearde session: takes take, list, reap, land, owns

spec02: exit 0
session tree /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.WwXOdnJBdD/code/.pearde/.sessions/s44009
session branch session/s44009

== the session commits something of its own ==
  ok   session branch ahead before the claim: '1'
== claim ==
$ pearde claim p1 → 0
    ▸ p1: specced → claimed · done 0/1 · 0% · open 0/1 · 0% · ready 0 · blocked 1 @∞ workers · pass file owed · as engineer
  ok   lane on disk: True
  ok   lane's upstream commit: 'd9ff499f5f0c63ba2ae5a4af3513954ca01678a2'
  ok   lane holds the session-only file: True

== the worker writes in its lane ==

== collect ==
$ pearde collect p1 → 0
    p1: lane lane/p1 merged — 1 commit(s)
    ▸ p1: claimed → done · done 1/1 · 100% · open 0/1 · 0% · ready 0 · blocked 0 @∞ workers · commit deb31d4 5dce361 · record 66d3c9d · landed on main · daemon answered in another shape — report not posted (TypeError: expected str, bytes or os.PathLike object, not NoneType) · pass file owed · as engineer

== where did the commit land ==
  ok   collect landed it on main itself: '0'
  ok   checkout src/app.py now says two: "print('two')\n"
  ok   session tree src/app.py: "print('two')\n"

== land again — nothing left ==
$ pearde session land → 0
    session/s44009 has nothing main has not got
  ok   land exit: 0
  ok   checkout main is the session's commit: 'deb31d45af03940e257f124e66023e001cc53447'
  ok   checkout src/app.py now says two: "print('two')\n"
  ok   main..session empty: '0'
  ok   one commit for the PRD: '2'

all checks pass

=== nosession — no ledger, old behaviour ===
  ok   repo_of is the checkout: '/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.CLb4hz0zWX/nosession/code'
  ok   prd_repo is the checkout: '/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.CLb4hz0zWX/nosession/code'
$ pearde claim p1 → 0
$ pearde collect p1 → 0
  ok   checkout main moved: '1'
  ok   checkout src/app.py: "print('two')\n"

=== two — two sessions, two lands ===
  ok   two trees on the ledger: True
$ pearde claim p1 → 0
$ pearde claim p2 → 0
  ok   lane A off session A: '2b7658a17a737eefe7480d7e489e4223d0da27f1'
  ok   lane B off session B: '2b7658a17a737eefe7480d7e489e4223d0da27f1'
$ pearde collect p1 → 0
$ pearde collect p2 → 0
  ok   both collects landed on main themselves: '0'
  ok   checkout holds A's file after the collects: "print('two')\n"
  ok   checkout holds B's file after the collects: True
$ pearde session land → 0
  ok   A lands: 0
$ pearde session land → 0
  ok   B lands after A: 0
  ok   A's commit still on main: '0'
  ok   checkout holds A's file: "print('two')\n"
  ok   checkout holds B's file: True
  ok   linear history: '0'

=== dirty — the checkout has uncommitted work of its own ===
$ pearde claim p1 → 0
$ pearde collect p1 → 0
  ok   collect still succeeds: 0
  ok   collect says the land was refused: True
  ok   the person's uncommitted work is untouched: "print('a person was here')\n"
  ok   the work is on the session branch: '1'

=== units — the resolver's own answers ===
  ok   held with no ledger: None
  ok   instead_of with no ledger is the repo it was handed: True
  ok   held when the ledger's worktree is not on disk: None
  ok   held is the session's tree: True
  ok   held for a row whose repo is another repo: None
  ok   held with no session process: None
  ok   instead_of with no session process: True
  ok   instead_of on a malformed ledger: True
  ok   my_id walks the process tree once for five asks: 1
  ok   held through a symlinked board: True
  ok   under() is a real-path test: True
  ok   checkout_of for a board that is its own repo: True
  ok   checkout_of for a board that is a plain dir in a repo: True
  ok   spelling_root for a repo the board hosts: True
  ok   spelling_root for a repo outside the board: True
  ok   a footprint under the board still routes to the board's repo: ('/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.CLb4hz0zWX/units/code/.pearde', '.gitignore')
  ok   ordinary code routes to the session's tree: ('/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.CLb4hz0zWX/units/code/.pearde/.sessions/s44146', 'src/app.py')
  ok   repo_of with a repo: key the ledger does not name: True
  ok   repo_of with a repo: key the ledger does name: True
  ok   plan.prd_repo with session.py absent: (0, True)
  ok   land_session with session.py absent: (0, "''")
  ok   land_session with no ledger: ''
  ok   land_session when land raises: True

=== edges — what land refuses, and the branch it aims at ===
$ pearde session land → 0
  ok   land on a trunk that is not called main: 0
  ok   the trunk carries the session's commit: '0'
  ok   no merge commit on the trunk: '0'
  ok   the checkout's own file moved: "print('two')\n"
$ pearde session land → 1
    session land: the checkout is on trunk itself — it is already the branch a person reads
  ok   land refuses the branch the checkout is already on: 1
  ok   and says why: True
$ pearde session land → 1
    session land: main would not fast-forward to session/s44833 in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.CLb4hz0zWX/dirtyland/code — error: Your local changes to the following files would be overwritten by merge:
  ok   land into a dirty checkout exits 1: 1
  ok   the person's uncommitted work is byte-identical: "print('a person was here')\n"
  ok   the commit is still on the session branch: '1'
  ok   pearde help names the verb: True

all checks pass

spec03: exit 0
