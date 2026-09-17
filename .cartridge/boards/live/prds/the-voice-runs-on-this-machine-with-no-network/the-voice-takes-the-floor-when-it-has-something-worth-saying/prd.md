---
state: open
origin: requested
priority: 84
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/local.rs", "src/turn.rs", "src/service.rs"]
needs: ["the-user-can-cut-the-voice-off-mid-sentence"]
---

# The voice takes the floor when it has something worth saying

## Outcome

Listening is not silence. While the user speaks, the partial transcript keeps
reaching a fast local model with one question: is there a reason to speak now?
Two reasons count — the user is working from a premise the record contradicts,
and the work cannot start until a question is answered. Everything else waits
for the turn to end.

When it does decide, it comes in the way a person does: a short line, at a pause
in the user's speech rather than over the middle of a word, and it yields
immediately if the user keeps going. Nothing about this is a timer; a persona
sets how readily it claims the floor, and the default is reluctant.

This is the half of full duplex the user asked for and the barge-in child does
not cover: there the user interrupts the voice, here the voice interrupts the
user. Both need the same duplex capture and echo cancellation, which is why this
child follows that one.

## Acceptance

- [ ] While the user speaks, partial transcripts reach the floor-claim check, and the check runs without delaying transcription.
- [ ] A spoken statement that contradicts something the record says produces a claim; an ordinary statement of the same length does not.
- [ ] A claim is spoken at a pause in the user's speech, never on top of a word, and stops within a documented time if the user continues.
- [ ] The persona's floor-claim dial changes the rate: at its lowest the voice never claims, at its highest it claims on both reasons, and the record shows the difference over the same fixture conversation.
- [ ] Claims are recorded in the conversation like any other turn, marked as unprompted.
