// The program side of a cartridge helper: lines of JSON on stdin from the
// node, lines of JSON on stdout back (docs/transport.txt, PROTOCOL LINES). The
// node serves stdout lines itself, so the program may write them at any time.
//
//   stdin   {"id": n, "call": name, "args": v}       answer with id n
//           {"call": name, "args": v}                handle, no answer
//           {"ask": id, "result"|"error": v}         the answer to an ask
//           {"id": n, "call": "dispose"}             run the cleanups, answer, exit
//   stdout  {"id": n, "result": v} | {"id": n, "error": s}
//           {"ask": id, "bail"|"gather": name, "args": v}
//           {"ask": id, "host": method, "params": v}
//           {"emit"|"notify": name, "data": v}, {"publish": channel, "data": v}

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

	/** Ask the host: `status`, `snapshot`, `cartridges` (`cartridge.host`). */
	host(method: string, params: Json = null): Promise<Json> { return this.ask({ host: method, params }); }

	/** Send an event to every listener without waiting (`cartridge.emit`). */
	emit(name: string, data: Json): void { this.write({ emit: name, data }); }

	/** Emit and publish on the channel of the same name (`cartridge.notify`). */
	notify(name: string, data: Json): void { this.write({ notify: name, data }); }

	/** Publish on one of this cartridge's channels (`cartridge.publish`). */
	publish(channel: string, data: Json): void { this.write({ publish: channel, data }); }

	private receive(line: string) {
		let frame: any;
		try { frame = JSON.parse(line); } catch { return diagnostic("wire", "unreadable line"); }
		if (typeof frame?.call === "string") return void this.answer(frame);
		if (frame?.ask === undefined) return;
		const waiter = this.asks.get(String(frame.ask));
		if (!waiter) return;
		this.asks.delete(String(frame.ask));
		frame.error !== undefined ? waiter.reject(new Error(String(frame.error))) : waiter.resolve(frame.result ?? null);
	}

	private async answer(frame: { id?: number; call: string; args?: Json }) {
		const reply = (body: Json) => { if (frame.id !== undefined) this.write({ id: frame.id, ...body }); };
		if (frame.call === "dispose") {
			await this.close();
			reply({ result: true });
			setTimeout(() => process.exit(0), 20);
			return;
		}
		try {
			const handler = this.handlers.get(frame.call);
			if (!handler) throw new Error(`\`${frame.call}\` is not served here`);
			reply({ result: (await handler(frame.args ?? null)) ?? null });
		} catch (error) {
			const message = error instanceof Error ? error.message : String(error);
			if (frame.id !== undefined) reply({ error: message });
			else diagnostic("wire", `${frame.call} failed: ${message}`);
		}
	}

	private ask(frame: Json): Promise<Json> {
		if (this.closing) return Promise.reject(new Error("the cartridge is stopping"));
		const id = `a${++this.next}`;
		return new Promise((resolve, reject) => {
			this.asks.set(id, { resolve, reject });
			this.write({ ask: id, ...frame });
		});
	}

	private write(frame: Json) { this.output.write(JSON.stringify(frame) + "\n"); }

	/** Refuse new asks and run every cleanup once. */
	close(): Promise<void> {
		if (!this.closing) {
			for (const waiter of this.asks.values()) waiter.reject(new Error("the cartridge is stopping"));
			this.asks.clear();
			this.closing = (async () => {
				for (const cleanup of this.finalizers.reverse()) { try { await cleanup(); } catch {} }
			})();
		}
		return this.closing;
	}
}
