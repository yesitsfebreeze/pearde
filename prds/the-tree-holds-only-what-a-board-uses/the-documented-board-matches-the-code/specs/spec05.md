---
complexity: 6
footprint:
  - references/parts/view.md
  - resources/board/view.js
  - resources/board/view.css
  - resources/board/viewtest.js
  - README.md
---

# spec05 — eight views, one shortcut each, and README's counts are the ones init writes

`references/parts/view.md` said **seven views** and `⌘1–7`. `render.py` draws
eight tabs in `#views` — boards, plan, board, analytics, asks, list, memos,
report — and eight `section[data-view]` blocks to match. `view.js` bound
`⌘1`–`⌘7`, so the eighth tab had no shortcut, and its own comment said `⌘1..⌘6`,
disagreeing with the condition two lines below it. The same stale "seven views"
comment sat in `view.css` and in `viewtest.js`.

`view.md`'s section table was worse than a wrong count: its row 1 was
**what's up**, which is not a tab at all but the prose aside `#purpose`, drawn
on every view — and `boards`, which is a tab, appeared in no row. Rows 1-8 now
name the eight tabs in bar order, and the aside is described below the table as
what it is.

This is the one line of the PRD where the code moved rather than the text:
binding `⌘8` is a one-character change and the alternative — documenting that
one tab is unreachable by keyboard — makes the page worse.

README's `init --example` row said the command writes four `.gitignore` names.
`init.ignored_names` returns ten, and a real run in a fresh git repo writes all
ten plus `grammar.md`, which the row also omitted.

**What already stands** (built in the analysis pass, uncommitted in the lane):
`view.md`'s count, its `⌘1–8` line in the prose and in the keyboard table, and
its rebuilt section table; `view.js`'s bound range and comment; the two stale
comments in `view.css` and `viewtest.js`; README's row.

**What is left to finish**: review and commit, and run the view's own browser
gate once against a served board — `node resources/board/viewtest.js
http://127.0.0.1:8443/board/<name>` — because `⌘8` is the only behaviour change
in this PRD. `view.md`'s `/pass` sentence needs nothing: the route is already
gone from `serve.py` and the page already says so.

## Acceptance

- [ ] `references/parts/view.md` says eight views and `⌘1–8`, in the prose and in the keyboard table.
- [ ] `view.md`'s section table has rows 1-8 naming boards, timeline, board, analytics, asks, list, memos, report — the same names and order as the `data-v=` anchors in `resources/board/render.py`'s `#views` nav.
- [ ] `view.md` describes `what's up` as the prose aside rather than as a numbered view, and no row of the section table names it.
- [ ] `resources/board/view.js` binds `⌘1` through `⌘8`, and its comment names the same range; `node --check` passes on it.
- [ ] Neither `view.css` nor `viewtest.js` still says "seven views".
- [ ] `README.md`'s `init --example` row says ten `.gitignore` names and lists `grammar.md` among what it writes, and `init.ignored_names` returns exactly ten entries.
- [ ] `node resources/board/viewtest.js <served board URL>` passes, and `⌘8` opens the report tab in a served page.

## Verify and Proof

```sh
sh .pearde/prds/the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code/probe/verify.sh "$PWD" "$PWD/.pearde"
node --check resources/board/view.js
node --check resources/board/viewtest.js
grep -q 'Eight views' references/parts/view.md
grep -q '⌘1–8' references/parts/view.md
grep -q 'e.key <= "8"' resources/board/view.js
test -z "$(grep -rn 'seven views' resources/board references)"
test "$(grep -c 'data-v="' resources/board/render.py)" = 8
grep -q 'ten `.gitignore` names' README.md
test "$(python3 -c "
import ast
src = open('resources/board/init.py', encoding='utf-8').read()
fn = next(n for n in ast.parse(src).body
          if isinstance(n, ast.FunctionDef) and n.name == 'ignored_names')
print(len(next(n for n in ast.walk(fn) if isinstance(n, ast.Return)).value.elts))
")" = 10
```
