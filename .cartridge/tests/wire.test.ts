import { expect, test } from "bun:test";
import { PassThrough } from "node:stream";
import { Wire } from "../../src/wire";

/** Plays the node: calls by id; asks on stdout are served and answered on stdin; other lines are collected. */
function node(input: PassThrough, output: PassThrough, serve: (line: any) => any) {
	let next = 0;
	const pending = new Map<number, (frame: any) => void>();
	const loose: any[] = [];
	const write = (frame: any) => input.write(JSON.stringify(frame) + "\n");
	let buffer = "";
	output.on("data", chunk => {
		buffer += String(chunk);
		for (let at; (at = buffer.indexOf("\n")) >= 0; buffer = buffer.slice(at + 1)) {
			const frame = JSON.parse(buffer.slice(0, at));
			const waiter = pending.get(frame.id);
			if (waiter) waiter(frame);
			else if (frame.ask !== undefined) {
				try { write({ ask: frame.ask, result: serve(frame) }); }
				catch (error) { write({ ask: frame.ask, error: String((error as Error).message) }); }
			} else loose.push(frame);
		}
	});
	const call = async (name: string, args: any = null) => {
		const reply = await new Promise<any>(resolve => { const id = ++next; pending.set(id, resolve); write({ id, call: name, args }); });
		if (reply.error !== undefined) throw new Error(reply.error);
		return reply.result;
	};
	return { call, loose, send: (frame: any) => write(frame) };
}

test("a call is answered by id, asks are served on stdin, and the program's own lines pass through", async () => {
	const input = new PassThrough(), output = new PassThrough();
	const wire = new Wire(input, output);
	const served: any[] = [];
	const host = node(input, output, line => {
		served.push(line);
		if (line.bail === "twice") return line.args * 2;
		if (line.host === "status") return { ok: true };
		throw new Error("unknown");
	});
	wire.on("apply", async config => config.name);
	wire.on("double", async n => wire.call("twice", n));
	wire.on("boom", async () => { throw new Error("no"); });
	expect(await host.call("apply", { name: "fixture" })).toBe("fixture");
	expect(await host.call("double", 21)).toBe(42);
	expect(served).toMatchObject([{ ask: "a1", bail: "twice", args: 21 }]);
	await expect(host.call("boom")).rejects.toThrow("no");
	await expect(host.call("missing")).rejects.toThrow("not served here");
	// Between calls the program asks and emits on its own.
	expect(await wire.host("status")).toEqual({ ok: true });
	await expect(wire.call("nothing", 1)).rejects.toThrow("unknown");
	wire.emit("ticked", { n: 1 });
	wire.notify("told", 2);
	wire.publish("chan", 3);
	await Bun.sleep(10);
	expect(host.loose).toEqual([{ emit: "ticked", data: { n: 1 } }, { notify: "told", data: 2 }, { publish: "chan", data: 3 }]);
	// An event without an id is handled and never answered.
	wire.on("agent.event", async event => { served.push(event); });
	host.send({ call: "agent.event", args: { kind: "text" } });
	await Bun.sleep(10);
	expect(served.at(-1)).toEqual({ kind: "text" });
	let closed = false;
	wire.onClose(() => { closed = true; });
	await wire.close();
	expect(closed).toBe(true);
});
