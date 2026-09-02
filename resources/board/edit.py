#!/usr/bin/env python3
"""pearde edit — the writers. Every change the view makes to a board goes
through here. Nothing else in the tree writes a `prd.md`.

Each writer touches the smallest thing that can be touched: one frontmatter
line, the `# title` line, the body under the frontmatter, or a `## Section`
appended to. Frontmatter and body are never written in the same call — a body
edit cannot lose a `state:`, and a state edit cannot reflow prose. Every write
is atomic, a temp file and a rename — the daemon reads these files a second at
a time.

Python 3 stdlib only.
"""
import os
import re


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)

def split_fm(text):
    """(before, fm_lines, after) — the frontmatter block, or None for fm_lines
    when the file has none."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[:1]), lines[1:i], "".join(lines[i:])
    return "", None, text

def set_key(path, key, value):
    """Set one scalar frontmatter key, in place, keeping the file's own
    indentation and any trailing comment. A key the file does not have is
    appended to the block; a file with no frontmatter gets one."""
    text = open(path, encoding="utf-8").read()
    head, fm, tail = split_fm(text)
    line_re = re.compile(r"^(\s*)" + re.escape(key) + r":\s*(.*?)(\s+#.*)?$")
    if fm is None:
        return write_atomic(path, f"---\n{key}: {value}\n---\n\n" + text)
    for i, line in enumerate(fm):
        m = line_re.match(line.rstrip("\n"))
        if m:
            fm[i] = f"{m.group(1)}{key}: {value}{m.group(3) or ''}\n"
            break
    else:
        fm.append(f"{key}: {value}\n")
    write_atomic(path, head + "".join(fm) + tail)

def del_key(path, key):
    text = open(path, encoding="utf-8").read()
    head, fm, tail = split_fm(text)
    if fm is None:
        return
    keep = [l for l in fm
            if not re.match(r"^\s*" + re.escape(key) + r":\s", l)]
    if len(keep) != len(fm):
        write_atomic(path, head + "".join(keep) + tail)

def set_body(path, body):
    """Replace everything under the frontmatter. The frontmatter is never
    touched — it is the machine-read half, and a body edit must not be able to
    lose a `state:`."""
    text = open(path, encoding="utf-8").read()
    head, fm, _ = split_fm(text)
    keep = head + "".join(fm) + "---\n" if fm is not None else ""
    write_atomic(path, keep + "\n" + body.rstrip("\n") + "\n")

def section_span(body, heading):
    """(start, end) of the first `## <heading>` section, or None.

    Anchored to the start of a line, the way every reader of these files
    finds a section — @plan._h2_sections, @resources/questions.py, and `section()` in
    @view.js. A substring search is not the same test: a PRD that *mentions*
    a heading in its prose — "the parent's `## Answers` settled that" — hands
    a substring search a match inside a paragraph, and a writer working off
    that match appends into the middle of the body, under a heading that is
    not there. That is how `legal/legal-privacy` on the manola board came to
    carry two answers above `## Constraints`, invisible to every reader that
    counts answers, on 2026-08-31. The writer now finds sections the way the
    readers do, so what is written back is what is read back."""
    m = re.search(r"(?m)^##\s+" + re.escape(heading) + r"\b[^\n]*$", body or "")
    if not m:
        return None
    nxt = re.compile(r"(?m)^##\s+").search(body, m.end())
    return m.start(), (nxt.start() if nxt else len(body))


def append_section(path, heading, text):
    """Append text under `## <heading>`, creating the heading at the end of
    the body when it is not there. Additive only — nothing already written is
    touched, so the daemon can do it unsupervised."""
    body = open(path, encoding="utf-8").read().rstrip("\n")
    block = text.strip()
    span = section_span(body, heading)
    if span:
        # into the existing section, at its end: answers accumulate in order
        i, j = span
        head, mid, tail = body[:i], body[i:j], body[j:]
        body = head + mid.rstrip("\n") + "\n\n" + block + "\n" + tail
    else:
        body += f"\n\n## {heading}\n\n{block}\n"
    write_atomic(path, body.rstrip("\n") + "\n")

def retract_answer(path, qid):
    """Remove one question's answer from `## Answers` — the `**Qn**` line and
    the continuation lines under it, up to the next answer, blank-separated
    block or heading. Reopening a question is this plus `state: question`;
    every reader that counts answers (`plan`, `questions.py`) sees the
    question back on the frontier because the file says so, not the page.
    A section left empty loses its heading too — an empty `## Answers` reads
    as answered when it is not."""
    body = open(path, encoding="utf-8").read()
    mark = "## Answers"
    span = section_span(body, "Answers")
    if not span:
        return False
    i, j = span
    head, mid, tail = body[:i], body[i:j], body[j:]
    line_re = re.compile(r"^\s*\*\*\s*" + re.escape(qid) + r"\s*\*\*",
                         re.I)
    any_re = re.compile(r"^\s*\*\*\s*Q?\d+[a-z]?\s*\*\*", re.I)
    lines, keep, dropping, dropped = mid.splitlines(keepends=True), [], False, False
    for line in lines:
        if line_re.match(line):
            dropping = dropped = True
            continue
        if dropping and (any_re.match(line) or not line.strip()
                         or line.lstrip().startswith("#")):
            dropping = False
        if not dropping:
            keep.append(line)
    if not dropped:
        return False
    left = "".join(keep)
    if not left.replace(mark, "").strip():
        left = ""                      # nothing under the heading: drop both
    write_atomic(path, (head + left + tail).rstrip("\n") + "\n")
    return True

def set_title(path, title):
    """The `# ` line is the PRD's title — sync reads it, not the directory
    name. Rewrite the first one; a PRD without a heading gets one."""
    text = open(path, encoding="utf-8").read()
    head, fm, tail = split_fm(text)
    lines = tail.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i] = f"# {title}\n"
            break
    else:
        i = 1 if lines and lines[0].strip() == "---" else 0
        lines.insert(i, f"\n# {title}\n")
    write_atomic(path, head + ("".join(fm) if fm else "") + "".join(lines))
