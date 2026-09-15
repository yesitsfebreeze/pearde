---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `AuditCandidate.preview` is the first 80 characters of the thought and its doc comment names that cap as what stops a flagged credential being re-leaked — but every built-in secret pattern matches well inside 80 characters

## Do

`audit_noise` (`src/graph/src/graph_ops.rs:387`) builds each candidate's
preview as `text.chars().take(80).collect()`, and the struct's doc comment
(`:344-346`) states the intent:

> `preview` is capped at 80 chars — the report names noise, it does not reprint
> it (a flagged secret must not be re-leaked by the audit that found it).

The cap does not do that. Measured against the ten patterns in
`SECRET_PATTERNS` (`src/hygiene/src/hygiene.rs:13-38`), every one of them
matches a span shorter than 80 characters — an AWS key is `AKIA` plus 16, a
GitHub token a four-character prefix plus 36, a Google key `AIza` plus 35, a
private-key block a 31-character header, and `secret_assignment` needs only a
keyword, a separator and eight characters. A thought that begins with a
credential is reprinted in full by the report that flagged it, in the same
JSON object whose `secrets` field was designed to name it without showing it.

The reach is not local. `audit` is on the MCP tool surface, so an agent asking
for the audit receives the previews — and the shipped reasoning default already
sends text off the machine
([[the-default-model-sends-every-distill-off-the-machine]]).

Redact instead of truncating: when `scored.secrets` is non-empty, replace the
matched spans (or drop the preview to the empty string) before the candidate is
built. The labels already carry everything a caller needs to act.

Measured on this store 2026-09-06, `memory audit --json --min-score 0.0`: 11,485
thoughts scanned, 7 rows flagged — labels `aws_access_key`, `github_token`,
`secret_assignment` — and in all 7 the matched span falls beyond the first 80
characters, so nothing is currently reprinted. That was checked by testing the
previews against the patterns, not by reading them, and it is a property of
those seven rows rather than of the cap.

**Done 2026-09-06.** `hygiene::redact_secrets` sits beside the patterns it
uses — the labels and the redaction are one thing, and putting the replacement
anywhere else would be a second copy of the pattern list. `audit_noise` calls it
*before* truncating, with the reason in the comment: truncation cannot know
where a match falls.

The doc comment that made the false claim is rewritten rather than deleted. It
now says the preview is redacted and then capped, and that the cap alone never
achieved what it was named for — an edit that adds, so the next reader learns
the cap was believed to be the guard.

Held by `a_flagged_secret_is_named_in_the_report_and_absent_from_its_preview`
(`src/graph/src/tests/graph_ops_test.rs`): four synthetic credentials of
distinct pattern shapes, each at the very start of the text where truncation
cannot help. It asserts the label is carried, and — the part that matters — that
`detect_secrets(&preview)` is **empty** rather than that the preview differs
from the original. Checking for a substring would pass on a preview leaking a
prefix; checking the pattern is the same question the flag asked.

## Acceptance
A thought whose first characters are a synthetic credential of each pattern's
shape is flagged with its label and its `preview` contains no match for the
pattern that flagged it. `just check` green. Both hold; the suite reads 1,245
passed.
