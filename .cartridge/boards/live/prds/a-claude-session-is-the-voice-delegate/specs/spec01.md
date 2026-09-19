---
complexity: small
footprint:
  - src/service.rs
---

# spec06 — the watcher is handed a line that carries the transcript, gives the work back when it goes, and never answers twice

Revision 6, applying the coordinator's Decision (2026-09-17): the review
allowance is exhausted at round 5 (78/100), so this revision is not a sixth
review round. It classifies every round-5 finding as GATE-ONLY (recorded in
the ceiling paragraph below, not fixed further) or PLAN (fixed here), fixes
every PLAN finding, and rebases the whole spec onto `live.ctg` @ `6922a8f`
(`Let a provider setting choose the voice transport, GPT by default`), which
moved every line number below `:265` or so by adding a `provider` setting and
a `Transport` seam. No line this spec touches changed in *substance* — the
diff renamed `Session` to `Transport` and added one config field and one
test, entirely above `dispatch` — but every anchor is re-measured against
`6922a8f`, not inherited from `ea3c16e`.

| Finding | Round | Classification | Disposition |
| --- | --- | --- | --- |
| F16 | R4, reopened R5 | GATE-ONLY | Ceiling paragraph below. No new gate layer. |
| F20 | R5 (new) | PLAN | Fixed: `watch`'s own lease write is now pinned to go through `lease()`, and `the_promised_answer_by_survives_another_watch` is a numbered step and a required test. |
| F21 | R5 (new) | PLAN | Fixed: this file no longer miscounts its own steps. |
| F22 | R5 (new) | GATE-ONLY | Not implemented. Round 5 itself measured that it would not have caught `cheatO`; adding it is another turn of the arms race the Decision closes. |
| (unnumbered, R1–R5) | carried since R1 | PLAN | Fixed: PRD box 1's second clause is now its own Acceptance line, not merely true and unstated. |

## What is already true

Measured at `live.ctg` @ `6922a8f`, working tree clean, `cargo test` → **21
passed; 0 failed** (three more than the `ea3c16e` baseline this PRD was
scoped against: `service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial`
and two `transport::tests::*`, all added by the transport commit and untouched
by this spec). Part of this PRD has already landed; what follows is only the
remainder.

- `watch` exists (`src/service.rs:693-732`): it takes a lease (`:695-698`,
  unconditional `insert`), hands every `delegated` task of the conversation,
  marks it `handed` (`:710`), and returns `{"conversation", "tasks":[{id,
  delegation, prompt, created}]}`. **There is no line, and the lease write
  does not go through any shared function — box 1's second clause (a held
  lease marks the conversation attached) is true by inspection, but nothing
  in this spec's own Acceptance said so.**
- The *attach* half of box 3 works: `watched()` (`:684-690`) reads the lease
  and both delegation paths consult it before falling back — `dispatch`
  (`:370-372`) and `delegate` (`:874-878`).
- The *detach* half does not exist. `hand_to_agent` has exactly two call
  sites, `:378` and `:878`, **both on first dispatch**. A lease is only ever
  read via `watched()` (`:684-690`, the liveness test itself at `:689`);
  nothing sweeps an expired one. A task moved to `handed` at `:710` is
  stranded in that phase forever once its watcher goes away.
- `reply` (`:735-766`) and `commentary()` (`:984-995`) are done; box 2
  stands.
- `spoken()` (`:418-441`) gathers **user** words only, on a hardcoded literal
  (`:435`). The assistant's words are recorded by the same handler
  (`:544-585`, role literal at `:573`/`:575`) and never gathered for a task.
- The pane surface already formats `task <id>: <prompt>` at `:351`, `:857`,
  `:866`.
- `describe()` (`:1071-1116`) names watch and reply in prose; its `op` is an
  unconstrained `{"type": "string"}` (`:1103`).
- `call()` (`:117-167`) matches thirteen operations: `status`,
  `conversations`, `open`, `voice`, `state`, `context`, `agents`, `attach`,
  `delegate`, `watch`, `reply`, `note`, `cancel`.

