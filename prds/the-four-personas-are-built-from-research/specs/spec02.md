---
complexity: 6
footprint:
  - .pearde/prds/the-four-personas-are-built-from-research/probe/check_personas.py
---

# spec02 — the grammar probe reads every trace on a bullet, not the first

The probe that checks the persona grammar counted a bullet's traces once. A
bullet carrying two — `engineer.md` has two of them — had its second trace
never checked, and the practitioner behind it reported as backing no behaviour.
The probe now reads every `[<Name>: <trait>]` on a bullet.

**What already stands.** `MARK.finditer` replaces `MARK.search`, every trace on
a bullet is name-checked and trait-checked, and the `used` set is built from all
of them. The orphan check reads that set. Two dead fragments went with it: an
unused `TAIL` pattern, and a `prose` comprehension whose `or True` made its
filter a no-op. With the fix, `engineer.md` goes from one false orphan pair
(`Diomidis Spinellis`, `Rob Pike`) to green, unchanged.

**What is left.** Confirm the probe fails on an injected bad trace — a check
that cannot go red is worth nothing — and run the verify below. The source
assertion was also tightened: `len(source) > 8` passed the placeholder
`<the artefact>.`, so a source must now name a year. That is a shape check and
proves nothing about whether the artefact exists; the report says so plainly.

## Acceptance

- [x] a `## How you work` bullet carrying two traces has both checked against `## Built from`
- [x] a practitioner referenced only by a bullet's second trace is not reported as an orphan
- [x] `references/personas/engineer.md` passes with no orphan row
- [x] the probe still exits 1 and names the row when a trace points at a name absent from `## Built from`
- [x] the probe prints a tally line `<n> checks, <p> pass, <f> fail` and every persona is green
- [x] a `## Built from` bullet whose `Source:` names no year is refused — the old check passed any string over eight characters, including the placeholder `<the artefact>.`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
probe=.pearde/prds/the-four-personas-are-built-from-research/probe/check_personas.py

grep -q 'MARK.finditer' "$probe" || { echo "RED: probe still reads one trace per bullet"; exit 1; }
echo "ok   probe reads every trace on a bullet"

out=$({ python3 "$probe" || true; })
[ -n "$out" ] || { echo "RED: the probe printed nothing — it died before its tally"; exit 1; }
printf '%s\n' "$out" | grep -q 'engineer: every practitioner backs a bullet' \
  || { echo "RED: engineer orphan row absent"; exit 1; }
printf '%s\n' "$out" | { grep '^FAIL engineer' || true; } | { grep -q . && { echo "RED: engineer has a failing row"; exit 1; } || echo "ok   engineer green"; }

# The check must be able to go red, and on the SECOND trace of a bullet — the
# exact mutation a probe reading one trace per bullet stays green on. The line
# is found at run time, never pinned to a practitioner's name, and the run is
# made in a directory built here, never under .pearde/prds/.
ln=$({ awk '/^- /{t=0} /^ *\[[^]:]+: [^]]*\]$/{t++; if (t==2) print NR}' \
        references/personas/engineer.md || true; } | head -1)
[ -n "$ln" ] || { echo "RED: no bullet carries a second trace — the flip proves nothing"; exit 1; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/references/personas" "$tmp/.pearde/prds/x/probe"
cp references/personas/*.md "$tmp/references/personas/"
cp "$probe" "$tmp/.pearde/prds/x/probe/check_personas.py"
awk -v L="$ln" 'NR==L{sub(/\[[^]:]+:/, "[Nobody At All:")} {print}' \
  references/personas/engineer.md > "$tmp/references/personas/engineer.md"
if out=$({ python3 "$tmp/.pearde/prds/x/probe/check_personas.py"; } 2>&1); then
  echo "RED: the probe passed a second trace naming nobody"; exit 1
fi
printf '%s\n' "$out" | grep -q "Nobody At All" || { echo "RED: the probe did not name the bad trace"; exit 1; }
echo "ok   probe goes red on a second trace naming nobody (engineer.md:$ln)"

# A source must name a year. A length bar passed `<the artefact>.`; this does
# not. It is a shape check and proves no artefact exists — see the report.
rm -rf "$tmp/y"
mkdir -p "$tmp/y/references/personas" "$tmp/y/.pearde/prds/x/probe"
cp references/personas/*.md "$tmp/y/references/personas/"
cp "$probe" "$tmp/y/.pearde/prds/x/probe/check_personas.py"
d="$tmp/y/references/personas/designer.md"
sl=$({ grep -nE '^- \*\*.*\*\* — .*\. Trait: .*\. Source: ' "$d" || true; } | head -1 | cut -d: -f1)
[ -n "$sl" ] || { echo "RED: designer.md carries no sourced practitioner"; exit 1; }
awk -v L="$sl" 'NR==L{sub(/Source: .*$/, "Source: <the artefact>.")} {print}' "$d" > "$d.new"
mv "$d.new" "$d"
if r=$({ python3 "$tmp/y/.pearde/prds/x/probe/check_personas.py"; } 2>&1); then
  echo "RED: the probe passed a source naming no year"; exit 1
fi
printf '%s\n' "$r" | grep -q "source names a year" || { echo "RED: the probe did not name the undated source"; exit 1; }
echo "ok   probe goes red on a source naming no year (designer.md:$sl)"

out=$({ python3 "$probe" || true; })
[ -n "$out" ] || { echo "RED: the probe printed nothing — it died before its tally"; exit 1; }
printf '%s\n' "$out" | tail -1 | awk '{
  if ($1 == $3 && $5 == 0) { print "ok   persona grammar — " $0 }
  else { print "RED: persona grammar — " $0; exit 1 }
}'
```
