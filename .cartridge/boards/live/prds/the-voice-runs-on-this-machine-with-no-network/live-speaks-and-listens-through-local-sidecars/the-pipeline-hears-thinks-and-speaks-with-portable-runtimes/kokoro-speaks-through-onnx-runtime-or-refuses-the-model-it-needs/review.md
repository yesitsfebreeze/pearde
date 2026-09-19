# Kokoro executable plan review history

Canonical scope: this Kokoro leaf. Five rounds are available, with independent
agent scores of at least 90 and no blocking findings required. No review has yet
been performed for this leaf. The sidecar ancestor exhausted five rounds, then
the user explicitly granted fresh child rounds in its Answer dated 2026-09-17
for the cross-platform Rust implementation. The pipeline split happened before
review; the delivered transport seam sibling records that it inherited no
rounds. That sibling's subsequent four rounds do not belong to this leaf.
The analyst report documents this provenance and the actual real-model probe.
No implementation, acceptance or collection is implied by the draft.


# Kokoro independent plan review — round 1

Reviewer: `/root/kokoro_reviewer`, independent of the analyst and future implementation.
Verdict: **FAIL, 87/100**, with two related blocking findings about bounded admission and close priority. This is a plan review, not a rejection of the demonstrated model choice. One round is now used and four remain, subject to coordinator recording. No user rating was requested or invented.

Canonical plan: `@live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/the-pipeline-hears-thinks-and-speaks-with-portable-runtimes/kokoro-speaks-through-onnx-runtime-or-refuses-the-model-it-needs`.
Source HEAD: `520888674a8d05ae435ef2f072b4d8e48812e312`, clean before review. The existing eight-path footprint suffices for the requested revisions; no service or transport ownership expansion is required.

## Score

| Dimension | Score / 20 | Evidence and deduction |
| --- | ---: | --- |
| Current user value and scope | 19 | Actual local English synthesis and the inherited greeting/delegated-result path are both retained. Whisper, turn detection, voice choice and measured pipeline latency stay with their owners. The fixed English fallback limitation is honestly documented. |
| Ownership and reuse | 19 | Reuses Source, Transport, the existing event callback and service buffering. A separate Kokoro module owns assets, tensor preparation and inference. No sibling private dependency or platform speech subprocess is introduced. |
| Dependencies and implementable slices | 18 | The delivered seam and fresh allowance are verified from their canonical records. The pinned Rust probe runs successfully. The worker boundary is feasible, but upstream admission and close signaling are not specified enough to implement its promised lifecycle reliably. |
| Observable acceptance and baseline evidence | 17 | Ten named new tests, explicit mandatory real-fixture tests, and full compatibility coverage are meaningful. Fixture hashes and the real Rust synthesis were independently verified. Missing adversarial admission/close tests leave B1 and B2 unproved; corrupt model shape and unsupported-text cases should be named cases within the existing tests. |
| Failure, recovery and compatibility | 14 | Missing/corrupt asset preflight, one error then closed, HTTP compatibility, silent context, and joined worker failure handling are strong. A bounded inference channel does not bound the current unbounded session input or one arbitrarily large utterance. FIFO close can wait behind additional queued synthesis, contrary to the stated cleanup boundary. |
| Total | 87 / 100 | Two blocking findings remain. |

## B1 — Bound admission and one utterance, not only the worker channel

Blocking. Implementation step 4 bounds the inner single-request worker, while step 6 adds queued client events without defining admission limits. The actual `local.rs` uses `mpsc::UnboundedSender<Msg>` and `mpsc::unbounded_channel`; `Session::audio` copies caller buffers before queueing. The turn loop awaits STT, assessment, brain and speech serially. Its brain response uses unrestricted `response.json()`, and the proposed speaker phonemizes an entire String, creates all token chunks, then may accumulate one combined PCM vector. A 510-token limit per chunk does not bound the number of chunks or bytes allocated for one response. The 32 KiB silent-context limit only applies after events are processed, not to queued events or generated speech.

