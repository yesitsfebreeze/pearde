// The program side of a cartridge's helper protocol: lines of JSON on stdin
// from the cartridge's init.lua, lines of JSON on stdout back. The program
// never sees the base; init.lua forwards. Copy this file into a cartridge.
//
// The node runs one Lua thread: while init.lua waits for an answer nothing
// else in it runs, so a line the program writes on its own would wait behind
// the answer it blocks. Hence two channels:
//
//   stdout, only in answer to a line with an id from init.lua
//     {"id": n, "result": v} | {"id": n, "error": s}          the answer
//     {"id": n, "ask": "a1", "bail": name, "args": v}         the base is needed first; init.lua
//     {"id": n, "ask": "a1", "host": method, "params": v}     serves it and continues with
//                                                             {"id": n+1, "answer": "a1", "result"|"error": ...}
//   the pump, a FIFO init.lua reads with `cat`, for lines written on the program's own
//     {"event": name, "data": v}                              cartridge.emit; likewise "notify" and "publish"
//     {"id": "a2", "bail": name, "args": v}                   an ask between calls, answered on stdin
//     {"id": "a2", "host": method, "params": v}               as {"id": "a2", "result"|"error": ...}
//   stdin from init.lua
//     {"id": n, "call": name, "args": v}                      answer with id n (or the id of the last answer line)
//     {"call": name, "args": v}                               an event to handle, no answer expected
//     {"id": n, "call": "pump"}                               answer with the FIFO path
//     {"id": n, "call": "dispose"}                            run the cleanups, answer, exit

