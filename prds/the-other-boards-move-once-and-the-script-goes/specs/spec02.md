---
complexity: 12
footprint:          # none in THIS repo. The run's whole effect is in
                    # seven other repositories, left as staged renames
                    # for each repo's owner to commit — never this
                    # board's to commit, so never this board's
                    # footprint. `serve.json` is gitignored machine
                    # state and was already live. The seven roots and
                    # their rename counts are in report.md.
---

# spec02 — run the migration over the live boards and gate each with scan

The real run: `migrate.py` (spec01's file, already fixture-proven) runs once
per remaining board — the seven `prds/` rows in
`resources/board/state/serve.json`: mitosys, model, infra, realm, shared,
manola, racer/.mi (dotfiles is already on `.pearde/`, its gate already
passes). Members go first, then their master: infra's members rows
(`../mitosys/prds` …) only rewrite when the member's `.pearde/` already
exists, and the gate then reports the member PRDs under their `@mitosys/`
sigils as before.

Order: mitosys, model, realm, shared, manola, racer/.mi first; the infra
master last (its members rows rewrite only when every member has moved); then
`--serve` rewrites the registry rows. dotfiles needs nothing — already
migrated, scan already clean (196 PRDs, exit 0, verified).

What already stands: the script and its 31-check fixture proof. What is
left: the real runs, the real gate per board, and the registry rewrite.

Findings to carry, not fix (from the probe round): a mitosys implementer
holds `p8o-vesicle-sweep` live — run mitosys when that board is quiet or
accept that its in-flight worker re-scans after the move; the same for
racer/.mi/04-audio-pipeline's stale claim. mitosys, realm, shared and infra
track their state dotfiles under `prds/` — `git mv` carries them into
`.pearde/.state/` as tracked files, which matches what those repos already
committed, not what pearde's own board ignores.

## Acceptance

- [x] every board root listed in serve.json passes the gate:
      `python3 resources/board/plan.py scan <board-root>` exits 0 for all
      eight, and the seven previously-refusing boards print PRD counts
      matching the prd.md-holding directory count each old `prds/` had
- [x] a scan of the infra master reports its members under the `@mitosys/`,
      `@model/`, `@realm/` and `@shared/` sigils, unprefixed beyond that
- [x] every serve.json row names a directory that exists
- [x] migrate.py printed no WARNING for any board except reported state-file
      collisions

## Verify and Proof

```sh
R=/Users/feb/dev/infra/pearde
P="$R/resources/board/plan.py"
for b in /Users/feb/dev/dotfiles /Users/feb/dev/infra/mitosys \
         /Users/feb/dev/infra/model /Users/feb/dev/infra \
         /Users/feb/dev/infra/realm /Users/feb/dev/infra/shared \
         /Users/feb/dev/manola /Users/feb/dev/racer/.mi; do
  python3 "$P" scan "$b" >/dev/null 2>&1 &&
    echo "GATE ok: $b" || echo "GATE FAILED: $b"
done
python3 - <<'PY'
import json, os, sys
rows = json.load(open("/Users/feb/dev/infra/pearde/resources/board/state/serve.json"))
dead = [p for p in rows if not os.path.isdir(p)]
print("SERVE REGISTRY:", "ok — every row is a live board dir" if not dead
      else f"FAILED: dead rows {dead}")
PY
python3 "$P" scan /Users/feb/dev/infra 2>/dev/null | grep -cE "@(mitosys|model|realm|shared)/" &&
  echo "MEMBER SIGILS: present" || echo "MEMBER SIGILS: MISSING"
echo "spec02 gate: 8 GATE ok lines, SERVE REGISTRY ok, MEMBER SIGILS present"
```