This is a reachable design gap under ordinary slow inference: new commentary events and microphone batches arrive while the one consumer waits. Moving those strings through a capacity-one worker does not limit the upstream retained work. The existing audio queue is baseline debt, but the new commentary and expensive real synthesis must have an explicit admission contract rather than assuming that the inner channel solves it.

Revise the plan to specify concrete byte/item limits at the new text/control admission boundary and before phonemization, plus a bounded generated speech/PCM policy. Reject oversized speech with a readable error rather than silently truncating it or losing tokens. Define what happens to audio/control ingress during a busy synthesis: a bounded queue with a terminal overload error, or another explicit bounded policy preserving the intended behavior. Limit brain response consumption before deserializing an arbitrarily large body; model output accumulation needs a concrete cap too. These can be internal constants within the current footprint. Do not synchronously invoke the service callback from `Session::send` on overflow, because service callers can hold their live-map lock; route terminal signaling through the session task.

Add a named deterministic test that holds the inference fixture, floods admission beyond its stated limits, and proves bounded accepted work plus the documented error/close behavior. Include oversized UTF-8 commentary and brain text, and prove no additional phonemization or inference begins for a rejected request. Include it in Verify. This is a behavioral boundary, not a test-framework gate-design exercise.

## B2 — Close must bypass queued speech and terminate the worker lifecycle

Blocking. Step 4 says closing the session closes the worker input and reaps it once current inference ends. The actual Session::close instead sends `Msg::Close` to the tail of the same FIFO. If a current synthesis has pending commentary or committed audio behind it, a direct extension of the existing loop executes that work before observing Close. Dropping one cloned handle does not close the channel either. The proposed lifecycle test mentions load count and Drop, but not this interleaving. It can therefore pass while a user ends a call and the task continues running queued speech.

Specify a separate close/cancellation signal or equivalent priority mechanism, observable while the task is busy, and stop accepting new work once it is set. Discard queued work on close; permit the currently executing native inference to finish if that remains the chosen policy, then close the worker input and join exactly once without starting another queued utterance. Check cancellation between long-text chunks. State whether the final current result is suppressed on close. Do not block an async runtime worker or the service mutex while joining.

Extend the lifecycle proof with a controlled in-flight inference, a second queued update, and a close request. Release the fixture and assert that the second update never invokes the brain/speaker, the state drops and the JoinHandle is reaped, and later sends cannot restart work. Also cover worker initialization failure and inference error with queued work, proving one terminal error/closed pair and no continued audio. This fits local.rs and local/kokoro.rs without changing service.rs.

## Non-blocking implementation notes

- The stated voice row `n - 1`, 510 content tokens, zero boundaries, f32 input shapes and fixed speed are consistent with the selected model and current upstream pipeline. Validate actual output name, dtype and dimensions; do not use only positional output zero in production because the disposable probe does.
- Misaki 0.6.0 without espeak has embedded lexicon/rules and character spelling fallback in its actual source. Ordinary English synthesis is feasible. Specify or test punctuation-only and unsupported-character-only input separately from an empty String: retained spaces or punctuation are not proof of speakable content. No multilingual or intelligibility measurement has been established here.
- The existing service commentary helper caps its own text but cannot bound the brain's generated reply or number of queued updates. It is not a substitute for B1.
- The Verify blocks obey lane/repository relative-cwd and isolated-target rules. Cargo and ORT build caches must actually be prepared before the engine's 120-second blocks. `--offline` constrains Cargo resolution; native ORT build preparation still needs its already-acquired cache. No model downloader is introduced by these blocks.
- Preserve the current full-library test as the GPT/service compatibility backstop, especially service buffering and missing-model status. The real Transport test is stronger than merely calling the Kokoro helper and must remain mandatory.

## Independently observed checks

