---
state: open
origin: requested
priority: 95
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: []
---

# The voice runs on this machine with no network

## Outcome

A conversation with this composition feels like talking to a coworker who knows
the project. It runs on this machine: the microphone, the transcript, the reply,
the speech and the delegation to the local agent stay inside the host, with no
voice session bought from anyone and no API key on the conversational path.

Both people may interrupt. The user can cut the voice off mid-sentence and it
stops and listens. The voice may also take the floor while the user is still
talking, when it has a reason — a wrong premise, a question it must ask before
the work can start — and it does so at a rate the persona sets, not constantly.

"On this machine" governs the models, not the agent's reach: when an answer is
not in the repository the delegated agent may look it up on the internet, and
the voice says so while it waits.

Nothing in the path may be specific to this operating system. Every model runs
through a runtime that exists on macOS, Linux and Windows — `whisper.cpp` for
speech to text, ONNX Runtime for voice activity, end of turn and speech — so
the cartridge that works here works wherever the composition is installed.

Measured on this machine (Apple M5, 32 GB, macOS 26.2) before this work began:
Apple `SpeechTranscriber` transcribes 6.87 s of English in 1.05 s with streaming
partials; Kokoro-82M through `mlx-audio` returns first audio for a clause in
0.119 s; a warm 3 B model answers its first token in 25–47 ms. The budget those
numbers imply, from the end of a spoken turn to the first sound of the reply, is
under 700 ms.

## Acceptance

- [ ] Every child is done.
- [ ] A conversation held with `provider: "local"` covers, in one session: a spoken question answered from the repository, an interruption by the user that stops the voice mid-sentence, a floor claim by the voice against a wrong premise, and an answer that required the internet.
- [ ] No request leaves this machine on the conversational path; only the delegated agent's own lookups do.
