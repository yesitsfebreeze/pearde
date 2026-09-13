import { createInterface } from 'node:readline';
import { HostBridge } from '../../../src/service';
if (process.argv[2] === 'hello') { console.log(JSON.stringify({ inject: ['prd', 'memory'], provide: ['probe'] })); process.exit(0); }
const send = (m: any) => console.log(JSON.stringify(m)), bridge = new HostBridge(send), events: any[] = [];
const tasks: Promise<any>[] = [];
for await (const line of createInterface({ input: process.stdin })) {
  const message = JSON.parse(line);
  if (bridge.accept(message)) continue;
  if (message.dispose) break;
  if (message.apply) { send({ provide: 'probe' }); send({ subscribe: 'prd' }); send({ ready: true }); }
  else if (message.call === 'probe') tasks.push((async () => {
    const call = (op: string, args: string[], id: string) => bridge.request('prd', { op: 'call', context: { session: 'test', run: 'one', call: id, cwd: message.args.cwd }, input: { op, args } }, undefined, 10000);
    try { const read = await call('read', ['example'], 'read'), added = await call('add', ['Native runtime event probe'], 'add'); const memory_calls = await bridge.request('memory', { op: 'fixture_calls' }); send({ reply: message.id, data: { read, added, memory_calls, events } }); }
    catch (error) { send({ reply: message.id, error: String(error) }); }
  })());
  else events.push(message.event ?? message);
}
bridge.close(); await Promise.allSettled(tasks);