1. `./task prompt` exited 0. ASP lookup eventually succeeded with `cartridge run asp` and an `op: search` payload; it returned no useful code location, so actual source reads followed. Two earlier syntax attempts exited 2 and 1; neither mutated state.
2. Read the canonical leaf PRD, spec and review; the full analyst report; seam acceptance and all four review rounds; predecessor analyst N4; the ancestor Answer dated 2026-09-17; current local.rs, transport.rs, relevant service.rs, manifest, dependencies and all three documentation surfaces; review-plan.md and the engine spec template.
3. `CARGO_TARGET_DIR=/tmp/cartridge-kokoro-analyst/target cargo run --offline --locked --manifest-path /tmp/cartridge-kokoro-analyst/probe/Cargo.toml` exited 0. Actual Misaki English text produced 37 content tokens. ORT exposed input_ids int64 [1,-1], style float32 [1,256], speed float32 [1]. It produced [1,61800] finite f32 samples with RMS 0.066915095. Model loading took 304.122208 ms; inference took 1.247023833 s on this invocation. These are observed probe times, not latency promises or a product-integration pass.
4. Recomputed all three fixture hashes; they exactly match the spec. No assets were downloaded during this review.
5. `CARGO_TARGET_DIR=/tmp/cartridge-kokoro-analyst/live-baseline cargo test --offline --locked --manifest-path live.ctg/Cargo.toml --lib` exited 0: 42 passed, 0 failed, 5.84 seconds. This is the current baseline, not tests of the unimplemented plan.
6. Inspected pinned local Misaki and ORT crate source. Independently opened the primary upstream pipeline at https://raw.githubusercontent.com/hexgrad/kokoro/main/kokoro/pipeline.py; its infer method selects pack[len(ps)-1] and its token path enforces the 510-phoneme limit. The pinned Hugging Face tokenizer fetch through the web tool failed internally; the already-acquired local tokenizer was read and hashed instead.
7. All reviewer-started commands are terminal. Probe handle 94126 exited 0; baseline handle 84729 exited 0. No source, PRD, spec, canonical review, state, acceptance checkbox or commit was changed. This report is the only repository write.

## Revision binding

All digests below are SHA-256. Paths are relative to the canonical leaf unless otherwise stated.

| Input | Digest |
| --- | --- |
| prd.md | 09910c498fb53fbc65533726324487117b7c12c771a93b1d6ffe866fd38fc4d5 |
| specs/spec01.md | 937c8a13de7ba8876763d6c1d7cd9f11ff282ce1c06b423c973153e9e24300d9 |
| review.md before this round | 13bac8f4b2acd745c462d7280ae77d7b74023d0a1bc1872f52ea8a2e9583519a |
| Analyst report | 121a02dae3e0c928ce45322af7130b76bdcb6a09ab18f919de9f0d33acbb83da |
| Sidecar ancestor prd.md including user Answer | 223d0e2173149abf162f684663c4aa6200de206f83d85403ebb3c4e081dc8171 |
| Pipeline parent prd.md | 7a6ea0aefc00050385279caf3d0412e0eb0e4cd667f23b1182cb1a5ee312d043 |
| Seam prd.md | 1e07329b9c4dfee1720e7536e93c184b7ad457ada4ac9df317d9164d3a0ef18a |
| Seam specs/spec01.md | b5cf09bcc308d43628629e3fca7aa5d19f18768e9006ab003eba653e0d9f1b15 |
| Seam review.md | 95964d7d89da1099a37a8296d126a38c56bf6de8912883403b430c02ef133c8a |
| prd.ctg/.cartridge/templates/spec.md | 0350746f33dde5398bf620c7982e5fe3c8163ff2e0c4879436631393704020ad |
| prd.ctg/.cartridge/workflows/review-plan.md | 1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9 |
| live.ctg/src/local.rs | 97f1ea18c90068a36faa1e6f89d35c996d4e70cba757938341b97d58716b0648 |
| live.ctg/src/service.rs | 9f5352d4e904b43c9477305e5b519fd9d32583c0e17c16972a235d2f4749e70a |
| live.ctg/src/transport.rs | c811cca8839eb115b832c33dabf7bdff9ac7e9c626fd34a4d351f8b4ca07dfc3 |
| live.ctg/Cargo.toml | be8a87f5bfbb9a29ae0b62d5f67f16cb8706e8c124152a09a53506dc8fcf940f |
| live.ctg/Cargo.lock | 6001fe4c015a3cc297c93d016cd31d7bcd14657f1b680a3d2637279b7384715a |
| live.ctg/cartridge.json | ca54bc9096dc2d5279547afd63bf6f9743878560899b8c4b1458417433791484 |

