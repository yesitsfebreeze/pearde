import { expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { runProcess } from '../../src/process';
import { Service } from '../../src/service';
import { atomic, git, scan } from '../../src/records';
import { completionProblem } from '../../src/lifecycle';

// Actual per-invocation Unix socket writes, including backpressure.
const writer = `const net = require('node:net'), { once } = require('node:events');
if (!process.env.PRD_NATIVE_EVENT_SOCKET) throw Error('missing dedicated event socket');
const socket = net.createConnection(process.env.PRD_NATIVE_EVENT_SOCKET);
await once(socket, 'connect');
async function bytes(value) {
  if (!socket.write(value)) await once(socket, 'drain');
}
async function emit(value) { await bytes(JSON.stringify(value)+'\\n'); }
`;
async function child(source: string, onEvent: (event: any) => void) {
  return runProcess([process.execPath, '-e', writer + 'try {\n' + source + '\n} finally { socket.end(); }'], { cwd: os.tmpdir(), timeout: 5000, onEvent });
}

test('event socket drains complete Unicode frames and the final event before process completion', async () => {
  const events: any[] = [];
  const result = await child(`const packet=Buffer.from(JSON.stringify({type:'fixture.progress',i:0,text:'日本語'})+'\\n');
const split=packet.indexOf(Buffer.from('日'))+1; await bytes(packet.subarray(0,split)); await Bun.sleep(25); await bytes(packet.subarray(split));
for(let i=1;i<40;i++) await emit({type:'fixture.progress',i,text:'日本語'});
await emit({type:'fixture.finished',last:true}); console.log('ordinary output');`, event => events.push(event));
  expect(result.state).toBe('completed'); expect(result.exit_code).toBe(0); expect(result.output.trim()).toBe('ordinary output');
  expect(events).toHaveLength(41); expect(events[0].text).toBe('日本語'); expect(events.at(-1)).toEqual({ type: 'fixture.finished', last: true });
  expect(result.events?.received).toBe(41); expect(result.events?.dropped).toBe(0); expect(result.events?.error).toBeUndefined();
});

test('event socket rejects malformed and oversized Unicode frames while retaining later valid events', async () => {
  const events: any[] = [];
  const result = await child(`await bytes('{malformed}\\n');
await emit({type:'fixture.oversized',text:'界'.repeat(3000)});
await emit({type:'fixture.finished'});`, event => events.push(event));
  expect(result.state).toBe('completed'); expect(events).toEqual([{ type: 'fixture.finished' }]);
  expect(result.events?.dropped).toBeGreaterThanOrEqual(2); expect(result.events?.error).toBeTruthy();
});

test('event socket callback failures are reported and do not prevent draining later events', async () => {
  const events: any[] = [];
  const result = await child(`await emit({type:'fixture.throw'}); await emit({type:'fixture.finished'});`, event => {
    if (event.type === 'fixture.throw') throw Error('fixture callback rejection'); events.push(event);
  });
  expect(result.state).toBe('completed'); expect(events).toEqual([{ type: 'fixture.finished' }]);
  expect(result.events?.dropped).toBeGreaterThanOrEqual(1); expect(result.events?.error).toContain('fixture callback rejection');
});

for (const mode of ['count', 'bytes']) test(`event socket ${mode} budget is bounded while excess frames are drained`, async () => {
  const events: any[] = [];
  const result = await child(mode === 'count'
    ? `for(let i=0;i<1500;i++) await emit({type:'fixture.burst',i}); console.log('drained');`
    : `for(let i=0;i<100;i++) await emit({type:'fixture.burst',i,text:'x'.repeat(4000)}); console.log('drained');`, event => events.push(event));
  expect(result.state, JSON.stringify(result)).toBe('completed'); expect(result.output.trim()).toBe('drained');
  expect(events.length).toBeGreaterThan(0); expect(events.length).toBeLessThanOrEqual(mode === 'count' ? 256 : 16);
  expect(result.events?.dropped).toBeGreaterThan(0);
});

function repository(directory: string) {
  fs.mkdirSync(directory, { recursive: true }); git(directory, ['init', '-q']); git(directory, ['config', 'user.name', 'Event fixture']); git(directory, ['config', 'user.email', 'fixture@example.invalid']);
  atomic(path.join(directory, 'seed.txt'), 'seed\n'); git(directory, ['add', '.']); git(directory, ['commit', '-qm', 'baseline']); return directory;
}
test('real service run streams attributed domain events before returning bounded verified completion', async () => {
  const root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-event-stream-'));
  const previous = process.env.PRD_ADAPTER_DIR;
  let service: Service | undefined;
  try {
    const records = repository(path.join(root, 'records')), code = repository(path.join(root, 'code')), board = path.join(records, '.cartridge/boards/root');
    atomic(path.join(records, '.gitignore'), '**/.state/\n**/.lanes/\n');
    atomic(path.join(board, 'settings.md'), `---\nname: fixture\nrepo: ${JSON.stringify(code)}\nrequire-repo: true\n---\n`);
    atomic(path.join(board, 'prds/one/prd.md'), `---\nstate: specced\nrepo: ${JSON.stringify(code)}\nfootprint: [seed.txt]\n---\n\n# One\n`);
    atomic(path.join(board, 'prds/one/specs/spec01.md'), '---\nfootprint: [seed.txt]\n---\n\n# Contract\n\n## Acceptance\n\n- [ ] Source changed\n\n## Verify\n\n```sh\ntest "$(cat seed.txt)" = changed\n```\n');
    git(records, ['add', '.']); git(records, ['commit', '-qm', 'contract']);
    const worker = path.join(root, 'worker.ts');
    atomic(worker, `import fs from 'node:fs'; import path from 'node:path';
const [board, rel] = process.argv.slice(2);
fs.writeFileSync('seed.txt','changed\\n');
const file=path.join(board,'prds',rel,'specs/spec01.md'); fs.writeFileSync(file,fs.readFileSync(file,'utf8').replace('- [ ]','- [x]'));
`);
    process.env.PRD_ADAPTER_DIR = path.join(root, 'adapters');
    atomic(path.join(process.env.PRD_ADAPTER_DIR, 'fixture.json'), JSON.stringify({ command: [process.execPath, worker, '{board}', '{rel}'] }));
    const events: { channel: string; event: any; whileRunning: boolean }[] = [];
    service = new Service({ root: records, adapter: 'fixture', job_timeout_seconds: 10 }, {
      publish(channel, event) { events.push({ channel, event, whileRunning: [...service!.jobs.values()].some(job => job.state === 'running') }); },
      async call() { return { status: 'committed' }; },
    });
    const context = { session: 'trusted-session', run: 'trusted-run', call: 'trusted-call', cwd: code };
    const started = await service.dispatch({ op: 'call', context, input: { op: 'run', args: ['--workers', '1'] } });
    expect(started.error).toBe(false); await Promise.allSettled([...service.tasks]);
    const job = [...service.jobs.values()][0]; expect(job.state, JSON.stringify(job)).toBe('completed');
    const domain = events.filter(row => !row.event.type.startsWith('command.'));
    for (const type of ['plan.updated', 'worker.started', 'worker.finished', 'transition.applied', 'verification.completed'])
      expect(domain.some(row => row.event.type === type), JSON.stringify({ domain, diagnostics: job.events })).toBe(true);
    expect(domain.some(row => row.whileRunning)).toBe(true);
    for (const row of domain) {
      expect(row.event.session).toBe(context.session); expect(row.event.run).toBe(context.run); expect(row.event.call).toBe(context.call);
      expect(row.event.board).toBe('root'); expect(row.event.operation).toBe('run'); expect(row.channel).toBe('prd');
    }
    expect(job.events.received).toBeGreaterThan(0); expect(job.events.published).toBe(domain.length); expect(job.events.unavailable).toBe(0);
    expect(Buffer.byteLength(JSON.stringify(service.publicJob(job)))).toBeLessThanOrEqual(service.outputCap);
    expect(completionProblem(scan(board).get('one')!)).toBeNull();
    service.host = { publish() { throw Error('fixture event host unavailable'); }, async call() { return {}; } };
    const fallback = await service.dispatch({ op: 'call', context: { ...context, call: 'delivery-failure' }, input: { op: 'plan', args: [] } });
    expect(fallback.error).toBe(false);
    const outcome = JSON.parse(fallback.content);
    expect(outcome.events.unavailable).toBeGreaterThan(0); expect(outcome.events.published).toBe(0);
  } finally {
    await service?.close(); if (previous === undefined) delete process.env.PRD_ADAPTER_DIR; else process.env.PRD_ADAPTER_DIR = previous;
    fs.rmSync(root, { recursive: true, force: true });
  }
}, 20000);
