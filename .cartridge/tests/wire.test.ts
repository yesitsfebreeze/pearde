import { expect, test } from "bun:test";
import { createReadStream } from "node:fs";
import { PassThrough } from "node:stream";
import { Wire } from "../../src/wire";

/** Plays init.lua: a call is one request; an ask on its answer line is served and continued with `answer`. */
function lua(wire: Wire, input: PassThrough, output: PassThrough, serve: (line: any) => any) {
	let next = 0;
	const pending = new Map<number, (frame: any) => void>();
	const loose: any[] = [];
	let buffer = "";
	output.on("data", chunk => {
		buffer += String(chunk);
		for (let at; (at = buffer.indexOf("\n")) >= 0; buffer = buffer.slice(at + 1)) {
			const frame = JSON.parse(buffer.slice(0, at));
			const waiter = pending.get(frame.id);
			waiter ? waiter(frame) : loose.push(frame);
		}
	});
	const request = (frame: any) => new Promise<any>(resolve => { const id = ++next; pending.set(id, resolve); input.write(JSON.stringify({ id, ...frame }) + "\n"); });
	const call = async (name: string, args: any = null) => {
		let reply = await request({ call: name, args });
		while (reply.ask) reply = await request({ answer: reply.ask, result: serve(reply) });
		if (reply.error !== undefined) throw new Error(reply.error);
		return reply.result;
	};
	return { call, loose, send: (frame: any) => input.write(JSON.stringify(frame) + "\n") };
}

test("a call is answered by id, its asks ride the answer lines, and the pump carries the program's own lines", async () => {
	const input = new PassThrough(), output = new PassThrough();
	const wire = new Wire(input, output);
	const served: any[] = [];
	const host = lua(wire, input, output, line => { served.push(line); return line.bail === "twice" ? line.args * 2 : null; });
	wire.on("apply", async config => config.name);
	wire.on("double", async n => wire.call("twice", n));
	wire.on("boom", async () => { throw new Error("no"); });
	expect(await host.call("apply", { name: "fixture" })).toBe("fixture");
	expect(await host.call("double", 21)).toBe(42);
	expect(served).toMatchObject([{ ask: "a1", bail: "twice", args: 21 }]);
	await expect(host.call("boom")).rejects.toThrow("no");

	const pump = createReadStream(await host.call("pump"), { encoding: "utf8" });
	const lines: any[] = [];
	pump.on("data", chunk => { for (const line of String(chunk).split("\n")) if (line) lines.push(JSON.parse(line)); });
	wire.emit("ticked", { n: 1 });
	const asked = wire.call("twice", 4);
	for (let i = 0; i < 100 && lines.length < 2; i++) await Bun.sleep(10);
	expect(lines).toEqual([{ event: "ticked", data: { n: 1 } }, { id: "a2", bail: "twice", args: 4 }]);
	host.send({ id: "a2", result: 8 });
	expect(await asked).toBe(8);
	// An event without an id is handled and never answered.
	wire.on("agent.event", async event => { served.push(event); });
	host.send({ call: "agent.event", args: { kind: "text" } });
	await Bun.sleep(10);
	expect(served.at(-1)).toEqual({ kind: "text" });
	expect(host.loose).toEqual([]);
	await wire.close();
	pump.destroy();
});