The user's ancestor Answer explicitly grants fresh cross-platform children rounds. The pipeline split preceded review; the seam subsequently spent four of its own rounds. This leaf had zero before this round. Nothing here resets the seam or any other exhausted plan.

Next action: make one coherent plan revision covering B1 and B2 and their named Verify tests, preserving the actual synthesis and commentary scope, then obtain fresh independent round 2 review.


## Coordinator record: round 2

Independent reviewer /root/kokoro_reviewer scored this revision FAIL 88/100. Two rounds are used and three remain. Input digests were checked before recording. The complete attributed report follows; B1 and B2 are resolved as design, B3 requires a focused revision.

# Kokoro independent plan review — round 2

Reviewer: `/root/kokoro_reviewer`, independent of the analyst and future implementation.
Verdict: **FAIL, 88/100**. Round 1 findings B1 and B2 are resolved as design contracts. One blocking consequence of the new admission policy remains: ordinary continuous quiet capture can exhaust the queue while a valid reply is being synthesized. Two rounds used, three remain after coordinator recording. No user rating was requested or invented.

Canonical plan: `@live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/the-pipeline-hears-thinks-and-speaks-with-portable-runtimes/kokoro-speaks-through-onnx-runtime-or-refuses-the-model-it-needs`.
Source HEAD remains clean at `520888674a8d05ae435ef2f072b4d8e48812e312`. The eight-path footprint is unchanged and sufficient. This review does not reopen the seam sibling's completed review or reset any round allowance.

## Score

| Dimension | Score / 20 | Evidence and deduction |
| --- | ---: | --- |
| Current user value and scope | 17 | Real Kokoro synthesis, real Transport proof and inherited commentary all remain. However, valid slow replies with the microphone still delivering silence can now close the session before speech is ready; B3 contradicts the ordinary voice path. |
| Ownership and reuse | 19 | Explicit local admission/control and Kokoro worker boundaries fit the current owner. The service lock boundary is correctly respected. No platform subprocess or new sibling dependency appears. |
| Dependencies and implementable slices | 18 | Required model APIs and assets remain demonstrated, waveform output is now named, and cancellation contracts are implementable. Busy audio ingestion needs one explicit stage-handling rule before implementation. |
| Observable acceptance and baseline evidence | 17 | Five new required tests cover saturation, input/output limits, prioritized close and real join completion. The quiet-pre-roll test does not require continuous capture while the consumer awaits a valid stage, so it can pass without detecting B3. |
| Failure, recovery and compatibility | 17 | B1 and B2 now cover active permits, first-terminal-wins, no inline callback, suppressed native results and joined cleanup. The chosen overflow behavior currently treats an ordinary inference delay plus silence as overload. |
| Total | 88 / 100 | One unresolved blocking finding: B3. |

## Findings resolved by this revision

**B1 is resolved as a boundedness design.** The actual outer ingress now has item and byte budgets including active work. Frame lengths are checked before copies, recognized text is bounded, silent context has a distinct limit, HTTP bodies are collected incrementally before parsing, token counts are capped before inference, and combined PCM is capped before accumulation/publication. Typed controls avoid arbitrary retained JSON. Full queues stop admission through task-owned terminal publication rather than callbacks under the caller's service lock. The native allocator limitation is stated accurately.

**B2 is resolved as a lifecycle design.** Close has an independent wakeable signal and wins over unreserved ordinary work/results. The specification states the stage/publication reservation boundary rather than claiming impossible preemption of an entered native call or callback. There is one outstanding native request, cancellation is checked between chunks, and logical close is distinguished from actual awaited JoinHandle completion. Client ownership excludes the task, so last-client drop has defined semantics. The new tests explicitly hold A, queue B, close, release A and inspect an actual completion receipt, including initialization/failure variants.

These are plan resolutions, not claims that code or new tests already exist. All real-synthesis and service/GPT compatibility requirements remain mandatory.

