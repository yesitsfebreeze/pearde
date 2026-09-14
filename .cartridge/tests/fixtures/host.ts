// Plays the cartridge host for one cartridge process over the transport wire.
import net from "node:net";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

export const HOST_TOKEN = "fixture-host-token";

type Rpc = { call(method: string, params?: any): Promise<any>; close(): void };

function lines(socket: net.Socket, frame: (message: any) => void) {
  let buffer = "";
  socket.setEncoding("utf8");
  socket.on("data", chunk => {
    buffer += chunk;
    for (let at; (at = buffer.indexOf("\n")) >= 0; buffer = buffer.slice(at + 1)) frame(JSON.parse(buffer.slice(0, at)));
  });
}

/** A socket path and the environment the host would start a cartridge with. */
export function environment() {
  const socket = join(mkdtempSync(join(tmpdir(), "cartridge-fixture-")), "c.sock");
  return { socket, env: { ...process.env, CARTRIDGE_SOCKET: socket, CARTRIDGE_HOST_TOKEN: HOST_TOKEN } };
}

/** Connect to a cartridge once it listens and authenticate as the host. */
export async function connect(path: string): Promise<Rpc> {
  // Polled rather than retried: a refused connect fails the test under `bun test` even when caught.
  for (let attempt = 0; !existsSync(path); attempt++) {
    if (attempt > 200) throw new Error(`nothing listens on ${path}`);
    await Bun.sleep(20);
  }
  const socket = await new Promise<net.Socket>(resolve => { const s = net.connect(path, () => resolve(s)); });
  let next = 0;
  const pending = new Map<number, { resolve: (v: any) => void; reject: (e: Error) => void }>();
  lines(socket, message => {
    const waiter = pending.get(message.id);
    pending.delete(message.id);
    message.error ? waiter?.reject(Object.assign(new Error(message.error.message), { code: message.error.code })) : waiter?.resolve(message.result);
  });
  const rpc: Rpc = {
    call: (method, params = null) => new Promise((resolve, reject) => {
      const id = ++next;
      pending.set(id, { resolve, reject });
      socket.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
    }),
    close: () => socket.destroy(),
  };
  await rpc.call("auth", { token: HOST_TOKEN });
  return rpc;
}

/** A socket standing in for another cartridge (or the host) that a cartridge reaches; `auth` is accepted for any token. */
export function peer(cartridge: string, answer: (method: string, params: any) => any) {
  const socket = join(mkdtempSync(join(tmpdir(), "cartridge-peer-")), "peer.sock");
  const server = net.createServer(connection => lines(connection, async message => {
    const reply = (body: object) => connection.write(JSON.stringify({ jsonrpc: "2.0", id: message.id, ...body }) + "\n");
    try { reply({ result: message.method === "auth" ? { cartridge } : await answer(message.method, message.params) ?? null }); }
    catch (error) { reply({ error: { code: -32000, message: String(error) } }); }
  })).listen(socket);
  return { address: { cartridge, socket, token: "fixture-cartridge-token" }, close: () => server.close() };
}
