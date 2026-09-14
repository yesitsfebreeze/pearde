import { afterEach, beforeEach, expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { Service, HostBridge } from '../../src/service';
import { atomic, git } from '../../src/records';
let root: string, board: string, service: Service;
const context = (session = 'one', call = randomUUID()) => ({ session, run: 'run', call, cwd: root });
const value = (answer: any) => JSON.parse(answer.content);
const call = (op: string, args: string[] = [], ctx = context(), extra = {}) => service.dispatch({ op: 'call', context: ctx, input: { op, args, ...extra } });
beforeEach(() => {
  root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-service-'));
  git(root, ['init', '-q']); board = path.join(root, '.cartridge/boards/root');
  atomic(path.join(board, 'settings.md'), `---\nname: root\nrepo: ${JSON.stringify(root)}\n---\n`);
  atomic(path.join(board, 'prds/one/prd.md'), '---\nstate: open\n---\n\n# One\n');
  service = new Service({ root, timeout_seconds: 2, job_timeout_seconds: 3, max_output_bytes: 8192 });
});
afterEach(async () => { await service.close(); fs.rmSync(root, { recursive: true, force: true }); });
test('real service describes and dispatches the native planner', async () => {
  expect((await service.dispatch({ op: 'describe' })).name).toBe('prd');
  const answer = await call('plan', ['--workers', '2']); expect(answer.error).toBe(false); expect(value(answer).data.slots).toBe(2); expect(value(answer).memory.status).toBe('unavailable');
});
test('context and closed model input cannot override execution', async () => {
  for (const ctx of [{}, { ...context(), cwd: 'relative' }, { ...context(), extra: true }, { ...context(), session: '' }]) expect((await call('scan', [], ctx as any)).error).toBe(true);
  for (const extra of [{ cwd: '/tmp' }, { context: context() }, { command: 'touch unwanted' }]) expect((await call('scan', [], context(), extra)).error).toBe(true);
  expect(fs.existsSync(path.join(root, 'unwanted'))).toBe(false);
});
test('argument whitelist refuses injected paths, flags, adapters and excess counts', async () => {
  const cases = [['scan', '--board', '/tmp'], ['plan', 'all'], ['read', '../other'], ['read', '/etc/passwd'], ['run', '--adapter', 'evil'], ['brief', 'one', '--transcript', '/tmp'], ['collect', 'one', '--trust'], ['plan', '--workers', '100'], ['plan', '--workers', '1.5'], ['read', 'one', 'two'], ['add', 'hello', '--body', '-'], ['scan', '--limit', '51']];
  for (const [op, ...args] of cases) expect((await call(op, args)).error).toBe(true);
  expect((await call('scan', ['x'.repeat(8193)])).error).toBe(true);
});
test('board and PRD symlinks cannot escape central records', async () => {
  const outside = path.join(root, 'outside'); fs.mkdirSync(outside); fs.symlinkSync(outside, path.join(path.dirname(board), 'escape'));
  for (const name of ['escape', '../outside', '/tmp', '.', 'root/../root']) expect((await call('scan', [], context(), { board: name })).error).toBe(true);
  fs.symlinkSync(outside, path.join(board, 'prds/escape')); expect((await call('read', ['escape'])).error).toBe(true);
});
test('duplicate invocation does not repeat a mutation and cancellation leaves a tombstone', async () => {
  const ctx = context(); expect((await call('add', ['New item'], ctx)).error).toBe(false); expect((await call('add', ['New item'], ctx)).error).toBe(true);
  const cancelled = context(); await service.dispatch({ op: 'cancel', context: cancelled }); expect(value(await call('scan', [], cancelled)).state).toBe('cancelled');
});
test('memory is attributed context and successful mutations publish scoped events', async () => {
  const calls: any[] = [], events: any[] = [];
  service.host = { request: async (name, args, turn) => { calls.push({ name, args, turn }); return { items: [{ id: 'fact', text: 'prior evidence' }] }; }, publish: (event, turn) => { events.push({ event, turn }); } };
  const answer = value(await call('read', ['one'])); expect(answer.memory.provider).toBe('memory'); expect(answer.memory.authority).toContain('context only');
  expect(calls[0].args.op).toBe('query');
  await service.dispatch({ op: 'call', context: context(), input: { op: 'claim', args: ['one', 'worker'] } }, 'turn-1');
  const completed = events.find(e => e.event.type === 'command.completed');
  expect(completed.event.refs).toEqual(['one']); expect(completed.turn).toBe('turn-1'); expect(completed.event.output).toBeUndefined();
});
test('only verified evidence enters the durable memory outbox with bounded retry', async () => {
  expect((await service.rememberVerified(board, context(), {})).status).toBe('not_recorded');
  const proof = { verification: [{ verified: true, ref: 'one', revision: 'a'.repeat(64), state: 'done' }] };
  let answer; for (let i = 0; i < 5; i++) answer = await service.rememberVerified(board, context(), proof);
  expect(answer.status).toBe('pending'); expect(answer.attempts).toBe(3);
});
test('memory replay acknowledges once and deduplicates simultaneous deliveries', async () => {
  const proof = { verification: [{ verified: true, ref: 'one', revision: 'a'.repeat(64), state: 'done' }] };
  await service.rememberVerified(board, context(), proof); let ingests = 0;
  service.host = { request: async () => { ingests++; await Bun.sleep(20); return { status: 'committed' }; }, publish: () => {} };
  await Promise.all([service.replayMemory(), service.rememberVerified(board, context(), proof)]);
  expect((await service.rememberVerified(board, context(), proof)).status).toBe('committed'); expect(ingests).toBe(1);
});
test('asynchronous jobs enforce session ownership and never signal stale journals', async () => {
  expect((await call('run')).error).toBe(true); service.adapter = 'unused';
  const started = value(await call('run', ['--dry'])); expect(started.state).toBe('running');
  expect((await call('status', [started.job_id], context('other'))).error).toBe(true);
  expect((await call('stop', [started.job_id], context('other'))).error).toBe(true);
  await call('stop', [started.job_id]);
  await service.close(); const journal = JSON.parse(fs.readFileSync(path.join(service.state, started.job_id + '.json'), 'utf8')); expect(journal.state).toBe('cancelled');
  const restarted = new Service({ root });
  try { expect((await restarted.dispatch({ op: 'call', context: context(), input: { op: 'stop', args: [started.job_id] } })).error).toBe(true); }
  finally { await restarted.close(); }
});
test('host bridge correlates replies and closes pending requests', async () => {
  const sent: any[] = [], bridge = new HostBridge(m => sent.push(m));
  const first = bridge.request('memory', { op: 'query' }, 'turn'); expect(sent[0].turn).toBe('turn');
  bridge.accept({ reply: sent[0].id, data: { ok: true } }); expect(await first).toEqual({ ok: true });
  const second = bridge.request('memory', {}); bridge.close(); await expect(second).rejects.toThrow('disconnected');
});
test('wire hello, apply, describe, native call, reload and dispose', async () => {
  const executable = path.resolve(import.meta.dir, '../../src/service.ts');
  const hello = Bun.spawnSync([process.execPath, executable, 'hello']); expect(JSON.parse(hello.stdout.toString()).provide).toEqual(['prd', 'tool.prd', 'source.board']);
  const child = Bun.spawn([process.execPath, executable], { stdin: 'pipe', stdout: 'pipe', stderr: 'pipe' });
  const reader = child.stdout.getReader(), decoder = new TextDecoder(); let buffer = '';
  async function receive(): Promise<any> { for (;;) { const newline = buffer.indexOf('\n'); if (newline >= 0) { const line = buffer.slice(0, newline); buffer = buffer.slice(newline + 1); return JSON.parse(line); } const chunk = await reader.read(); if (chunk.done) throw Error('wire ended'); buffer += decoder.decode(chunk.value, { stream: true }); } }
  const send = (v: any) => child.stdin.write(JSON.stringify(v) + '\n');
  try {
    send({ apply: { config: { root } } }); expect(await receive()).toEqual({ provide: 'prd' }); expect(await receive()).toEqual({ provide: 'tool.prd' }); expect(await receive()).toEqual({ provide: 'source.board' }); expect(await receive()).toEqual({ on: 'fabric.announce' }); expect(await receive()).toEqual({ ready: true });
    send({ id: 1, call: 'prd', args: { op: 'describe' } }); expect((await receive()).data.name).toBe('prd');
    // The announce: this cartridge contributes its own tool to the graph.
    send({ id: 9, event: 'fabric.announce', data: { scope: {} } }); const announced = await receive(); expect(announced.reply).toBe(9); expect(announced.data.nodes).toEqual([{ kind: 'tool', key: 'tool.prd', name: 'prd', description: expect.any(String) }]);
    send({ id: 2, call: 'prd', args: { op: 'call', context: context(), input: { op: 'scan' } } }); expect((await receive()).data.error).toBe(false);
    send({ id: 3, call: 'prd', turn: 'turn-3', args: { op: 'call', context: context(), input: { op: 'read', args: ['one'] } } });
    const query = await receive(); expect(query.call).toBe('memory'); expect(query.turn).toBe('turn-3'); send({ reply: query.id, data: { items: [] } }); expect(value((await receive()).data).memory.status).toBe('available');
    send({ id: 4, reload: true }); expect(await receive()).toEqual({ reply: 4, data: null }); send({ dispose: true }); expect(await child.exited).toBe(0);
  } finally { child.kill(); child.stdin.end(); reader.releaseLock(); }
}, 10000);
