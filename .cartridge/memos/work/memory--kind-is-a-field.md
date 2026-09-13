---
kind: work
level: 10
status: done
description: kind moves off the session:// source title onto the entity, and the format version byte moves with it
read_when: "executing the fold"
---

# kind-is-a-field

From [[@prd/work/memory--fold-parts-into-the-graph.md]]. Needs
[[@prd/work/memory--node-source-reads-frontmatter.md]] to have a producer for the field.

## Do
End the kind-in-the-title convention. Add `kind` to the persisted entity, fill
it from the `kind` [[@prd/work/memory--node-source-reads-frontmatter.md]] already reads and
discards, and replace the four sites that parse
`session://<kind>` out of `Source::Session.title` with a field read. Move the
format version byte in the same change — `format-version` makes the
checksum test fail the build until it does. `report --group claim_kind` reads
the field.

## Check
`just build && just check && just test` green, including the format-version
checksum test. `memory report --group claim_kind` returns the same labels for
the same store as before the change, and `grep -rn 'session://' src/` shows
no parse of a kind out of a title.

Landed 2026-09-05. `Entity.claim_kind` is the field, appended after
`session_id`; `Job` and `DirectJob` carry it from the producer that knows it —
the distiller's claim kind, a part's front-matter `kind` on both file legs —
and `place_document` puts it on the entity beside `review` and `valid_from`.
The three readers (`heat::decayed_for`, the query filter, `report --group
claim_kind`) read the field; `claim_kind_label` and `report_claim_kind_label`
are gone and the intake writes an empty Session title. FORMAT_VERSION moved
11 to 12: `legacy.rs` freezes v11 (v10 leaves with it — one hop is the whole
promise) and recovers the label from the old `session://<kind>` title on the
way forward, which is the one remaining parse of that convention and the only
one that may exist. `just build && just check && just test` green, both layout
checksums repinned. Measured at the close: the same store read by the new
binary answers `report --group claim_kind` with the same ten labels and counts
the running v11 daemon gives, and `memory doctor` names the v11-to-v12 read.