## B3 — Ordinary quiet capture must not exhaust ingress during a valid slow stage

Blocking. The new limit is 32 items and 128 KiB of retained payload. The actual microphone path in `live.ctg/src/audio.rs:179` onwards emits a 4,800-sample i16 batch every approximately 200 milliseconds, including quiet frames. Its half-duplex check only pauses capture when `playback.speaking()` is true. No audio has been published while the local pipeline is still assessing, asking the brain or synthesizing, so that check does not protect this interval.

Each batch costs 9,600 bytes. Thirteen batches cost 124,800 bytes; the fourteenth costs 134,400 bytes and exceeds 131,072 bytes. That is **2.8 seconds** at the actual capture cadence, before accounting for the already-active item, which can make it earlier. The raw capacity is only 2.730667 seconds of 24 kHz mono i16 audio. The current service permits an 8.5-second assessment wait and three-second HTTP requests, and the revision's actual model log reports 2.709458125 seconds of inference alone for one short phrase. Allowed longer utterances require multiple inference chunks.

The existing loop awaits each stage before reading another ingress item. The revised plan selects stop at those awaits but does not specify consuming ordinary quiet capture during them. Its 200-millisecond pre-roll prevents idle accumulation only when the consumer gets to process those frames. A direct implementation of the specified loop therefore rejects ordinary quiet microphone traffic as overload during a successful but sufficiently slow reply. This is a new functional consequence of the revision, not a request to make an unbounded queue or guarantee a latency measurement.

Revise the plan to define bounded busy audio handling that preserves normal continuous quiet capture. One implementable option is to keep ingesting audio while a turn stage is in flight, coalescing idle silence into the fixed pre-roll and retaining genuine new speech in a separately bounded turn buffer with an explicit overflow policy. Another concrete design is acceptable if it explains what happens to real speech and does not silently lose accepted commentary or user audio. Merely documenting that a normal 2.8-second operation disconnects the call, or making the model fixture artificially fast, does not meet the intended voice behavior. A larger finite budget can help but needs a reasoned relationship to the allowed stage envelope and tests; it must not pretend to support an unbounded native runtime.

Add a named mandatory test, for example `local_quiet_capture_during_slow_reply_stays_bounded_and_open`. Hold a valid assessment/brain/synthesis fixture while continuing normal quiet capture beyond the old thirteen-frame threshold. Use per-frame processed acknowledgments or actual cadence with generous outer timeouts, rather than flooding all frames synchronously and calling that microphone cadence. Assert bounded storage, no overload/error/close, no extra user turn from silence, then release the stage and observe its ordered transcript/audio successfully. Cover the same interaction with genuine later speech according to the chosen explicit bounded policy. Keep the existing deliberately excessive burst test: real overload must still terminate correctly.

This revision fits local.rs and local/kokoro.rs; it does not require altering audio.rs, changing turn-model ownership, or adding hardware to Verify.

## Additional implementation notes

- Continue to distinguish errors discovered during synchronous path preflight from model loading inside the cancellable blocking worker. Missing-model service buffering remains a required compatibility test.
- The model metadata evidence now names `waveform` as float32 [1,-1]. Production must validate and access that named output, not infer its identity from positional index zero.
- Reqwest 0.12's locally installed Response::chunk method is available without adding its stream feature. Preserve the planned incremental length checks; `.bytes()` followed by a size check is insufficient.
- Test completion receipts must follow successful awaiting/inspection of the blocking JoinHandle. Emitting a receipt from a worker Drop guard alone would weaken the explicit plan.
- The callback reservation race is acceptable as stated. A callback reserved before stop can finish without the caller synchronously waiting under a service lock. A result held across stop cannot obtain a new reservation.
- No cross-platform execution, intelligibility-by-listening, OS memory quota or fixed inference latency has been proven; the plan continues to avoid these claims.

## Observed checks and evidence

`./task prompt` exited 0. Reused the relevant Rust model/lifecycle skills and repository workflow already read in round 1. Read the entire canonical revised spec and analyst-codex-2.md, compared draft revisions, inspected current local Session/turn loop, Service::speak locking, actual audio capture and turn implementation, local reqwest response methods and the new output-metadata log. Source status is clean and its HEAD is unchanged.

