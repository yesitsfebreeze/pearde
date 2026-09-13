# Frozen baseline — 2026-09-13

The 20-case corpus and existing register/unslop instructions were committed in
`aad13b8` before candidate guidance. The installed local granite4:3b model ran
all 20 cases with seeds 11, 29 and 47. Requests, native completion-token counts,
model/tokenizer digest and complete responses are in evaluation/runs/baseline.

The first run already demonstrates missing meaning: v03 omits the distinct-ID
boundary and test reference; v06 omits successful/durable counts; v12 omits
configuration names, verification and production uncertainty. c03 drops the
instruction to preserve uncommitted changes. v10 invents an incorrect reverse
Tab order. Memos often add repetitive labels and headings. These are observations
of this model and exact prompt, not general claims about the register.

Candidate scoring must preserve every frozen fact even where the baseline failed.
The baseline's short but incomplete replies make the 50% median target harder;
no shortening score can excuse missing facts. Keep all failed outputs and record
bounded repairs if the frozen gate fails.
