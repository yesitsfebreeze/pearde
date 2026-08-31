# ── can a verify block fail? ──────────────────────────────────────────────────

# collect runs every `## Verify and Proof` block under `bash -e -o pipefail`
# with the code repo as cwd, and reads the exit code that comes out. Between
# those two rules the block goes red only when something makes the script's
# exit non-zero: a failing command aborts the script when it is the LAST
# element of its and-or list — any earlier element merely shapes the flow,
# `set -e` exempts it, and the list's own non-zero result is carried on
# without an abort — and where nothing aborts, the block's exit is its
# final statement's status. So a block cannot fail iff no statement can
# abort and the last one can only end 0: every fallible command sits behind
# an always-0 fallback (`|| true`), an inversion (`!`), or a condition, and
# the block ends on an `echo`. collect reads exactly that exit, so a box
# carried by such a block is not a check — the shape the runner surfaced
# four times today. `specced` refuses it.

import re


# Builtin commands whose exit status is 0 come what may. Anything not listed
# counts as able to exit non-zero — over-counting only ever accepts a block;
# under-counting would refuse a live one.
# counts as able to exit non-zero — over-counting only ever accepts a block;
# under-counting would refuse a live one.
ALWAYS0 = frozenset(("echo", "printf", "true", ":", "pwd", "export", "unset",
                     "set", "readonly", "declare"))
# Words that open a segment whose failure is a condition or syntax — it
# routes instead of aborting, or it is the frame around the real command.
_COND_HEAD = re.compile(r"^(if|elif|while|until|for|case)([ \t(]|$)")
_FRAME_HEAD = ("then", "else", "do", "fi")


def _segments(line, op=""):
    """[(op-before, text)] — top-level split at `;`, `&`, `|`, `&&`, `||`,
    never inside quotes or unquoted parentheses (a `$( )` substitution is
    one argument and keeps its own operators)."""
    out, cur, quote, depth = [], "", None, 0
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            cur += line[i:i + 2]
            i += 2
            continue
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and ch in ";|&":
            two = line[i:i + 2]
            if two in ("||", "&&"):
                out.append((op, cur))
                op, cur, i = two, "", i + 2
                continue
            out.append((op, cur))
            op, cur, i = ch, "", i + 1
            continue
        cur += ch
        i += 1
    out.append((op, cur))
    return out


_EXIT_RE = re.compile(r"^(exit|exec|logout|bye)([ \t]|$)")


def _leaves_shell(text):
    """`exit` (and kin) leave no fallback: executed, the shell is gone with
    its own status, whatever operator follows — but only when that status
    can be non-zero; `exit 0` is a success like `true`."""
    t = text.strip()
    if not _EXIT_RE.match(t):
        return False
    if re.match(r"^exit[ \t]+0$", t):
        return False
    return True


def _plain_succeeds(text):
    """True only when this command is KNOWN to succeed — the inverse's only
    failure mode. An unknown command may succeed, so an inverted unknown
    command may return 1."""
    tokens = text.strip().split()
    while len(tokens) > 1 and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=",
                                        tokens[0]) or tokens[0] in
                               _FRAME_HEAD):
        tokens = tokens[1:]
    first = tokens[0].strip("\"'") if tokens else ""
    return first in ALWAYS0


def _seg_can_fail(text):
    """True unless this one pipeline member always exits 0 — the
    conservative read: an unlisted command, or any shape this walker cannot
    read, counts as able to fail."""
    s = text.strip()
    if not s or s == "!":
        return True                     # a lone `!` is a syntax error
    if s.startswith("!") and not s.startswith("[["):
        # an inversion routes: a failing command turns 0, a succeeding one
        # turns 1 — and a `!`-pipeline's failure never trips `set -e`. Only
        # the SUCCESS of the command underneath can leave a 1 behind.
        return _plain_succeeds(s[1:].strip())
    if _COND_HEAD.match(s):
        return False                    # a condition routes, not aborts
    if re.match(r"^(done|fi|esac)([ \t;&|]|$)", s):
        return False                    # a loop or branch frame
    if re.match(r"^exit[ \t]+0$", s):
        return False
    stripped, tokens = False, s.split()
    while len(tokens) > 1 and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=",
                                        tokens[0]) or tokens[0] in
                               _FRAME_HEAD):
        tokens, stripped = tokens[1:], True
    first = tokens[0].strip("\"'") if tokens else ""
    if first == "exit":
        return True                     # exits the shell, fallback or not
    if first in ALWAYS0:
        return False
    # a bare assignment holds no status of its own — `x=1` is 0 come what
    # may, `x=$(cmd)` inherits the substitution's: the classic abort
    if not stripped and all(re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t)
                            for t in tokens):
        return bool(re.search(r"\$\(|`", s))
    return True