A deterministic arithmetic check of the specified admission counter against actual frame size produced first rejection at frame 14: accepted 124800 bytes, next 134400 bytes, limit 131072 bytes, elapsed 2.8 seconds at 200 ms per frame. This is a source-and-contract calculation, not a claim to have run the unimplemented candidate. No implementation exists to run that candidate behavior yet.

The independently executed round 1 baseline of 42 passing library tests and real Rust synthesis of 61,800 finite samples remain valid unchanged-source evidence; they were not unnecessarily rerun. The analyst's new output metadata log was inspected, not mislabeled as a fresh reviewer execution. It reports waveform float32 [1,-1], real output [1,61800], load 1.154256583 seconds and inference 2.709458125 seconds. No asset downloads or external service mutations occurred.

All reviewer commands completed synchronously. No background command is outstanding. This report is the only repository write; source, canonical PRD/spec/review, state and acceptance boxes were not edited, and no commit was made.

## Revision binding

All digests are SHA-256. Canonical leaf and unchanged dependency identities are those recorded in reviewer-codex-1.md; the unchanged source commit binds all source files. The exact canonical inputs for this round are:

| Input | Digest |
| --- | --- |
| Canonical prd.md | 09910c498fb53fbc65533726324487117b7c12c771a93b1d6ffe866fd38fc4d5 |
| Canonical specs/spec01.md | 0bbc3e59cb002767825b4150474015a69c222cc2d1279318c7f48fdf29d6ff9a |
| Canonical review.md including round 1 | 2531d25d2315103e74482944ea55f46f19ef81cd9365b88196791ea7a745052f |
| analyst-codex-2.md | 0a9690e33f2e966587bc2e2e5662e577450b3b77a2059caca313a685f11d9afa |
| live.ctg/src/audio.rs | e67a1fa001f545061c2cb47116cfe0861e690b3d858c70b9bf1204cc86b0f60f |
| live.ctg/src/local.rs | 97f1ea18c90068a36faa1e6f89d35c996d4e70cba757938341b97d58716b0648 |
| live.ctg/src/service.rs | 9f5352d4e904b43c9477305e5b519fd9d32583c0e17c16972a235d2f4749e70a |
| live.ctg/src/assessment.rs | 52659336323d4dd6fa4d3613ab70fa1339c496517dc649937ea2c7f76ef6f15a |

Disposition: make one focused revision of busy capture handling and its named success test, preserve B1/B2 and all mandatory real synthesis scope, then request independent round 3 within the three remaining rounds.


## Coordinator record: round 3

Independent reviewer /root/kokoro_reviewer scored the exact bound revision PASS 94/100 with no blockers. Three rounds are used and two remain. Input and report digests were validated before recording. Implementation is authorized; runtime proof and independent verification remain pending.

# Kokoro independent plan review — round 3

Reviewer: `/root/kokoro_reviewer`, independent of the analyst and future implementation.
Verdict: **PASS, 94/100**, with no unresolved blocking finding. Three rounds used and two remain after coordinator recording. This passes the reviewed plan revision for implementation; it does not assert that the implementation, new tests or collection are complete. No user rating was requested or invented.

Canonical plan: `@live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/the-pipeline-hears-thinks-and-speaks-with-portable-runtimes/kokoro-speaks-through-onnx-runtime-or-refuses-the-model-it-needs`.
Source HEAD is unchanged and clean at `520888674a8d05ae435ef2f072b4d8e48812e312`. The eight-path footprint remains sufficient. The fresh allowance follows the explicit ancestor user Answer and pre-review pipeline split already bound in round 1; this result does not reset any sibling's review history.