import { closeSync, constants, mkdtempSync, openSync, rmSync, writeSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

type Json = any;
type Handler = (args: Json) => Json | Promise<Json>;
type Waiter = { resolve: (v: Json) => void; reject: (e: Error) => void };

/** One diagnostic line on stderr; the base records it. */
export function diagnostic(src: string, msg: string, fields: Record<string, unknown> = {}): void {
	process.stderr.write(JSON.stringify({ t: Date.now(), src, msg, ...fields }) + "\n");
}

export class Wire {
	private handlers = new Map<string, Handler>();
	private asks = new Map<string, Waiter>();
	private finalizers: (() => void | Promise<void>)[] = [];
	private next = 0;
	private closing: Promise<void> | undefined;
	/** A call is being answered: asks ride its answer lines. */
	private busy = false;
	/** The id the next stdout line answers; absent while init.lua has the turn. */
	private current: number | undefined;
	private queued: Json[] = [];
	private done: Json | undefined;
	/** Lines for the pump, kept until `cat` has the FIFO open. */
	private lines: string[] = [];
	private pump: { dir: string; path: string; fd?: number; timer?: ReturnType<typeof setTimeout> } | undefined;

	constructor(private input: NodeJS.ReadableStream = process.stdin, private output: NodeJS.WritableStream = process.stdout) {
		let buffer = "";
		input.setEncoding("utf8");
		input.on("data", chunk => {
			buffer += String(chunk);
			let at: number;
			while ((at = buffer.indexOf("\n")) >= 0) {
				const line = buffer.slice(0, at).trim();
				buffer = buffer.slice(at + 1);
				if (line) this.receive(line);
			}
		});
		const gone = () => { void this.close().then(() => setTimeout(() => process.exit(0), 20)); };
		input.on("end", gone);
		input.on("close", gone);
		input.resume();
	}

	/** `apply` receives the config; any other name answers that `call`. */
	on(name: string, handler: Handler): void { this.handlers.set(name, handler); }

	/** Runs when the cartridge stops, last registered first. */
	onClose(cleanup: () => void | Promise<void>): void { this.finalizers.push(cleanup); }

	/** Send an event and take the first answer (`cartridge.bail`). */
	call(name: string, args: Json): Promise<Json> { return this.ask({ bail: name, args }); }

	/** Ask the host: `status`, `snapshot`, `cartridges`, `bridge.status`, `bridge.call` (`cartridge.host`). */
	host(method: string, params: Json = null): Promise<Json> { return this.ask({ host: method, params }); }

	/** Send an event to every listener without waiting (`cartridge.emit`). */
	emit(name: string, data: Json): void { this.line({ event: name, data }); }

	/** Emit and publish on the channel of the same name (`cartridge.notify`). */
	notify(name: string, data: Json): void { this.line({ notify: name, data }); }

	/** Publish on one of this cartridge's channels (`cartridge.publish`). */
	publish(channel: string, data: Json): void { this.line({ publish: channel, data }); }

	private receive(line: string) {
		let frame: any;
		try { frame = JSON.parse(line); } catch { return diagnostic("wire", "unreadable line"); }
		if (typeof frame?.call === "string") return void this.answer(frame);
		if (typeof frame?.answer === "string") {
			this.settle(frame.answer, frame);
			this.current = frame.id;
			return this.flush();
		}
		if (typeof frame?.id === "string") this.settle(frame.id, frame);
	}

	private settle(id: string, frame: { result?: Json; error?: Json }) {
		const waiter = this.asks.get(id);
		if (!waiter) return;
		this.asks.delete(id);
		frame.error !== undefined ? waiter.reject(new Error(String(frame.error))) : waiter.resolve(frame.result ?? null);
	}

	private async answer(frame: { id?: number; call: string; args?: Json }) {
		if (frame.call === "dispose") {
			await this.close();
			if (frame.id !== undefined) this.write({ id: frame.id, result: true });
			setTimeout(() => process.exit(0), 20);
			return;
		}
		if (frame.id !== undefined) { this.busy = true; this.current = frame.id; }
		if (frame.call === "pump") { this.done = { result: this.openPump() }; return this.flush(); }
		try {
			const handler = this.handlers.get(frame.call);
			if (!handler) throw new Error(`\`${frame.call}\` is not served here`);
			const result = await handler(frame.args ?? null);
			if (frame.id !== undefined) { this.done = { result: result ?? null }; this.flush(); }
		} catch (error) {
			const message = error instanceof Error ? error.message : String(error);
			if (frame.id !== undefined) { this.done = { error: message }; this.flush(); }
			else diagnostic("wire", `${frame.call} failed: ${message}`);
		}
	}

	/** One stdout line per turn: an ask if any waits, else the answer once it is ready. */
	private flush() {
		if (this.current === undefined || this.closing) return;
		if (this.queued.length) {
			const { id, ...ask } = this.queued.shift();
			this.write({ id: this.current, ask: id, ...ask });
			this.current = undefined;
		} else if (this.done !== undefined) {
			this.write({ id: this.current, ...this.done });
			this.current = undefined;
			this.done = undefined;
			this.busy = false;
		}
	}

	private write(frame: Json) { this.output.write(JSON.stringify(frame) + "\n"); }

	private ask(frame: Json): Promise<Json> {
		if (this.closing) return Promise.reject(new Error("the cartridge is stopping"));
		const id = `a${++this.next}`;
		return new Promise((resolve, reject) => {
			this.asks.set(id, { resolve, reject });
			if (this.busy || !this.pump) { this.queued.push({ id, ...frame }); this.flush(); }
			else this.line({ id, ...frame });
		});
	}

	private line(frame: Json) {
		this.lines.push(JSON.stringify(frame) + "\n");
		this.pumpFlush();
	}

	private openPump(): string {
		const dir = mkdtempSync(join(tmpdir(), "cartridge-pump-"));
		const path = join(dir, "pump");
		const made = Bun.spawnSync(["mkfifo", path]);
		if (made.exitCode !== 0) throw new Error(`mkfifo: ${made.stderr.toString().trim()}`);
		this.pump = { dir, path };
		return path;
	}

	/** Write pump lines once `cat` has the FIFO open; a full pipe or an absent reader waits and retries. */
	private pumpFlush() {
		const pump = this.pump;
		if (!pump || pump.timer || this.closing) return;
		const retry = () => { pump.timer = setTimeout(() => { pump.timer = undefined; this.pumpFlush(); }, 10); };
		try {
			if (pump.fd === undefined) pump.fd = openSync(pump.path, constants.O_WRONLY | constants.O_NONBLOCK);
			while (this.lines.length) {
				const line = this.lines[0];
				const wrote = writeSync(pump.fd, line);
				if (wrote < line.length) { this.lines[0] = line.slice(wrote); return retry(); }
				this.lines.shift();
			}
		} catch (error) {
			const code = (error as NodeJS.ErrnoException).code ?? "";
			if (["ENXIO", "EAGAIN", "EWOULDBLOCK", "EINTR"].includes(code)) return retry();
			diagnostic("wire", `pump: ${error}`);
		}
	}

	/** Refuse new asks and run every cleanup once. */
	close(): Promise<void> {
		if (!this.closing) {
			for (const waiter of this.asks.values()) waiter.reject(new Error("the cartridge is stopping"));
			this.asks.clear();
			this.closing = (async () => {
				for (const cleanup of this.finalizers.reverse()) { try { await cleanup(); } catch {} }
				const pump = this.pump;
				if (pump) {
					clearTimeout(pump.timer);
					if (pump.fd !== undefined) try { closeSync(pump.fd); } catch {}
					try { rmSync(pump.dir, { recursive: true, force: true }); } catch {}
				}
			})();
		}
		return this.closing;
	}
}
