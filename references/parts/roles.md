# Roles

The role is the job; the persona is who holds it —
@references/personas/INDEX.md.

| role             | does                                                        |
|------------------|--------------------------------------------------------------|
| **orchestrator** | works the board. The ONLY writer of PRD state — nothing to race, so no locking. One per board; on a master board it owns every member it merges |
| **analyst**      | turns one `open` PRD into specs, a split, or questions       |
| **implementer**  | turns one `specced` PRD's specs into verified code           |
| **consultant**   | a persona the orchestrator calls mid-pass and talks to. Reads the session and the board, answers, writes nothing |

Workers do the work; the orchestrator moves the states. A consultant does
neither — called, it answers, and the exchange stays open until the question
is settled, @references/parts/consult.md.