## Score

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Real local Kokoro synthesis and inherited commentary/greeting remain the goal. Continuous quiet capture now survives valid slow replies without losing later speech. Fixed English voice and finite backlog are clearly bounded; broader voice/persona/turn-model work stays separate. |
| Ownership and reuse | 19 | The local reactor owns capture scheduling, admission and event publication; the Kokoro worker owns model state and native operations. Existing Turn methods supply classification and commit rules, avoiding a second VAD or out-of-footprint audio rewrite. |
| Dependencies and implementable slices | 18 | Current APIs, pinned assets and actual Rust synthesis remain demonstrated. One active stage plus bounded current/later slots, pending markers and explicit cancellation form an implementable state machine. The reactor is a substantial change and still requires careful implementation diff review rather than treating the former simple loop as a drop-in edit. |
| Observable acceptance and baseline evidence | 19 | The two new mandatory tests distinguish frame processing from queue acceptance, retain a held stage across more than the old envelope, add actual cadence, and compare later speech bytes exactly. Existing real-model, public Transport, overflow and join tests remain mandatory. No proposed test is mislabeled as already executed. |
| Failure, recovery and compatibility | 19 | B1/B2 bounds and prioritized joined cleanup remain intact; B3 is resolved by consuming capture rather than inflating the FIFO or discarding busy speech. Excess later speech has a documented terminal refusal. Native completion after logical close remains an explicit limitation, with suppressed results and observed eventual join. |
| Total | 94 / 100 | No unresolved blocking findings. |

## Findings resolved

**B3 is resolved in the design.** The revised task remains responsive while initialization, assessment, brain or synthesis is pending. It polls ingress and capture-stall timing as well as the active stage, prioritizes stop, and requires fairness among ordinary ready work. Quiet frames are consumed into only the 4,800-sample idle pre-roll, with their ingress permits released after processing. They therefore do not accumulate behind inference and do not depend on playback gating.

The design also addresses the obvious false fix: it does not discard all microphone input while busy. One later turn retains pre-roll, every voiced frame and terminating silence up to an explicit 720,000-sample bound. Its committed audio is frozen and represented by one marker ordered at commit among pending commentary. Subsequent quiet frames do not alter it. Further real speech while that slot is occupied receives an explicit backlog-full failure; it is not silently merged, replaced or dropped. Current/later sample storage and permitted text jobs are separately bounded, so consuming ingress does not hide an unbounded secondary queue.

The success proof is appropriately stronger than a fast-model fixture. Forty acknowledged normal frames are processed while the valid stage remains held; acknowledgment must be issued after the production reactor performs bookkeeping, not from send. One variant also runs twenty frames at actual 200-millisecond cadence. The later-speech test compares eventual STT bytes exactly and separately exercises excess speech and sample-cap refusal. Existing deliberate burst/control overload tests still prove finite admission, instead of treating ordinary quiet capture as abuse.

**B1 and B2 remain resolved.** Limits still cover admitted control work, input frames, HTTP bodies, extracted text, token count, PCM and retained errors. Moving commentary into a pending list preserves its accounting permit. Only the session task publishes terminal callbacks, outside the admission gate. Close remains a separate first-terminal-wins signal; stage/publication reservations define the cooperative race boundary; held-across-stop inference results are suppressed; one retained native worker handle is awaited exactly once. Stop now explicitly drains the later-turn slot and pending markers as well.

## Implementation and verification notes

These notes interpret the accepted requirements; they do not require another design round or new scope.

- Implement the real reactor behind the test fixtures. A processed-frame acknowledgment must follow classification, bounded copy/coalescing and permit release. A test-only ingress consumer that bypasses production scheduling would not prove B3.
- Keep pending commentary ordering and audio commit ordering visible in the implementation. A later-turn marker owns its frozen slot until selected, and promotion frees that slot exactly once. Do not let a context update or stage completion accidentally duplicate promotion.
- Avoid rebuilding a capture-stall sleep on unrelated commentary; the accepted text correctly ties it to processed capture arrival. A ready expired timer must be disarmed or advanced after handling so it cannot spin and starve stage completion. This is ordinary implementation of the stated fair reactor.
- Take bounded stage snapshots and keep callback publication in the reactor. This permits capture/context mutation while network stages are pending without holding a service mutex or a mutable borrow across the long operation.
- The existing peak-based Turn classifier remains a documented placeholder; the term genuine speech refers to that classifier here, not to a newly proven acoustic detector. Do not duplicate its threshold in local.rs.
- Test fixtures may prove scheduling, limits and cleanup. They cannot replace either mandatory real-model synthesis test. The real Transport test, companion refusal cases, finite waveform validation, model reuse, HTTP endpoint compatibility and full GPT/service suite remain required.
- Native inference is cooperative: logical closure can precede native completion, but no later chunk or result may run/publish, and final task receipt must follow the actual JoinHandle await. The plan makes no OS memory quota, intelligibility-by-listening, multi-platform execution measurement or fixed latency promise.
- Prepare both lane and repository Cargo/ORT caches before collection's bounded Verify blocks. The blocks remain relative to each repository root and isolate CARGO_TARGET_DIR. Missing fixture files must fail rather than skip, and Verify must not download them.

