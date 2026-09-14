// Plays init.lua for one helper program: the line protocol of src/wire.ts over
// its stdin and stdout, and the pump it opens.
import { createReadStream } from "node:fs";

type Json = any;
export type Program = {
	/** A call answered by id; what the program asks of the base on the way is served. */
	call(name: string, args?: Json): Promise<Json>;
	/** An event the program handles without answering. */
	send(name: string, args?: Json): void;
	/** Lines the program wrote on its own: events on the pump, and anything else on stdout. */
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
		try { return { id: line.id, result: (await serve(line)) ?? null }; }
		catch (error) { return { id: line.id, error: error instanceof Error ? error.message : String(error) }; }
	};
	const each = async (stream: AsyncIterable<Uint8Array | string>, frame: (line: Json) => void) => {
		let buffer = "";
		for await (const chunk of stream) {
			buffer += typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk);
			for (let at; (at = buffer.indexOf("\n")) >= 0; buffer = buffer.slice(at + 1)) {
				const line = buffer.slice(0, at);
				if (line) try { frame(JSON.parse(line)); } catch { /* not a frame */ }
			}
		}
	};
	void each(child.stdout, frame => {
		const waiter = pending.get(frame.id);
		if (waiter) { pending.delete(frame.id); waiter(frame); } else lines.push(frame);
	});
	const request = (frame: Json) => new Promise<Json>(resolve => { const id = ++next; pending.set(id, resolve); write({ id, ...frame }); });
	// One call at a time, as the node does.
	let turn: Promise<unknown> = Promise.resolve();
	const call = (name: string, args: Json = null) => {
		const run = async () => {
			let reply = await request({ call: name, args });
			while (reply.ask) {
				const served = await answer(reply);
				reply = await request({ answer: reply.ask, result: served.result, error: served.error });
			}
			if (reply.error !== undefined) throw new Error(reply.error);
			return reply.result;
		};
		const result = turn.then(run);
		turn = result.catch(() => {});
		return result;
	};
	const pump = createReadStream(await call("pump"), { encoding: "utf8" });
	void each(pump, async line => {
		if (line.id !== undefined) write(await answer(line));
		else { lines.push(line); await serve(line); }
	});
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
		close: async () => { pump.destroy(); child.kill(); await child.exited; },
	};
}
