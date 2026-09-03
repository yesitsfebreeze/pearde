r"""Every backtick-quoted token and every fenced line at <ref> survives in the
working tree. Unwraps hard-wrapped prose first, so a token split across two
lines is one token. Strips a leading `@` — an address may gain or lose it.

Code spans are read by the CommonMark rule: a run of N backticks opens one and
the next run of exactly N closes it. Pairing them with `` `([^`]+)` `` instead
mis-reads the double-backtick escape a literal backtick needs — measured on
`references/workflow.md`, whose one such line left a backtick unpaired and,
because the body is joined before matching, inverted every span after it, so
49 stretches of ordinary prose were held character-identical as though they
were commands.

An `@` address carries its trailing punctuation: `AT` matches `[\w./-]+`, so
`@index.md.` at the end of a sentence is one token and re-punctuating the
sentence around it reads as a lost address. Deliberate — the sentence is the
address's only delimiter here — but the message names the token, not the
change, so check the diff before putting a fact back."""
import re, subprocess, sys

FENCE = re.compile(r"^\s*```")
RUN = re.compile(r"`+")
AT = re.compile(r"@@?[\w./-]+")


def spans(text):
    """The content of every code span, CommonMark backtick-run pairing."""
    out, runs, i = [], [(m.start(), m.end()) for m in RUN.finditer(text)], 0
    while i < len(runs):
        s, e = runs[i]
        n = e - s
        for j in range(i + 1, len(runs)):
            s2, e2 = runs[j]
            if e2 - s2 == n:
                out.append(text[e:s2])
                i = j
                break
        i += 1
    return out


def tokens(text):
    body, fenced, inside = [], [], False
    for line in text.splitlines():
        if FENCE.match(line):
            inside = not inside
            continue
        (fenced if inside else body).append(line.strip())
    joined = " ".join(body)
    out = {re.sub(r"\s+", " ", t).strip().lstrip("@") for t in spans(joined)}
    out |= {l for l in (x.strip() for x in fenced) if l}
    out |= {a.lstrip("@") for a in AT.findall(joined)}
    return {t for t in out if t}


ref = sys.argv[1]
bad = 0
for f in sys.argv[2:]:
    old = subprocess.run(["git", "show", f"{ref}:{f}"], capture_output=True, text=True).stdout
    lost = sorted(tokens(old) - tokens(open(f, encoding="utf-8").read()))
    if lost:
        bad = 1
        print(f"{f}: {len(lost)} lost: " + " · ".join(repr(t) for t in lost))
sys.exit(bad)
