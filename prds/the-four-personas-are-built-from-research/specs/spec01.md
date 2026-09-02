---
complexity: 14
footprint:
  - references/personas/designer.md
  - references/personas/mentor.md
  - references/personas/skeptic.md
---

# spec01 — designer, mentor and skeptic are sourced composites

The three personas that carried no provenance become research-backed
composites, in the file format of `@references/personas/INDEX.md`. Each names
its practitioners under `## Built from`, and every `## How you work` bullet
closes with the trait it was taken from, repeated character for character.
`engineer` already stood this way and is untouched.

**What already stands.** All three files are written and pass the probe. The
practitioners were researched by dispatched workers and every source was
verified to exist: designer holds seven (Cooper, Krug, Schoger, Fried, Hurff,
Covert, Nielsen), mentor six (Naur, Metz, Wilson, Hunt, Reilly, Fournier),
skeptic seven (Hendrickson, Miller, Yuan, Bloch, Maguire, Winters, Zeller).
Ids, names, professions, `## Voice` and the behaviours themselves are as the
2026-09-02 rewrite left them — only the opening line and the traces are new.

**What is left.** Read the three files, confirm no behaviour was altered to fit
a citation, and run the verify below. The block is hermetic: no command's exit
in it is decided by a file outside the footprint. `engineer.md`, `INDEX.md` and
`references/files.md` all sit under live sibling sessions, so the probe is run
against a fixture holding the three footprint files plus block-authored stubs
of the first two, and the third is not read at all. Per
`@.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`.

## Acceptance

- [x] `references/personas/designer.md`, `mentor.md` and `skeptic.md` each hold exactly one `## Built from`
- [x] each `## Built from` holds at least three bullets in the shape `- **<Name>** — <known for>. Trait: <trait>. Source: <artefact>.`
- [x] every `## How you work` bullet in the three files closes with `[<Name>: <trait>]`, the name under `## Built from` and the trait identical to the one recorded there
- [x] no practitioner under `## Built from` backs zero bullets
- [x] the first line of each of the three bodies contains the word `composite`
- [x] no gendered third-person pronoun appears in any of the three bodies
- [x] no `python3 resources/index.py check` line names one of the three footprint files
- [x] the probe goes red and names the break when a trace is broken in a fixture copy of each of the three files
- [x] the probe run backing this spec is hermetic — it reads the three footprint files and block-authored stubs, and prints a non-empty tally

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# Hermetic by construction. No command's exit below is decided by a file
# outside this spec's footprint: `references/personas/engineer.md`,
# `references/personas/INDEX.md` and `references/files.md` are all under live
# sibling sessions, so the probe is never run over the tree — it runs over a
# fixture built here from the three footprint files plus stubs this block
# writes, and `references/files.md` is not read at all. A repo-wide command
# may be printed; it may not decide the colour.
# .pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md

FEET="references/personas/designer.md references/personas/mentor.md references/personas/skeptic.md"
probe=.pearde/prds/the-four-personas-are-built-from-research/probe/check_personas.py

for f in $FEET; do
  n=$({ grep -c '^## Built from' "$f" || true; })
  [ "$n" = 1 ] || { echo "RED: $f holds $n '## Built from'"; exit 1; }
  b=$({ grep -c '^- \*\*.*\*\* — .*\. Trait: .*\. Source: .*\.$' "$f" || true; })
  [ "$b" -ge 3 ] || { echo "RED: $f holds $b practitioners"; exit 1; }
  y=$({ grep -o 'Source: .*' "$f" | grep -cvE '(19|20)[0-9]{2}' || true; })
  [ "$y" = 0 ] || { echo "RED: $f has $y source(s) naming no year"; exit 1; }
  first=$(awk '/^---$/{d++; next} d>=2 && NF {print; exit}' "$f")
  case "$first" in
    *composite*) ;;
    *) echo "RED: $f — first body line does not say composite: $first"; exit 1 ;;
  esac
  echo "ok   $f — one '## Built from', $b sourced practitioners, all dated, first line says composite"
done

