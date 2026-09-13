# Bounded writer repairs

These are checks within this writer leaf, not substitute completion claims.
The PRD remains unfinished while its required quality gate fails.

- [ ] Preserve every unique fact and answer to frozen retrieval questions. The
  first Granite candidate omitted distinct-ID limits/provenance in v03, nearly
  all import facts in v06 runs 1/2, diagnostic/unknown author in v09, and the
  configuration names in v12. Candidate 2 still omitted facts and incorrectly
  described eligibility as deletion in v11. Recheck every output after tuning;
  do not drop fixtures or accept an unsupported inference.
- [ ] Preserve exact literals and executable memo structure. Both Granite
  variants dropped p02 frontmatter; candidate 2 reduced it to a code block.
  The first local gpt-oss candidate also changed spaces/hyphens in identifiers.
  Require exact protected-string and parser checks on every repeat.
- [ ] Do not expand already concise inputs. Granite c02 gained headings and
  c04 expanded or lost provenance. Require source-length and meaning checks;
  exact copying is preferred.
- [ ] Meet the verbose target without losing meaning, or identify irreducible
  facts transparently. Granite candidate 1 aggregate median ratio was 0.941;
  candidate 2 was 0.740. Neither passed the target of 0.5. Per-repeat results
  and mechanical failures are in evaluation/candidate-audit.json and
  evaluation/candidate-2-audit.json. Full semantic rubric scoring was not
  completed for those already-failing variants; no qualification is claimed.

The alternate installed local model has its own paired baseline and exactly
pinned settings. Tuning keeps the same frozen fixtures and questions. A model
that fails is not qualified by a different model passing.
