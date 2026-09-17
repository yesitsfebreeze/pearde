---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: [".cartridge/bench", ".cartridge/tests", "justfile"]
needs: ["live-speaks-and-listens-through-local-sidecars"]
---

# The local voice pipeline is measured on this machine

## Outcome

The pipeline reports its own timing instead of being argued about. Every turn
logs one clock: speech start and end, the turn decision and its confidence,
transcript final, first token, first audio, playback start, and any
interruption with the milliseconds actually played. A bench target replays
fixture audio through the pipeline and prints the per-stage table plus the
end-to-end distribution.

The numbers that matter are the median and the ninety-fifth percentile from the
end of a turn to the first sound, the false-interrupt count, and the count of
turns committed while the speaker was still talking.

## Acceptance

- [ ] `just bench live` replays fixtures and prints per-stage and end-to-end timings.
- [ ] A conversation writes the per-turn timing record to a documented path.
- [ ] The bench reports median and p95 first-sound latency over at least twenty turns.
