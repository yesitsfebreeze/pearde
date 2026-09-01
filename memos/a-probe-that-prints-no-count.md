---
memo: a-probe-that-prints-no-count
kind: decision
status: decided
subject: the seven-closed-probes container's run-all.sh prints pass=0 fail=0 on every row and empty FAIL excerpts, so only its exit code carries information
date: 2026-09-01
prds:
  - seven-closed-probes-drifted-red
---

# a-probe-that-prints-no-count — every row reads zero, and the sweep reads fine

## Decision

`prds/seven-closed-probes-drifted-red/probe/run-all.sh` uses `printf "" "$out"`
where it means `printf '%s\n' "$out"`, twice. Every row it prints reads
`pass=0 fail=0` and every `FAIL` excerpt is empty.

**Read that file's exit code and nothing else.** Any number quoted from its
rows is zero because the format string ate it, not because the harness found
nothing — and a reader who does not know that will read a passing sweep as an
empty one, or an empty one as passing.

## Why

`printf` takes its first argument as the format. An empty format consumes the
operand and emits nothing, and it does not fail: `printf "" "$out"` exits 0
having printed no bytes. So the bug is invisible in every way a shell script
usually announces itself — no error, no non-zero exit, no missing file. The
only symptom is a column of zeroes that looks like a harness which ran and
found nothing.

Three separate workers hit this on 2026-09-01 and each independently worked
around it by reading exit codes, which is the correct response and also the
reason it survived: a defect everyone routes around is a defect nobody fixes.
It cost three rounds a paragraph of explanation apiece, and it will cost the
next one the same until it is either fixed or written down. This is the written
down.

The container closed `done` at `752af7a` with the bug still in it. That is
deliberate: the container's own contract is "every child done", which is a
state check the tool makes, not something `run-all.sh` measures. Nothing about
the parent's verdict depended on the rows.

Under @references/parts/derived.md rule 2 this is a memo, not a PRD: fixing it
changes nothing about what ships, only whether the board can read its own
sweep.

## Alternatives considered

**Fix the two `printf` calls in the same round** — a two-character change with
an obvious right answer, and genuinely tempting. It lost because the container
was mid-collect and the file is inside its footprint: an orchestrator editing a
PRD's own probe while closing it makes the record of what that PRD's worker
built unreadable. It is the first thing to do in the next round that legitimately
opens that directory.

**File it as a derived PRD** — it lost on rule 2 and on proportion. A PRD whose
entire deliverable is a format string is the shape `derived.md` names as the
loop feeding on itself, and the board already carries 19 derived against 64
requested.

**Leave it to the workers who keep routing around it** — what happened three
times today. It lost because the workaround is invisible to the next worker:
each one rediscovers the zeroes, spends a paragraph establishing they are
meaningless, and writes it in a report nobody downstream reads.

## Consequences

- The container is `done` with a probe that cannot report. Anyone re-running
  that sweep for evidence about the seven closed probes gets a wall of zeroes
  and has to come here to learn why.
- It deliberately does not fix the file, and it does not audit the other
  harnesses for the same spelling. `printf` with a variable or empty format is
  a whole family of silent bugs and only this one instance has been looked at.
- It says nothing about the wider defect it sits next to: `doctor --harnesses`
  (`resources/doctor.sh:722`) launches all 47 harnesses at once with no job cap,
  so counts from the sweep are decided partly by scheduling. That one has its
  own memo — `a-check-decided-by-scheduling.md`.