def _unquote_hash(line):
    """Cut an unquoted trailing comment — its words are no command."""
    quote, i = None, 0
    while i < len(line):
        ch = line[i]
        if ch == "\\":
            i += 2
            continue
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
        i += 1
    return line


def _logical_lines(script):
    """[line] — comments gone, backslash continuations joined, heredoc bodies
    and function definitions skipped: what they hold is data or something
    defined, not a command that runs."""
    raw = script.splitlines()
    out, i = [], 0
    while i < len(raw):
        line = raw[i]
        i += 1
        while line.rstrip().endswith("\\") and i < len(raw):
            line = line.rstrip()[:-1] + " " + raw[i]
            i += 1
        line = _unquote_hash(line)
        m = re.search(r"<<-?[ \t]*([\"']?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        if m:
            while i < len(raw) and raw[i].strip() != m.group(2):
                i += 1
            i += 1
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^function[ \t]+\w+|^\w+[ \t]*\(\)[ \t]*\{", line):
            # a definition: the body does not run here, but what FOLLOWS it
            # on the line does — cut the braces out of the line and keep the
            # rest; a multi-line body skips past its closing brace
            if line.count("{") > line.count("}"):
                depth = line.count("{") - line.count("}")
                while i < len(raw) and depth > 0:
                    depth += raw[i].count("{") - raw[i].count("}")
                    i += 1
                i += 1
                continue
            line = re.sub(r"\{[^}]*\}", ":", line)
            stripped = line.strip()
        if line in ("{", "}"):
            continue
        out.append(line)
    return out


def _pipe_member_can_fail(idx, text):
    """One member of a pipeline: fallible unless always-0. A `!` is legal
    only as the FIRST word of a whole pipeline — mid-pipeline it is a syntax
    error, and a syntax error is a failure."""
    s = text.strip()
    if idx > 0 and s.startswith("!"):
        return True
    return _seg_can_fail(text)
    """(possible exit statuses, aborts) for one and-or statement — a walk
    over the abstract statuses each element can leave behind. An element
    runs when the operator before it allows: `&&` after a 0, `||` after a
    non-0, a bare element always. A failing element is exempt from
    `set -e` while it is not the list's LAST element, and an inverted `!`
    pipeline is exempt always — its non-zero status merely carries. `exit`
    kills the shell through any operator when its status can be non-zero."""
    last = len(elements) - 1
    statuses, abort = {0}, False
    for i, (op, cf, lethal, inverted) in enumerate(elements):
        runs = False
        for s in statuses:
            if op == "|" or (op in ("", "&&") and s == 0) or \
                    (op == "||" and s != 0):
                runs = True
                break
        if not runs:                          # nothing executes from here on
            continue
        old = statuses
        statuses = {0, 1} if cf else {0}
        if lethal or (cf and i == last and not inverted):
            abort = True
            break
        if op == "||" and not cf:
            statuses = {0}                    # the fallback resets the status
        elif 1 in old:
            statuses.add(1)                   # a carried non-zero lives on
    return statuses, abort


def _statement_outcomes(elements):
    """(possible exit statuses, aborts) for one and-or statement — a walk
    over the abstract statuses each element can leave behind. An element
    runs when the operator before it allows: `&&` after a 0, `||` after a
    non-0, a bare element always. A failing element is exempt from
    `set -e` while it is not the list's LAST element, and an inverted `!`
    pipeline is exempt always — its non-zero status merely carries. `exit`
    kills the shell through any operator when its status can be non-zero."""
    last = len(elements) - 1
    statuses, abort = {0}, False
    for i, (op, cf, lethal, inverted) in enumerate(elements):
        runs = False
        for s in statuses:
            if op == "|" or (op in ("", "&&") and s == 0) or \
                    (op == "||" and s != 0):
                runs = True
                break
        if not runs:                          # nothing executes from here on
            continue
        old = statuses
        statuses = {0, 1} if cf else {0}
        if lethal or (cf and i == last and not inverted):
            abort = True
            break
        if op == "||" and not cf:
            statuses = {0}                    # the fallback resets the status
        elif 1 in old:
            statuses.add(1)                   # a carried non-zero lives on
    return statuses, abort




def _cannot_fail_why(script):
    """Why the block cannot exit non-zero, or None when something can make
    it red — the one check a box must pass to be a check at all: every
    statement analysed, `||` fallbacks routing instead of aborting, a
    failure only fatal when it is the list's last element."""
    statements, elements, elem_op, pipe = [], [], "", []

    def flush_element():
        nonlocal pipe
        if pipe:
            # a `!` mid-pipeline never parses: the script dies at parse,
            # before any operator could absorb anything
            if any(i > 0 and t.strip().startswith("!")
                   for i, t in enumerate(pipe)):
                return "syntax"
            cf = any(_pipe_member_can_fail(i, t) for i, t in enumerate(pipe))
            lethal = any(_leaves_shell(t) for t in pipe)
            inverted = all(t.strip().startswith("!") for t in pipe) and pipe[0].strip().startswith("!")
            elements.append((elem_op, cf, lethal, inverted))
            pipe = []

    def flush_statement():
        if flush_element():
            return "syntax"
        if elements:
            statements.append(elements[:])
            del elements[:]
        nonlocal elem_op
        elem_op = ""

    for line in _logical_lines(script):
        if line.lstrip().startswith("set +e"):
            return None                        # unanalysable — it can fail
        if re.match(r"^(while|until|for|if|elif)\b", line.strip()) or \
                re.match(r"^(do|then|else|done|fi|esac)\b", line.strip()) or \
                re.search(r"(^|[;&|])\s*(if|then|done|fi|do)\b", line.strip()):
            # a loop or branch: multi-line when the head line opens it, and
            # its head/frames mask the `;` boundaries. The head's condition
            # routes; the body can fail like a bare command — but the body
            # is unattributable across lines, so let the whole construct
            # count as able to fail unless its body is empty or only
            return None
        if re.match(r"^[|]", line.strip()) or re.match(r"^&&", line.strip()):
            # a pipeline member on its own line — the walk rejoins backslash
            # continuations but not implicit `|` continuations; unreadable
            return None
            if not stripped or stripped in (";", ":"):
                continue
            for _, t in _segments(stripped):
                t = t.strip()
                if not t:
                    continue
                if re.match(r"^(while|until|for|if|elif)\b", t):
                    continue                   # the condition is exempt
                if _seg_can_fail(t):
                    # the body can run and fail in a world where its
                    # condition held — `if grep; then exit 1` aborts when
                    # grep finds; the condition itself never decides
                    return None
            continue
        for op, text in _segments(line):
            if op == "|":
                pipe.append(text)
                continue
            if op in ("&&", "||"):
                if flush_element():
                    return None
                elem_op = op
            else:                              # "", ";", "&" — a boundary
                if flush_statement():
                    return None
            if text:
                pipe.append(text)
        if pipe or elements:
            if flush_statement():
                return None
    if flush_statement():
        return None
    if not statements:
        return "it holds no command"
    guarded = 0
    for si, elements in enumerate(statements):
        statuses, abort = _statement_outcomes(elements)
        if abort:
            return None
        # a non-zero result carried out of a statement is the script's exit
        # only when nothing runs after it — a later statement overwrites it
        if si == len(statements) - 1 and statuses != {0}:
            return None
        guarded += sum(1 for _, cf, _l, _i in elements if cf)
    if guarded == 0:
        return "it holds no command that runs and can exit non-zero"
    return ("every fallible command is guarded and its last statement only "
            "ends 0 — nothing in it can make the block red")