---
complexity: 12
footprint:
  - references/personas
---

# spec02 — the four personas and their roster are rewritten dense

`designer.md`, `engineer.md`, `mentor.md`, `skeptic.md` and `INDEX.md` carry
the same facts in fewer words, in the file format `INDEX.md` prescribes.

Two strings in a persona are frozen against each other and are not free prose:
a `## How you work` bullet closes with `[<Name>: <trait>]`, and the matching
`## Built from` bullet repeats that trait character for character. A `Built
from` bullet is also a citation — who, known for, the trait, the artefact — so
its words are facts, not padding. Of `skeptic.md`'s 634 words, 241 sit under
`## Built from` and a further ~75 in the bracketed traits, leaving ~290 words
a rewrite may touch.

Already standing, uncommitted in the lane: `skeptic.md` rewritten, 634 → 613
words, provenance still matching on both sides, `prose.py check` green. Left to
finish: `designer.md`, `engineer.md`, `mentor.md`, `INDEX.md`, and a second
pass over `skeptic.md`.

One collision the probe hit and settled: `prose.py check` flagged the trait
`price the change over the time it must be maintained` for its `it must`, and
the trait is a paraphrase rather than a quotation, so both copies were reworded
together to `price the change over the time of maintaining it`. A trait that
trips the checker is reworded in **both** places in one edit, never in one.

## Acceptance

- [x] `python3 resources/prose.py check references/personas/*.md` exits 0.
- [x] The group's words, `prose.py`'s own count, fall from 3112 to **2872 or fewer** — `prose.py stat <base>` summed over the group's lines. 7.7% off, and the check fails on the count itself.
- [x] Every persona's traits still match on both sides: for each file, the set of `Trait: <t>. Source:` strings under `## Built from` equals the set of `[<Name>: <t>]` strings under `## How you work`, and every `<Name>` in a bracket has a `## Built from` bullet.
- [x] Every persona keeps its prescribed shape: frontmatter of exactly `name`, `profession`, `description`; a first body paragraph naming the person and saying it is a composite; `## How you work` with 3-6 bold-led bullets; `## Voice`; `## Built from`.
- [x] Every `## Built from` citation is byte-identical to the base revision except where a trait was reworded in both copies at once — `git diff <base>` shows no changed book title, year, page, chapter, journal or URL.
- [x] `INDEX.md`'s **Roster** table still holds one row per file in the directory, with the same four columns and the same `id`, `name`, `profession` values.
- [x] `INDEX.md` still carries the fenced file-format block and the six numbered `persona create` steps.
- [x] `python3 resources/index.py check` names no `@` in `references/personas/`.
- [x] Every persona body is still second person: no pronoun anywhere stands for the person named in the file's own frontmatter. Read, not grepped — `they` for a user or a cited practitioner is correct and common, so no pattern separates the two.

## Verify and Proof

```sh
BASE=${BASE:-$(git merge-base HEAD main)}
set -e
PE="references/personas"
python3 resources/prose.py check $PE/designer.md $PE/engineer.md \
  $PE/mentor.md $PE/skeptic.md $PE/INDEX.md

# the two provenance lists still match, and the shape is intact
python3 - references/personas/designer.md references/personas/engineer.md \
         references/personas/mentor.md references/personas/skeptic.md <<'PROV'
import re, sys
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
BR = re.compile(r"^\s*\[([^:\]]+):\s*([^\]]+)\]\s*$", re.M)
BU = re.compile(r"^\s*- \*\*([^*]+)\*\* — .*?\. Trait: (.+?)\. Source: (.+)$", re.M)
bad = 0
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8").read()
    fm = FM.match(t)
    keys = tuple(l.split(":", 1)[0].strip()
                 for l in (fm.group(1).splitlines() if fm else []) if ":" in l)
    probs = []
    if keys != ("name", "profession", "description"):
        probs.append("frontmatter keys %s" % (keys,))
    for h in ("## How you work", "## Voice", "## Built from"):
        if "\n%s\n" % h not in t:
            probs.append("no `%s`" % h)
    if not probs:
        how, built = t.split("## Built from", 1)
        ht = {x.strip() for _, x in BR.findall(how)}
        bt = {x.strip() for _, x, _ in BU.findall(built)}
        probs += ["trait unbacked: %r" % x for x in sorted(ht - bt)]
        probs += ["trait backs nothing: %r" % x for x in sorted(bt - ht)]
        n = len(re.findall(r"^- \*\*", how, re.M))
        if not 3 <= n <= 6:
            probs.append("%d `## How you work` bullets, want 3-6" % n)
    print(p + (": ok" if not probs else ": " + "; ".join(probs)))
    bad += bool(probs)
sys.exit(1 if bad else 0)
PROV

# every citation is byte-identical apart from a trait reworded in both copies
for f in $PE/designer.md $PE/engineer.md $PE/mentor.md $PE/skeptic.md; do
  git show "$BASE:$f" | sed -n '/^## Built from/,$p' \
    | sed 's/\. Trait: .*\. Source: /. Source: /' > /tmp/c.old
  sed -n '/^## Built from/,$p' "$f" \
    | sed 's/\. Trait: .*\. Source: /. Source: /' > /tmp/c.new
  if ! diff /tmp/c.old /tmp/c.new; then
    echo "$f: a citation changed"; exit 1
  fi
done

# the roster still has one row per persona file
rows=$(grep -c '^| `' $PE/INDEX.md)
files=$(ls $PE/*.md | grep -vc INDEX.md)
[ "$rows" = "$files" ]

if python3 resources/index.py check | grep -q '^references/personas/'; then
  echo "a dangling @ under references/personas/"; exit 1
fi
# the ceiling, on prose.py's own count
python3 resources/prose.py stat "$BASE" | grep '^references/personas/' \
  | awk -F'[ >]+' '{b+=$2; a+=$4} END {
      printf "group: %d -> %d (%.1f%% off)\n", b, a, 100*(b-a)/b;
      if (a > 2872) { printf "over the %d ceiling\n", 2872; exit 1 } }'
```
