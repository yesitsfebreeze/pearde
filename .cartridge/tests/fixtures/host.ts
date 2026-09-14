// Plays the node for one helper program: the line protocol of src/wire.ts over
// its stdin and stdout.
type Json = any;
export type Program = {
	/** A call answered by id; what the program asks of the base meanwhile is served. */
	call(name: string, args?: Json): Promise<Json>;
	/** An event the program handles without answering. */
	send(name: string, args?: Json): void;
	/** Lines the program wrote on its own: emits, notifies, publishes and anything else. */
	lines: Json[];
	until(predicate: (line: Json) => boolean, ms?: number): Promise<Json>;
	close(): Promise<void>;
};

/** Start `argv`; `serve` answers its asks (`bail`, `host`) and sees its events. */
export async function program(argv: string[], serve: (line: Json) => Json | Promise<Json> = () => null, options: { cwd?: string } = {}): Promise<Program> {
	const child = Bun.spawn(argv, { cwd: options.cwd, stdin: "pipe", stdout: "pipe", stderr: "inherit" });
	const write = (frame: Json) => { child.stdin.write(JSON.stringify(frame) + "\n"); child.stdin.flush(); };
	const pending = new Map<number, (frame: Json) => void>();
	const lines: Json[] = [];
	let next = 0;
	const answer = async (line: Json) => {
		try { return { ask: line.ask, result: (await serve(line)) ?? null }; }
		catch (error) { return { ask: line.ask, error: error instanceof Error ? error.message : String(error) }; }
	};
	void (async () => {
		let buffer = "";
		for await (const chunk of child.stdout) {
			buffer += new TextDecoder().decode(chunk);
			for (let at; (at = buffer.indexOf("\n")) >= 0; buffer = buffer.slice(at + 1)) {
				const line = buffer.slice(0, at);
				if (!line) continue;
				let frame: Json;
				try { frame = JSON.parse(line); } catch { continue; }
				const waiter = pending.get(frame.id);
				if (waiter) { pending.delete(frame.id); waiter(frame); }
				else if (frame.ask !== undefined) write(await answer(frame));
				else { lines.push(frame); await serve(frame); }
			}
		}
	})();
	const call = async (name: string, args: Json = null) => {
		const reply = await new Promise<Json>(resolve => { const id = ++next; pending.set(id, resolve); write({ id, call: name, args }); });
		if (reply.error !== undefined) throw new Error(reply.error);
		return reply.result;
	};
	const until = async (predicate: (line: Json) => boolean, ms = 4000) => {
		for (const deadline = Date.now() + ms; ;) {
			const found = lines.find(predicate);
			if (found) return found;
			if (Date.now() > deadline || child.exitCode !== null) throw new Error(`no line matched; saw ${JSON.stringify(lines)}`);
			await Bun.sleep(5);
		}
	};
	return {
		call, lines, until,
		send: (name, args = null) => write({ call: name, args }),
		close: async () => { child.kill(); await child.exited; },
	};
}
