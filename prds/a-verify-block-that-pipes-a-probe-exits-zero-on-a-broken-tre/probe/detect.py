"""Prototype of the check this PRD asks for, plus a census of the board.

Two green-on-broken shapes that `_cannot_fail_why` lets through:

  drain  — a bare pipeline whose LAST member is a pure formatter. pipefail
           carries a non-zero the probe RAISES; it carries nothing from a
           probe that reports by PRINTING. The formatter ends 0 either way.
  eater  — a command that reads stdin with no redirect and no pipe into it.
           collect feeds the block to `bash` ON STDIN, so that command eats
           the rest of the block: every statement after it never runs and
           the block exits 0.
"""
import os, re, sys
# the repo holding the specs.py under test — the lane, by default
REPO = os.environ.get("PEARDE_REPO", "/Users/feb/dev/infra/pearde/pearde/"
                      ".lanes/a-verify-block-that-pipes-a-probe-exits-zero-"
                      "on-a-broken-tre")
sys.path.insert(0, os.path.join(REPO, "resources", "board"))
import specs  # noqa: E402

# end 0 whatever they are handed: they reformat, they do not judge
FORMATTERS = frozenset((
    "tail", "head", "cat", "sed", "awk", "tr", "sort", "uniq", "cut", "nl",
    "wc", "column", "fold", "rev", "tee", "expand", "unexpand", "paste"))
# read stdin when given no file operand
EATERS = frozenset((
    "cat", "grep", "egrep", "fgrep", "sed", "awk", "sort", "wc", "head",
    "tail", "read", "xargs", "tr", "uniq", "cut", "nl", "column", "rev",
    "tee", "python3", "python", "sh", "bash", "jq"))
_OPT = re.compile(r"^-")


def _words(text):
    return [w for w in text.strip().split() if w]


def _cmd_of(text):
    ws = _words(text)
    while ws and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", ws[0])
                  or ws[0] in ("!", "then", "else", "do", "time", "command")):
        ws = ws[1:]
    return ws[0].strip("\"'") if ws else ""


def _has_operand(text):
    """A file operand — something after the command that is not an option,
    not an option's value, and not a redirect."""
    ws = _words(text)[1:]
    for w in ws:
        if w.startswith("<") or w.startswith(">") or w.startswith("2>"):
            return True                      # redirected: stdin is not ours
        if _OPT.match(w):
            continue
        if w in ("|", "&&", "||"):
            break
        return True
    return False


def _redirected(text):
    return bool(re.search(r"(^|\s)<", text))


def findings(script):
    """[(kind, snippet)] — every drain and every eater in the block."""
    out = []
    for line in specs._logical_lines(script):
        segs = specs._segments(line)
        # rebuild the pipelines: consecutive segments joined by `|`
        pipes, cur, op_in = [], [], ""
        for op, text in segs:
            if op == "|":
                cur.append(text)
                continue
            if cur:
                pipes.append((op_in, cur))
            cur, op_in = [text], op
        if cur:
            pipes.append((op_in, cur))
        for op_in, members in pipes:
            # drain: a BARE pipeline (nothing routes its status) of two or
            # more members whose last member only reformats
            if len(members) > 1 and op_in in ("", ";", "&"):
                last = _cmd_of(members[-1])
                if last in FORMATTERS:
                    nxt = segs[segs.index((op_in, members[0])) + len(members)] \
                        if False else None
                    out.append(("drain", " | ".join(
                        m.strip() for m in members)[:70]))
            # eater: a first-position command reading stdin with no operand
            first = members[0]
            c = _cmd_of(first)
            if c in EATERS and not _has_operand(first) \
                    and not _redirected(first):
                out.append(("eater", first.strip()[:70]))
    return out


def board_census(board):
    rows = []
    prds = os.path.join(board, "prds")
    for prd in sorted(os.listdir(prds)):
        sd = os.path.join(prds, prd, "specs")
        if not os.path.isdir(sd):
            continue
        for f in sorted(os.listdir(sd)):
            if not f.endswith(".md"):
                continue
            p = os.path.join(sd, f)
            text = open(p, encoding="utf-8").read()
            m = re.search(r"^## Verify and Proof\s*$(.*?)(?=^## |\Z)", text,
                          re.M | re.S)
            if not m:
                continue
            b = re.search(r"^```[a-z]*\s*$(.*?)^```\s*$", m.group(1),
                          re.M | re.S)
            if not b:
                continue
            script = b.group(1)
            fs = findings(script)
            if fs:
                rows.append((f"{prd}/specs/{f}", fs,
                             specs._cannot_fail_why(script)))
    return rows


if __name__ == "__main__":
    board = sys.argv[1]
    rows = board_census(board)
    nd = ne = 0
    for path, fs, why in rows:
        kinds = sorted({k for k, _ in fs})
        nd += sum(1 for k, _ in fs if k == "drain")
        ne += sum(1 for k, _ in fs if k == "eater")
        print(f"{path}")
        for k, s in fs:
            print(f"    {k:6s} {s}")
        print(f"    cannot-fail checker says: "
              f"{'REFUSED' if why else 'accepted'}")
    print(f"\n{len(rows)} spec(s) hit · {nd} drain · {ne} eater")
