---
state: open
origin: requested
priority: 0
complexity: 0
blast-radius:
needs:
  - the-capability-registry
---
---

# The fire check

*Source: `docs/content/docs/improvements/integration-skill-fire.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Layer:** index · **Tool:** skills + doctor · **Unblocked by:**
[the registry](/docs/improvements/integration-registry)

## Why now

A skill is found by its `name:` and fires on its `description:` — the one
line deciding whether the machine's capability is ever reached. Doctor
checks the frontmatter parses and the name agrees with the file; it cannot
check the *description*, because "would this fire?" has no oracle. The
result: a skill whose description undersells its moment is silently dead —
the model reads it mid-loop, declines, and the failure reads exactly like a
judgment call. The reference says this in one sentence ("a skill that
silently never fires, which reads exactly like a model choosing not to use
the skill") and then stops.

## The change

A probe corpus, one line per skill: the *moment* the skill should fire,
written as the request a user or a pass would actually produce ("I keep
losing track of what's next across sessions", "is there a record of why we
dropped time as an axis"). `pearde doctor --skills-probe` runs the corpus
through the same surface the agent reads skills from and reports per skill:
fired / declined / never seen. It is a harness, not a model call in the
loop — run on demand, by a person, the way the drill probes are run. The
corpus lives beside the skill; the skill's own file gains one frontmatter
key, `fires-on:`, naming its probe line.

## Done when

- Every skill file carries `fires-on:`, and the probe reports each skill
  fired for its own moment — the check is the doctor row's `ok` only when
  the probe went round.
- A description deliberately weakened (one verb's description stripped of
  its trigger words) reads `declined` on its probe — the check can fail,
  which is what makes the pass meaningful.
- The corpus rows live in the skills themselves, so a skill move carries
  its probe (every file finds its siblings by one rule).

## Fails when

- The probe becomes a model-cost sink — 20 skills × 20 moments per doctor
  run is a spend. Guard: the probe is **not** part of `doctor.sh`'s default
  report; it is an opt-in harness like `--harnesses`, run when a skill
  changes, one call per skill, not per moment.

## What stays out

No auto-rewrite of descriptions — the probe names the decline, and the
author decides. A description that survives its probe is the contract;
rewriting it by machine would remove the only check that the words still
mean the moment.
