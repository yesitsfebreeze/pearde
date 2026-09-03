#!/usr/bin/env python3
"""pearde spend — what the workers cost, per model, off their transcripts.

    spend.py [--since YYYY-MM-DD] [--dir <projects dir>]

Walks `<dir>/*/*/subagents/*.jsonl` (default ~/.claude/projects) modified
since `--since` (default today). Per model: turns, context tokens billed
(input + cache_read + cache_creation), the average per turn, output tokens,
the median first-turn context (the floor), turns over 80K and their share of
the bill, idle-poll Bash turns (`sleep N; echo`, `true`, `:`) and their
context, and tool_result count and bytes by tool. Cost is turns × context
re-sent per turn, so the floor and the fat tail are the two numbers to move.

Python 3 stdlib only.
"""
import collections
import datetime
import glob
import json
import os
import re
import statistics
import sys

CAP = 80000
IDLE = re.compile(r"^(sleep \d+;?\s*)?(echo\s*\S*|true|:)\s*$")
CTX = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def rows(line):
    try:
        return json.loads(line)
    except ValueError:
        return None


def main(argv):
    since, root = datetime.date.today().isoformat(), "~/.claude/projects"
    it = iter(argv[1:])
    for a in it:
        if a == "--since":
            since = next(it)
        elif a == "--dir":
            root = next(it)
        else:
            print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
            return 2
    t0 = datetime.datetime.fromisoformat(since).timestamp()
    files = [f for f in glob.glob(os.path.expanduser(root) + "/*/*/subagents/*.jsonl")
             if os.path.getmtime(f) >= t0]
    turns, ctx, out, first, over, over_ctx, idle, idle_ctx = (
        collections.Counter() for _ in range(8))
    firsts = collections.defaultdict(list)
    res_n, res_b = collections.Counter(), collections.Counter()
    for f in files:
        seen, tool_of = False, {}
        for line in open(f, errors="ignore"):
            d = rows(line)
            if not d:
                continue
            m = d.get("message") or {}
            content = m.get("content") if isinstance(m.get("content"), list) else []
            if d.get("type") == "assistant" and m.get("usage"):
                us, mdl = m["usage"], m.get("model", "?")
                c = sum(us.get(k, 0) for k in CTX)
                turns[mdl] += 1
                ctx[mdl] += c
                out[mdl] += us.get("output_tokens", 0)
                if not seen:
                    firsts[mdl].append(c)
                    seen = True
                if c > CAP:
                    over[mdl] += 1
                    over_ctx[mdl] += c
                for b in content:
                    if b.get("type") != "tool_use":
                        continue
                    tool_of[b.get("id")] = b.get("name", "?")[:16]  # a mangled call has a page for a name
                    if b["name"] == "Bash" and IDLE.match(
                            (b.get("input") or {}).get("command", "").strip()):
                        idle[mdl] += 1
                        idle_ctx[mdl] += c
            elif d.get("type") == "user":
                for b in content:
                    if b.get("type") == "tool_result":
                        s = b.get("content")
                        s = s if isinstance(s, str) else json.dumps(s)
                        name = tool_of.get(b.get("tool_use_id"), "?")
                        res_n[name] += 1
                        res_b[name] += len(s)
    print(f"transcripts: {len(files)} since {since} under {root}")
    for mdl in sorted(ctx, key=lambda k: -ctx[k]):
        t = turns[mdl]
        print(f"\n{mdl}: turns={t} ctx={ctx[mdl] / 1e6:.1f}M avg={ctx[mdl] // t} "
              f"out={out[mdl] / 1e6:.2f}M floor(median first turn)="
              f"{int(statistics.median(firsts[mdl])) if firsts[mdl] else 0}")
        print(f"  turns >{CAP // 1000}K: {over[mdl]} = {over_ctx[mdl] / 1e6:.1f}M "
              f"({100 * over_ctx[mdl] / max(1, ctx[mdl]):.0f}% of ctx)")
        print(f"  idle-poll Bash turns: {idle[mdl]} = {idle_ctx[mdl] / 1e6:.1f}M ctx")
    print("\ntool_result by tool (count, bytes):")
    for name, n in res_n.most_common():
        print(f"  {name:<14} {n:>7} {res_b[name]:>12}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
