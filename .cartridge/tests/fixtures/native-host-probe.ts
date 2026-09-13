import { createInterface } from 'node:readline';
import { HostBridge } from '../../../src/service';
if (process.argv[2] === 'hello') {
  console.log(JSON.stringify({ inject: ['prd', 'memory'], provide: ['native-host-probe'] }));
  process.exit(0);
}
const send = (message: unknown) => console.log(JSON.stringify(message));
const bridge = new HostBridge(send), events: any[] = [], tasks: Promise<void>[] = [];
for await (const line of createInterface({ input: process.stdin })) {
  const message = JSON.parse(line);
  if (bridge.accept(message)) continue;
  if (message.dispose) break;
  if (message.apply) { send({ provide: 'native-host-probe' }); send({ subscribe: 'prd' }); send({ ready: true }); }
  else if (message.call === 'native-host-probe') tasks.push((async () => {
    try {
      const request = (op: string, args: string[]) => bridge.request('prd', {
        op: 'call', context: { session: 'native-host-fixture', run: 'isolated', call: op, cwd: message.args.cwd }, input: { op, args },
      }, undefined, 30000);
      const seed = await bridge.request('memory', { op: 'ingest', text: 'The release code name is Cedar.', raw: true, sync: true });
      const read = await request('read', ['example']);
      const collected = await request('collect', ['example']);
      const recalled = await bridge.request('memory', { op: 'query', text: 'Verified PRD collection', k: 10 });
      send({ reply: message.id, data: { seed, read, collected, recalled, events } });
    } catch (error) { send({ reply: message.id, error: String(error) }); }
  })());
  else events.push(message.event ?? message);
}
bridge.close(); await Promise.allSettled(tasks);