## Observed checks

1. `./task prompt` exited 0. Reused the already-read relevant Rust model/lifecycle skills and repository review workflow.
2. Read the full canonical spec, analyst-codex-3.md and focused round-2-to-round-3 draft diff. Inspected current audio capture, existing Turn methods and local turn loop again. Source status is clean; HEAD is the same revision reviewed in rounds 1 and 2.
3. Recomputed the canonical PRD/spec/review, analyst report, prior review and Turn source digests below. Canonical spec bytes exactly equal spec01-codex-3.md.
4. Compared mandatory `pass:` sets: no previous required test was removed; exactly `local_quiet_capture_during_slow_reply_stays_bounded_and_open` and `local_busy_capture_preserves_later_speech_and_refuses_excess` were added. Both real-model names and every previous B1/B2 proof remain present.
5. The unchanged independently executed round-1 baseline of 42 passing library tests and real Rust model synthesis remain the baseline evidence, not a test of the new unimplemented behavior. They were not unnecessarily repeated. No model acquisition or web fetch was needed for this focused revision.
6. All commands completed synchronously. No command remains running. This report is the only repository write; canonical PRD/spec/review, source, engine state, acceptance boxes and commits were not changed.

## Revision binding

All digests are SHA-256. Unchanged prerequisite/source identities remain those bound in reviewer-codex-1.md and reviewer-codex-2.md; the clean source commit above binds the full current tree.

| Input | Digest |
| --- | --- |
| Canonical prd.md | 09910c498fb53fbc65533726324487117b7c12c771a93b1d6ffe866fd38fc4d5 |
| Canonical specs/spec01.md | 27c4c0844797e157e7af14fc671ac338657a78530748cc1526675204191418bf |
| Canonical review.md including rounds 1 and 2 | aaaa7a31997d4b51514b8ece589ebdc0b6e211a61485a15241cfce58b87252cf |
| analyst-codex-3.md | c16fc66ddc8b8f76df89499e5965f9359b06b5419501228ef65a17544795f885 |
| reviewer-codex-2.md | 9960f007848cbe2d62b3dae3108b244e8e368cbebcbdebdc9658623b8f20d3a7 |
| live.ctg/src/turn.rs | 704a4d1b74523fe807edd65d1115e0788fef683d9ed8a3e44b9c763d77d7b44a |

Disposition: proceed to implementation of this exact accepted revision, then fresh independent verification of the actual diff and all Verify blocks. Two review rounds remain for any later substantive plan change.


## Independent implementation verification

/root/kokoro_verifier passed clean candidate 2872c7a872c6165519c37112ab95167b7a77b3f7 after full source/contract inspection and every canonical block, owner gate, audit and isolation. Both mandatory actual-model tests ran; 64 ordinary tests and all 22 required pass names succeeded. Report SHA-256 78be74094713df43b9c623588f187be5c92e1b8cd8fb63e91e6cc1cbd90ab100 is retained in live/.state/loop/kokoro-speaks-through-onnx-runtime-or-refuses-the-model-it-needs/verifier-codex-1.md. Coordinator checked input identities and mapped all fourteen criteria before ticking. Live manifest and three documentation files have foreign overlapping work; candidate acceptance is not collection and none of those edits may be swept. Integrated verification remains required.