`tool.live`'s `mcp/**` box was already reworded by the coordinator; there is
no `mcp/` directory at `6922a8f` (checked directly — the directory does not
exist anywhere in this repository's history), no `live-mcp` cartridge, and
the MCP surface of this cartridge is the `tool.live` event, answered by
`Service::tool` (`:904-913`), whose `"call"` arm forwards to `tool_call`
(`:915-936`), whose own fallback (`:928-934`) forwards any name it does not
otherwise recognise to `call()` (`:933`). No step writes into `mcp/**`, and
this spec's own `footprint` never named it.

## Acceptance

- [ ] A `watch` that hands a task over returns, for that task, a line
      `task <id>: <user words> (live said: <what the voice already said>)`,
      built by the service and not by its caller.
- [ ] `watch` marks the conversation as having an attached delegate for as
      long as the lease it just took is held (PRD box 1's second clause):
      `watched()` reads that same lease, and both delegation paths already
      consult it (`:370-372`, `:874-878`, unchanged by this spec).
- [ ] A watcher whose lease lapses without answering gives its tasks back:
      they are dispatched again, which sends them to `agent.ctg` exactly as
      if nothing had ever attached.
- [ ] An offline test drives a mock voice session, a watcher and a reply end
      to end: the session is dialled on loopback, its transcript and its
      delegation arrive over the wire, the watcher is handed the line, and
      the reply comes back out of that same session tied to the delegation.
- [ ] `tool.live` names `watch` and `reply` among the operations it accepts.
- [ ] A delegate that is still working does not lose its task: the hand-back
      fires on a watcher that has actually gone, not on one that is merely
      slow, and a task handed back cannot then be completed twice.
- [ ] The hand-over promise (`answer_by`) cannot be shortened by a further
      poll of the same conversation (F20): `watch`'s own entry-lease write
      goes through the one function that can only extend a lease, not just
      the hand-over write.
- [ ] The twenty-one tests at `6922a8f` still pass, unchanged.

## Base and dependencies

Base `live.ctg` @ `6922a8f12d5732c74a47f18c15c30e1fbc132467`, `cargo test` →
`21 passed; 0 failed` (measured). No new crate. `cartridge.json` is **not**
edited, so the cartridge is not untrusted and the running daemon keeps `live`
(repo memory: *Editing a manifest untrusts its cartridge*). Only
`src/service.rs` changes; `src/transport.rs`, added by the base commit, is
untouched.

## Implementation

1. **`spoken()` gathers the role it is asked for.** Change the signature
   (`:418`) to `fn spoken(&self, task: &Task, role: &str) -> Option<String>`
   and replace the `"user"` literal at `:435` with `role`. Two callers:
   `dispatch` (`:349`) becomes `self.spoken(&task, "user")`, and the existing
   test `spoken_words_are_the_prompt_of_the_delegation_that_follows_them`
   (`:1509`, `assert_eq!(service.spoken(&task).as_deref(), …)`) becomes
   `service.spoken(&task, "user")`. Nothing else calls it.

2. **One lease, one place, only ever later.** Add, beside `watched()`
   (`:684-690`):

   ```rust
   /// One lease per conversation, and it only ever moves the deadline
   /// further out. Both writers go through this: a later call can extend
   /// the trust a surface was given, never cut short a promise already
   /// handed to a delegate.
   fn lease(&self, conversation: &str, until: i64) -> i64 {
       let mut watchers = self.watchers.lock().expect("watchers");
       let held = watchers.entry(conversation.to_owned()).or_insert(until);
       *held = (*held).max(until);
       *held
   }

   /// A delegate that keeps talking keeps its trust. Extending only, never
   /// shortening, or a quiet word one second into a five-minute task would
   /// cut a `HELD_GRACE` lease down to `LEASE_GRACE`.
   fn renew(&self, conversation: &str) {
       if let Some(lease) = self.watchers.lock().expect("watchers").get_mut(conversation) {
           *lease = (*lease).max(store::now() + LEASE_GRACE);
       }
   }
   ```

   Add two constants beside `SETTLE_MS` (`:18`):
   `const LEASE_GRACE: i64 = 15000;` (how long a delegate that is merely
   *watching* may go quiet before it stops being trusted with new work) and
   `const HELD_GRACE: i64 = 300_000;` (how long a delegate keeps work it has
   actually been **handed**, because holding it is itself the evidence it is
   working). A third, `const LEASE_POLL: u64 = 250;`, is used by step 4.

   **This is where F20 is actually closed.** `watch`'s own entry-lease write
   at `:695-698` — today `self.watchers.lock().expect("watchers").insert(…)`,
   unconditional — must become `self.lease(conversation, store::now() +
   timeout as i64 + LEASE_GRACE);`. Round 4 renamed the constant here but left
   the write an `insert`, so a further `watch` poll — which `describe()`'s own
   text tells the delegate to make — could cut a five-minute hand-over promise
   back to fifteen seconds. Going through `lease()` for **both** writes (this
   one, and the hand-over write in step 5) is the whole fix; nothing else
   changes shape.

3. **One line per delegated task.** Add beside the constants above:

   ```rust
   /// One delegated task as a delegate reads it: which task, the words that
   /// asked for it, and what the voice had already said out loud — the
   /// transcript that led to the delegation travels with it.
   fn line(&self, task: &Task) -> String {
       match self.spoken(task, "assistant") {
           Some(said) => format!("task {}: {} (live said: {said})", task.id, task.prompt),
           None => format!("task {}: {}", task.id, task.prompt),
       }
   }
   ```

4. **A watcher that goes away gives the work back.**

   ```rust
   /// A watcher holds work only while its lease holds. When the lease goes —
   /// the surface detached, or simply stopped asking — anything it was
   /// handed and never answered goes back to the queue and is dispatched
   /// again, which is what sends it to the composition's own agent.
   fn hand_back_when_the_lease_goes(self: &Arc<Self>, conversation: &str) {
       if !self
           .sweeping
           .lock()
           .expect("sweeping")
           .insert(conversation.to_owned())
       {
           return;
       }
       let service = self.clone();
       let conversation = conversation.to_owned();
       tokio::spawn(async move {
           while service.watched(&conversation) {
               tokio::time::sleep(std::time::Duration::from_millis(LEASE_POLL)).await;
           }
           service.sweeping.lock().expect("sweeping").remove(&conversation);
           // Flipped under the one lock, so a second sweep of the same
           // conversation finds nothing to take and cannot dispatch it twice.
           let stranded: Vec<String> = service
               .tasks
               .lock()
               .expect("tasks")
               .values_mut()
               .filter(|task| task.conversation == conversation && task.phase == "handed")
               .map(|task| {
                   task.phase = "queued".into();
                   task.id.clone()
               })
               .collect();
           for id in stranded {
               service.dispatch(&id).await;
           }
       });
   }
   ```

   This folds in F7 (one sweeper per conversation, and it leaves): add a
   `sweeping: Mutex<HashSet<String>>` field beside `watchers` on `Service`
   (and `HashSet` to the `std::collections` import), initialised
   `Mutex::new(HashSet::new())` in `Service::new`. The sweeper returns
   immediately unless its `insert` of the conversation returned `true`, and
   removes itself before dispatching, so two hand-overs to the same
   conversation start one sweeper and it exits as soon as the lease has gone
   rather than living as long as the process.

   Reuse, not new machinery: `dispatch` (`:342-387`) already chooses pane,
   then watcher, then `hand_to_agent`, and already handles the agent being
   unreachable by marking the task `unassigned` (`:378-386`). Putting the task
   back to `queued` and calling `dispatch` is the whole hand-back. Polling the
   lease rather than sleeping to its expiry is deliberate: a watcher renews
   its lease on every poll (via `reply`'s `renew`, step 6), and a sweep that
   slept the whole lease could not notice a renewal or a detach between them.

5. **`watch` hands the line, the deadline and the sweeper over.** Rewrite
   `watch` (`:693-732`):

   ```rust
   /// A surface asks for spoken work and holds a lease while it answers.
   async fn watch(self: &Arc<Self>, conversation: &str, timeout_ms: u64) -> Result<Value> {
       let timeout = timeout_ms.min(25000);
       self.lease(conversation, store::now() + timeout as i64 + LEASE_GRACE);
       // The node is held while this waits, so the wait is short and the
       // caller loops; a lease outlives each poll.
       let deadline = store::now() + timeout.min(1000) as i64;
       loop {
           let handed: Vec<Task> = self
               .tasks
               .lock()
               .expect("tasks")
               .values_mut()
               .filter(|task| task.conversation == conversation && task.phase == "delegated")
               .map(|task| {
                   task.phase = "handed".into();
                   task.clone()
               })
               .collect();
           if !handed.is_empty() {
               for task in &handed {
                   let _ = self.store().save(task);
               }
               // Being handed work is the longer commitment: holding it is
               // itself the evidence a delegate is still working.
               let answer_by = self.lease(conversation, store::now() + HELD_GRACE);
               let tasks: Vec<Value> = handed
                   .iter()
                   .map(|task| {
                       json!({
                           "id": task.id,
                           "delegation": task.delegation,
                           "prompt": task.prompt,
                           "created": task.created,
                           "line": self.line(task),
                           "answer_by": answer_by,
                       })
                   })
                   .collect();
               self.hand_back_when_the_lease_goes(conversation);
               return Ok(json!({"conversation": conversation, "tasks": tasks}));
           }
           if store::now() >= deadline {
               return Ok(json!({"conversation": conversation, "tasks": []}));
           }
           tokio::time::sleep(std::time::Duration::from_millis(100)).await;
       }
   }
   ```

   Collecting `Vec<Task>` rather than `Vec<Value>` and saving in the same pass
   deletes the second-lock save loop the base has (`:720-724`), which
   re-locked `tasks` per id only to reach the record; this was never an
   inverted-lock hazard (the codebase only ever orders `tasks` then `store`)
   and is a tidy simplification, not a behaviour change.

6. **The pane delegate reads the same line.** Replace the three
   `format!("task {}: {}", …)` arguments to `send_keys` at `:351`, `:857`,
   `:866` with `&self.line(&task)`. One source of truth, and the terminal
   delegate carries the transcript the watching one carries.

7. **`reply` renews the lease and refuses a second answer.** In `reply`
   (`:735`), call `self.renew(conversation);` as the first line of the
   function body — this is what a delegate's own quiet word or answer keeps
   its trust with. Inside the `Some(id) =>` arm, before setting `task.phase =
   "completed"`, add:

   ```rust
   if task.phase == "completed" || task.phase == "cancelled" {
       return Err(format!("`{id}` already carries an answer, in phase `{}`", task.phase));
   }
   ```

   Whoever answers first wins and the loser is told, instead of both
   speaking; the refusal returns before `speak`, so the user hears one
   answer.

   What steps 2–7 together promise, exactly: a delegate loses work only after
   five minutes in which it neither answered nor said anything, the deadline
   is handed to it with the work, and a further poll of the conversation it
   is watching cannot shorten a promise already made. There is no obligation
   a delegate can fail without being told it exists.

8. **`tool.live` names its operations.** In `describe()`'s fallback
   (`:1103`), give `op` an `enum` of the thirteen ops `call()` matches
   (`:125-166`) and a `description` naming `answer_by`:

   ```rust
   "op": {"type": "string", "enum": [
       "status", "conversations", "open", "voice", "state", "context",
       "agents", "attach", "delegate", "watch", "reply", "note", "cancel",
   ], "description": "`watch` hands back one line per delegated task and an `answer_by` deadline; call `watch` again before it lapses to keep the work, or `reply` to answer it."},
   ```

9. **The end-to-end test**,
   `a_watching_delegate_is_handed_the_line_and_its_reply_reaches_the_voice_session`
   (`#[tokio::test(flavor = "multi_thread")]`): hold `crate::socket::TEST` and
   `only_the_dummy_key(crate::socket::DUMMY)`; build `fixture()` and
   `wired(&fixture, audio::fake::open)`; `open` a conversation and
   `voice(&conversation, Some(true))`; await `fixture.heard("session.start")`;
   **take the lease first** with `service.call(json!({"op": "watch",
   "conversation": conversation, "timeout_ms": 0}))`; push two
   `session.input_transcript.delta` fragments and one
   `session.output_transcript.delta` fragment through `fixture.to_client`
   (each with its own `event_id`, `start_ms`, `end_ms` — F17's concern, so
   `spoken()`'s window actually admits them), then a
   `session.delegation.created` with `delegation.target == "client"`,
   `delegation.id == "d1"` and an `offset_ms` after the fragments; poll
   `service.call(json!({"op": "watch", …, "timeout_ms": 900}))` in a
   **bounded** loop (8 is ample — `SETTLE_MS` is 800 ms and `watch` loops at
   most 1 s) until `["tasks"][0]["line"]` is a string; assert that line
   starts with `task live-fixture:d1: `, contains the user's words, and
   contains `(live said: I can do that)`; then
   `service.call(json!({"op": "reply", "conversation": conversation, "id":
   "live-fixture:d1", "text": "four files"}))` and assert
   `fixture.heard("session.commentary.append")` carries that content **and**
   `delegation_id == "d1"`. End with `voice(&conversation, Some(false))`: the
   fake devices are process-global and `fake::open` clears the put-down log,
   so a test that leaves its session running makes
   `voice_runs_a_session_on_the_wire_…` fail on a stale log (measured in the
   round-4/5 history: without the stop it fails with `left: ["speaker",
   "microphone", "speaker", "microphone"]`).

10. **The hand-back test**,
    `a_watcher_that_detaches_hands_its_task_back_to_the_agent`. No fixture
    needed: `service()` suffices. `service.call(json!({"op": "watch", …,
    "timeout_ms": 0}))`, `service.delegate(&conversation, "four files", None,
    None)` and assert the phase is `delegated` (the watcher kept it), watch
    again and assert the task comes back, then make the surface go away by
    writing an already-past lease directly into `watchers` for that
    conversation. Then wait — `until()` (5 s bound) — for the task's phase to
    **settle**, and assert it is `unassigned`. Wait for `phase ==
    "unassigned" || phase == "delegated"`, not for `phase != "handed"`:
    `queued` is a transient the sweeper passes through on its way to the
    agent, and a predicate that stops at it reds a correct tree.

    That assertion is the gate's real strength. Offline, `Ctx::call` has no
    base to answer it, so `hand_to_agent` returns `Err` and `dispatch` sets
    `unassigned`. **`unassigned` is set on exactly one line of this file, in
    the agent hand-off failure path.** A task can only reach it by being
    dispatched again, so the phase itself is the proof the work went back to
    `agent.ctg` rather than merely being requeued or forgotten.

11. **Two tests for box 5.**
    `a_delegate_that_is_still_working_keeps_its_task`: watch, delegate, watch
    again so the task is `handed`, write a lease one millisecond from
    lapsing, then `service.call(json!({"op": "reply", …, "quiet": true}))`
    with no id. Sleep `LEASE_POLL * 4` and assert the task is **still
    `handed`** — the sweeper ran and left it alone because the quiet word
    renewed the lease.
    `a_task_handed_back_cannot_be_answered_twice`: watch, delegate, watch,
    `reply` with the id once (it is accepted), then `reply` with the same id
    again and assert the second call `is_err()` and that the task's stored
    text is still the first answer.

12. **Two cheap tests.** `the_live_tool_offers_watch_and_reply`: read
    `describe("tool.live")["input_schema"]["properties"]["op"]["enum"]` and
    assert it contains both `"watch"` and `"reply"`, and that the
    `description` mentions `answer_by`.
    `the_promised_answer_by_survives_another_watch` (F20's own test, closing
    the finding rather than just its production code): watch, delegate,
    watch to get `answer_by` from the payload, assert it exceeds
    `LEASE_GRACE`, watch **again**, and assert the lease held for that
    conversation is still `>= answer_by` — a further poll does not shorten
    what was promised.

Twelve steps. (F21: the previous revision said "steps 1–13" while prescribing
twelve; this revision has exactly twelve and says so.)

## Verify and Proof

All three blocks follow the engine facts in
`prd.ctg/.cartridge/templates/spec.md`: `sh -eu -c`, run first in the lane and
then in `repo`, paths relative to the repo root, no `cd`, an isolated
`CARGO_TARGET_DIR` for every cargo command. None writes inside the footprint;
scratch is `$$`-suffixed under `$TMPDIR` with a `trap … EXIT`.

Block 1 is structural: it pins each service property **inside the item that
owes it**, asks of each test only that it drives the seam, and forbids a test
to read the service's own source. Block 2 executes the suite, the required-test
list and clippy. **Block 3 executes a mutant**, and is where the line's
behaviour is actually proved. This is the same three-block shape round 5
reviewed; the only content change from revision 5 is one new pin (`self.lease(`
inside `watch`, closing F20) and one new required-test name
(`the_promised_answer_by_survives_another_watch`, also F20). Nothing about the
mutant, the ban list or the named-test clause changed, because F16 is GATE-ONLY
(see the ceiling below) and changing them again without a working new idea
would only restart the same arms race round 5 ended.

```sh
test -f src/service.rs
python3 - <<'PY'
import re, sys
LINE_TEST = "a_watching_delegate_is_handed_the_line_and_its_reply_reaches_the_voice_session"
BACK_TEST = "a_watcher_that_detaches_hands_its_task_back_to_the_agent"
WORK_TEST = "a_delegate_that_is_still_working_keeps_its_task"
ONCE_TEST = "a_task_handed_back_cannot_be_answered_twice"
src = open("src/service.rs").read()
# A comment is not code: a token that only ever appears in one proves nothing.
code = re.sub(r'//.*$', '', src, flags=re.M)
fail = []

cut = code.find("\nmod tests")
if cut < 0:
	cut = code.find("\n#[cfg(test)]")
if cut < 0:
	fail.append("src/service.rs: the test module cannot be located, so the service cannot be told from its suite")
	cut = len(code)
service, suite = code[:cut], code[cut:]

def regions(text, name):
	"""Every item of this exact name, each from its signature to the next item at
	that indent. Exact, and all of them: a decoy called `line_of` is a different
	function and must not be able to stand in for `line`."""
	out = []
	for m in re.finditer(r'\n\t(?:pub )?(?:async )?fn ' + re.escape(name) + r'\s*(?:<|\()', text):
		rest = text[m.start() + 1:]
		nxt = re.search(r'\n\t(?:pub )?(?:async )?fn |\n\t#\[', rest[1:])
		out.append(rest if not nxt else rest[:nxt.start() + 1])
	return out

def asserted(text):
	"""Only what an assertion actually reads: each assert's balanced argument list."""
	out = []
	for m in re.finditer(r'\bassert(_eq|_ne)?!\s*\(', text):
		keeps = 2 if m.group(1) else 1
		depth, i = 0, m.end() - 1
		while i < len(text):
			if text[i] == '(':
				depth += 1
			elif text[i] == ')':
				depth -= 1
				if depth == 0:
					args = text[m.end():i]
					# The trailing message is prose, not a claim; every cheat so
					# far satisfied these checks out of it. `assert!` claims its
					# first argument, `assert_eq!` its first two.
					depth2, seen, cutp = 0, 0, len(args)
					for k, ch in enumerate(args):
						if ch in "([{":
							depth2 += 1
						elif ch in ")]}":
							depth2 -= 1
						elif ch == "," and depth2 == 0:
							seen += 1
							if seen == keeps:
								cutp = k
								break
					out.append(args[:cutp])
					break
			i += 1
	return "\n".join(out)

# Each service property is pinned inside the item that owes it, never merely
# somewhere in the file: a token loose in the service proves only that someone
# typed it.
for head, why, token in [
	("watch",
	 "the watch operation does not put the line it hands over into the payload it returns",
	 '"line": self.line('),
	("watch",
	 "the watch operation never arranges for work it hands over to come back",
	 "self.hand_back_when_the_lease_goes("),
	("watch",
	 "watch's own entry lease can bypass the one place a lease is allowed to move (F20)",
	 "self.lease("),
	("line",
	 "the line is built without ever asking the record what the voice itself had said",
	 'self.spoken(task, "assistant")'),
	("hand_back_when_the_lease_goes",
	 "nothing takes a task that a departed watcher was handed and never answered",
	 '"handed"'),
	("hand_back_when_the_lease_goes",
	 "a task taken back is never put where it can be dispatched again",
	 '"queued"'),
	("reply",
	 "answering does not tell the lease that the delegate is still there",
	 "self.renew("),
	("watch",
	 "the delegate is handed work without being told when the commitment on it lapses",
	 '"answer_by"'),
	("lease",
	 "a lease can be set to an earlier instant than one already promised",
	 ".max("),
	("reply",
	 "a task that already carries an answer can be answered a second time",
	 'task.phase == "completed"'),
]:
	found = regions(service, head)
	if not found:
		fail.append(f"src/service.rs: {why}")
	elif not any(token in one for one in found):
		fail.append(f"src/service.rs: {why}")

if "(live said: " not in service:
	fail.append("src/service.rs: the service itself never formats what the voice had already said; the suite alone may not carry it")

# Each gating test's own region, and — for what it claims to observe — only the
# text its assertions actually read. Several of these tokens occur elsewhere in
# the baseline file, so a file-wide test would be satisfied before any work.
owed = [
	(LINE_TEST, [
		("it never asks the service to watch", '"op": "watch"', False),
		("it never reads the line the watch hands back", '["line"]', False),
		("it never answers through the service", '"op": "reply"', False),
		("it never observes the answer arriving at the voice session", 'fixture.heard("session.commentary.append")', False),
		("it never requires the words the voice had already said to travel in that line", '(live said: I can do that)', True),
	]),
	(BACK_TEST, [
		("it never asks the service to watch", '"op": "watch"', False),
		("it never requires the stranded task to reach the agent hand-off", 'unassigned', True),
	]),
	(WORK_TEST, [
		("it never has the delegate say anything while it works", '"quiet": true', False),
		("it never requires the working delegate to still hold its task", 'handed', True),
	]),
	(ONCE_TEST, [
		("it never answers the same task a second time", '"op": "reply"', False),
		("it never requires that second answer to be refused", 'is_err()', True),
	]),
]
# A suite that reads its own source is not watching what the service does; it is
# watching what the service is spelled like, and it will report on a copy of
# itself rather than on the run.
for reader in ("include_str!", "include_bytes!", "read_to_string", "CARGO_MANIFEST_DIR"):
	if reader in suite:
		fail.append("src/service.rs: a test reads the service's own source text instead of observing what it does")
		break

for name, properties in owed:
	found = regions(suite, name)
	body = found[0] if found else None
	if body is None:
		fail.append(f"src/service.rs: `{name}` is not a test in this module")
		continue
	claims = asserted(body)
	for why, token, must_assert in properties:
		if token not in (claims if must_assert else body):
			where = " in anything it asserts" if must_assert else ""
			fail.append(f"src/service.rs: `{name}` proves nothing — {why}{where}")

for line in fail:
	print(line, file=sys.stderr)
sys.exit(1 if fail else 0)
PY
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/voice-delegate-verify}"
out="${TMPDIR:-/tmp}/live-delegate-verify-$$.out"
list="${TMPDIR:-/tmp}/live-delegate-verify-$$.list"
trap 'rm -f "$out" "$list"' EXIT
if ! cargo test --quiet >"$out" 2>&1; then
	tail -40 "$out"
	echo "the suite does not pass"
	exit 1
fi
cargo test --quiet -- --list >"$list" 2>/dev/null
for name in \
	audio::tests::a_refused_microphone_is_the_error_the_caller_sees \
	audio::tests::a_voice_puts_its_devices_down_before_stopping_returns \
	audio::tests::an_unchanged_rate_copies \
	audio::tests::halving_the_rate_averages_neighbours \
	audio::tests::the_speaker_holds_the_gate_while_it_has_audio \
	service::tests::a_conversation_opens_once_and_is_found_again \
	service::tests::a_device_that_will_not_open_is_a_readable_voice_error_in_the_state \
	service::tests::a_key_the_fixture_does_not_know_never_opens_a_session \
	service::tests::a_note_comes_back_in_the_state \
	service::tests::a_spoken_line_is_capped_rather_than_read_out_whole \
	service::tests::a_transcript_names_each_speaker_once \
	service::tests::an_answer_with_no_voice_session_is_recorded_rather_than_refused \
	service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial \
	service::tests::spoken_words_are_the_prompt_of_the_delegation_that_follows_them \
	service::tests::the_voice_session_is_told_what_the_record_says \
	service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns \
	socket::tests::a_delta_that_is_not_base64_is_no_audio_rather_than_a_panic \
	socket::tests::audio_decodes_back_to_the_samples_it_carried \
	socket::tests::the_environment_key_wins \
	transport::tests::an_unknown_provider_is_refused_before_any_dial \
	transport::tests::the_default_provider_builds_the_gpt_transport \
	service::tests::a_watching_delegate_is_handed_the_line_and_its_reply_reaches_the_voice_session \
	service::tests::the_live_tool_offers_watch_and_reply \
	service::tests::a_watcher_that_detaches_hands_its_task_back_to_the_agent \
	service::tests::a_delegate_that_is_still_working_keeps_its_task \
	service::tests::a_task_handed_back_cannot_be_answered_twice \
	service::tests::the_promised_answer_by_survives_another_watch
do
	grep -q "^$name: test\$" "$list" || { echo "missing test: $name"; exit 1; }
done
cargo clippy --all-targets --quiet -- -D warnings
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/voice-delegate-verify}"
mutant="${TMPDIR:-/tmp}/live-delegate-mutant-$$"
out="${TMPDIR:-/tmp}/live-delegate-mutant-$$.out"
proof="service::tests::a_watching_delegate_is_handed_the_line_and_its_reply_reaches_the_voice_session"
trap 'rm -rf "$mutant" "$out"' EXIT
rm -rf "$mutant"
mkdir -p "$mutant"
# A copy, so the mutation never touches the footprint the collector is verifying.
tar -cf - --exclude ./target --exclude ./.git . | tar -xf - -C "$mutant"
python3 - "$mutant/src/service.rs" <<'PY'
import sys
path = sys.argv[1]
text = open(path).read()
# The gathering itself is made to ignore which speaker was asked for. The call
# sites keep their text, so a tree cannot survive this by watching its own source.
whose = "fragment.role == role"
if whose not in text:
	print("the record is never asked for one speaker's words rather than another's", file=sys.stderr)
	sys.exit(1)
open(path, "w").write(text.replace(whose, 'fragment.role == role.replace("assistant", "user")'))
PY
# A mutant that does not build teaches nothing: any red would satisfy a gate that
# only asked for red, so the build must succeed before the run means anything.
if ! cargo build --tests --quiet --manifest-path "$mutant/Cargo.toml" >"$out" 2>&1; then
	tail -20 "$out"
	echo "the mutated service does not build, so nothing can be concluded from the suite failing on it"
	exit 1
fi
# The service now repeats the user's words back instead of the voice's. The test
# that claims to observe the line must be the one that dies of it.
if cargo test --quiet --manifest-path "$mutant/Cargo.toml" -- --exact "$proof" >"$out" 2>&1; then
	echo "the test that claims to watch the line still passes against a service that repeats the user's words back to them"
	exit 1
fi
```

## What these blocks prove, and what they do not

Re-measured at `live.ctg` @ `6922a8f`, `CARGO_TARGET_DIR` outside every
repository, working tree clean before and after (the analyst's clone under
`scratchpad/analyst-delegate/`; nothing in `live.ctg` was written):

| Tree | what it is | b1 | b2 | b3 |
| --- | --- | ---: | ---: | ---: |
| `clean` | `6922a8f` untouched | **1** | **1** | **1** |
| `honest` | steps 1–12 (this revision, built and run) | 0 | 0 | 0 |

`honest`: 27 tests pass (21 baseline + 6 this spec adds), `cargo clippy
--all-targets -- -D warnings` exit 0. Block 3 adds about 3 s.

The historical cheat rows below are **preserved from round 5's review, measured
against `ea3c16e`**, and are not re-run here. None of them touches anything the
transport commit changed — every cheat and every pin lives in `dispatch`
through `describe()`, all strictly after the `Transport`/`provider` seam — so
re-deriving them against `6922a8f` would remeasure the same mechanism for no
new information, which is exactly the kind of extra gate-verification round
the Decision says to stop spending:

| Tree | what it is | b1 | b2 | b3 |
| --- | --- | ---: | ---: | ---: |
| `cheatJ` | round 3's `format!` string surgery | **1** | 0 | **1** |
| `cheatK` | round 3's fixture hoisted to a `const` | **1** | 0 | **1** |
| `cheatL` | every step done, every pin satisfied, only `line()` discards the voice's words | 0 | 0 | **1** |
| `cheatM1` | round 4's cheat: `include_str!` guard on the call site | **1** | 0 | **1** |
| `cheatM2` | the adaptive form: guard on the mutation site | **1** | 0 | **1** |
| `cheatN` | round 4's unconditional insert, promise test kept | **1** | **1** | 0 |
| `cheatN2` | round 5's: `cheatN`'s defect, promise test deleted | 0 | 0 | 0 |
| `cheatO` | round 5's: `cheatL` + a run-time source read (fifth route) | 0 | 0 | 0 |

**F20 is closed by this revision.** `cheatN2` was 0/0/0 against revision 5
because block 1's `.max(` pin was scoped to `lease`'s own region — satisfied
by a `lease()` used only at the hand-over — while `watch`'s entry write
bypassed it entirely, and block 2's required-test list did not contain
`the_promised_answer_by_survives_another_watch`. This revision adds the pin
`self.lease(` inside `watch`'s own region and adds that test's name to block
2's list. Against the *code* this revision actually ships — where the entry
write **is** `self.lease(…)` — `cheatN2` no longer describes a tree distinct
from `honest`; reverting the entry write back to a raw `insert` now fails
block 1 on the new pin before block 2 is even reached.

## The ceiling (F16, and why F22 is not attempted)

Five review rounds tried, in order: a grep for the production shape (beaten by
a tree that declared the field and never read it); a named executed test
(beaten by a tree that kept the name and swapped the body); a required phrase
counted once in the test's own region (beaten by `format!` string surgery and
a fixture hoisted to a `const`); a mutant with an `include_str!`-source-reading
ban (beaten by `cheatM1`/`cheatM2`, whose guard reads the mutated copy at
compile time and dies for a reason unrelated to the behaviour); and the same
mutant plus a build-must-succeed clause, a named-test-must-die clause, and a
four-spelling source-reading ban (beaten by `cheatO`, which reads its own
source at **run time** through `std::fs::read(file!())` — no banned spelling,
a runtime read so the mutant still builds, and `file!()` resolving to the
mutated copy because `--manifest-path` runs with cwd at the mutant's package
root, so the named test is exactly the one that dies).

The pattern, stated once: **a Verify block can require a named test to exist,
to run, and to turn red on a mutated tree — but it cannot establish that the
test died of the behaviour rather than of something the test itself supplied.**
Where the judge (the test) and the judged (the mutation) run in the same
process, the judged can see the judge, by some route a finite ban list cannot
enumerate in advance. Round 4's own remaining suggestion — require that the
rest of the suite still pass on the mutant build too — was measured in round 5
not to close this: `cheatO`'s guard lives inside the named test itself, so a
whole-suite-passes clause would not have caught it either. This spec does not
add that clause (F22): doing so would be a sixth attempt at a gate the fifth
attempt already showed the shape of the defeat, not a fix for anything new.

Per `prd.ctg/.cartridge/workflows/review-plan.md` step 4, this claim has
reached the ceiling: a Verify block can require the named test to exist, to
execute and to turn red on the one mutation this spec's block 3 performs
(whose words reach the line — that much **is** genuinely proved by execution,
reproducibly, on both `ea3c16e` and `6922a8f`), and no more than that. The
hand-back, the double-answer refusal and the `answer_by` contract rest on
their named executed tests (measured passing in `honest`, above) plus block
1's structural pins — strictly weaker than an executed proof, and a reviewer
reading those test bodies against the running code is the backstop for them,
exactly as the Decision states. This is not a blocking finding by itself; it
is the honest limit of what a same-process gate can establish, recorded here
instead of spending a sixth round discovering it again.

## Remaining work, deliberately not in this slice

`cartridge.json` is not edited and no `mcp/` directory is created. A task
delegated to a **pane** that dies is already handled separately (`:358-368`)
and is not touched. `LEASE_GRACE` and `HELD_GRACE` are constants, not
settings: making them configurable needs a manifest edit, which untrusts the
cartridge, and no evidence yet says five minutes is wrong. The out-of-process
differential harness that would close F16 for good (build the library twice,
compare observable output, never let the test see which build it is in) is
its own PRD, per the coordinator's Decision, and nothing on this board depends
on it today.