# The map, printed and never gated on. Only a line naming a footprint file may
# redden this spec; a neighbour's unmapped file is somebody else's row.
idx=$({ python3 resources/index.py check 2>&1 || true; })
printf 'index.py check said: %s\n' "${idx:-(silent)}"
drift=$({ printf '%s\n' "$idx" | grep -E 'references/personas/(designer|mentor|skeptic)\.md' || true; })
[ -z "$drift" ] || { echo "RED: the map is drifted on a footprint file: $drift"; exit 1; }
echo "ok   index.py check names no footprint file"

# The fixture. Only the three footprint files come from the tree.
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/base/references/personas" "$tmp/base/.pearde/prds/x/probe"
cp $FEET "$tmp/base/references/personas/"
cp "$probe" "$tmp/base/.pearde/prds/x/probe/check_personas.py"
# The stubs' headings are written `@@ ` and raised to `## ` by sed: the spec
# reader that finds this block is line-based and fence-blind, so a literal
# `## ` at the start of a line in here would end the section before the fence.
sed 's/^@@ /## /' > "$tmp/base/references/personas/engineer.md" <<'STUB'
---
name: Fixture Engineer
profession: fixture
description: A stub this block writes, so no sibling decides this spec.
---

A composite stub standing in for a persona outside this spec's footprint.

@@ How you work

- **One.** A behaviour. [A Name: a trait]
- **Two.** A behaviour. [B Name: b trait]
- **Three.** A behaviour. [C Name: c trait]

@@ Voice

Flat. This file is a fixture and is read by nothing else.

@@ Built from

- **A Name** — a practitioner. Trait: a trait. Source: *A Book* (1999).
- **B Name** — a practitioner. Trait: b trait. Source: *B Book* (1999).
- **C Name** — a practitioner. Trait: c trait. Source: *C Book* (1999).
STUB
cat > "$tmp/base/references/personas/INDEX.md" <<'STUB'
# Fixture roster

A stub. The roster is `engineer`, `designer`, `mentor` and `skeptic`, and
every file carries a Built from section.
STUB

cp -R "$tmp/base" "$tmp/t"
out=$({ python3 "$tmp/t/.pearde/prds/x/probe/check_personas.py" || true; })
[ -n "$out" ] || { echo "RED: the probe printed nothing on the fixture — it died before its tally"; exit 1; }
for f in designer mentor skeptic; do
  printf '%s\n' "$out" | grep -q "^ok   $f: every practitioner backs a bullet" \
    || { echo "RED: $f — the probe reports no green orphan row"; exit 1; }
done

# A tally over this spec's own rows, computed here and never pinned to a
# literal: a check added anywhere else cannot move it.
printf '%s\n' "$out" | awk '
  /^(ok  |FAIL) (designer|mentor|skeptic):/ { n++; if ($1 == "ok") p++ }
  END { printf "%d checks, %d pass, %d fail — designer, mentor, skeptic\n", n, p, n - p
        if (n > 0 && n == p) print "ok   the three footprint personas are green"
        else { print "RED: a footprint persona row failed"; exit 1 } }'

# The flip, one per footprint file — a flip probe runs every file it certifies.
for f in designer mentor skeptic; do
  rm -rf "$tmp/t"
  cp -R "$tmp/base" "$tmp/t"
  g="$tmp/t/references/personas/$f.md"
  who=$(grep -Eo '^ +\[[^]:]+:' "$g" | head -1 | sed -e 's/^ *\[//' -e 's/:$//')
  [ -n "$who" ] || { echo "RED: $f carries no trace to break"; exit 1; }
  sed "s/\[$who:/[Nobody At All:/" "$g" > "$g.new"
  mv "$g.new" "$g"
  if r=$({ python3 "$tmp/t/.pearde/prds/x/probe/check_personas.py"; } 2>&1); then
    echo "RED: $f — the probe passed a trace naming nobody"; exit 1
  fi
  printf '%s\n' "$r" | grep -q "^FAIL $f: 'Nobody At All' is under Built from" \
    || { echo "RED: $f — the probe did not name the broken trace"; exit 1; }
  echo "ok   $f — the probe goes red on a trace naming nobody (was [$who: …])"
done
```
