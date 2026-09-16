import { afterEach, beforeEach, expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { Service } from '../../src/service';
import { program } from './fixtures/host';
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
  service.host = { call: async (name, args) => { calls.push({ name, args }); return { items: [{ id: 'fact', text: 'prior evidence' }] }; }, publish: (channel, event) => { events.push({ channel, event }); } };
  const answer = value(await call('read', ['one'])); expect(answer.memory.provider).toBe('memory'); expect(answer.memory.authority).toContain('context only');
  expect(calls[0].args.op).toBe('query');
  await service.dispatch({ op: 'call', context: context(), input: { op: 'claim', args: ['one', 'worker'] } });
  const completed = events.find(e => e.event.type === 'command.completed');
  expect(completed.event.refs).toEqual(['one']); expect(completed.channel).toBe('prd'); expect(completed.event.output).toBeUndefined();
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
  service.host = { call: async () => { ingests++; await Bun.sleep(20); return { status: 'committed' }; }, publish: () => {} };
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
test('memory calls are bounded so a stalled provider never holds up planning', async () => {
  service.host = { call: () => new Promise(() => {}), publish: () => {} };
  const started = Date.now(); const answer = value(await call('read', ['one']));
  expect(answer.memory.status).toBe('unavailable'); expect(answer.memory.error).toContain('timed out'); expect(Date.now() - started).toBeLessThan(6000);
}, 10000);
test('wire apply, describe, graph announce, native call with memory, and dispose', async () => {
  const requests: any[] = [];
  const service = await program([process.execPath, path.resolve(import.meta.dir, '../../src/service.ts')], line => {
    if (line.bail === 'memory') { requests.push(line); return { items: [] }; }
    throw Error('unexpected ask ' + JSON.stringify(line));
  });
  try {
    expect(await service.call('apply', { root })).toBeNull();
    expect((await service.call('prd', { op: 'describe' })).name).toBe('prd');
    // The announce: this cartridge contributes its own tool to the graph.
    expect(await service.call('graph.announce', { scope: {} })).toEqual({ nodes: [{ kind: 'tool', key: 'tool.prd', name: 'prd', description: expect.any(String) }], edges: [] });
    expect((await service.call('prd', { op: 'call', context: context(), input: { op: 'scan' } })).error).toBe(false);
    const read = await service.call('prd', { op: 'call', context: context(), input: { op: 'read', args: ['one'] } });
    expect(value(read).memory.status).toBe('available');
    expect(requests).toMatchObject([{ bail: 'memory', args: { op: 'query' } }]);
    expect(await service.call('dispose')).toBe(true);
  } finally { await service.close(); }
}, 10000);
test('the job journal is keyed by node, so a second attached instance never interrupts a live job', async () => {
  service.adapter = 'unused';
  const instance = (run: string) => ({ session: 'shared', run, call: randomUUID(), cwd: root });
  const first = value(await call('run', ['--dry'], instance('one')));
  // A second attached instance calls in while the first job is still on the books.
  const second = value(await call('run', ['--dry'], instance('two')));
  expect((await call('scan', [], instance('two'))).error).toBe(false);
  // The job key is the node's service instance, not the invocation that started it.
  for (const started of [first, second]) {
    expect(service.jobs.get(started.job_id).instance).toBe(service.instance);
    expect(JSON.parse(fs.readFileSync(path.join(service.state, started.job_id + '.json'), 'utf8')).instance).toBe(service.instance);
    expect(value(await call('status', [started.job_id], instance('three'))).state).not.toBe('interrupted');
  }
  // A journal entry from a service that really did end still reports interrupted.
  const stale = { job_id: 'f'.repeat(32), session: 'shared', instance: 'a-previous-service', invocation: '[]', board: 'root', state: 'running', started_at: 0 };
  atomic(path.join(service.state, stale.job_id + '.json'), JSON.stringify(stale));
  expect(value(await call('status', [stale.job_id], instance('four'))).state).toBe('interrupted');
});
test('the memory outbox replays once per pending acknowledgment however many instances call in', async () => {
  const proof = { verification: [{ verified: true, ref: 'one', revision: 'b'.repeat(64), state: 'done' }] };
  let ingests = 0;
  service.host = { call: async () => { ingests++; await Bun.sleep(20); return { status: 'committed' }; }, publish: () => {} };
  const one = { session: 'shared', run: 'one', call: randomUUID(), cwd: root };
  const two = { session: 'other', run: 'two', call: randomUUID(), cwd: root };
  // Two attached instances land the same verified evidence at once, and the node replays alongside them.
  const [from1, from2] = await Promise.all([service.rememberVerified(board, one, proof), service.rememberVerified(board, two, proof), service.replayMemory()]);
  expect(ingests).toBe(1);
  expect(from1.status).toBe('committed'); expect(from2.status).toBe('committed');
  expect(fs.readdirSync(path.join(service.state, 'memory-outbox')).length).toBe(1);
  // A committed acknowledgment is never sent again, by replay or by a later instance.
  await service.replayMemory();
  expect((await service.rememberVerified(board, two, proof)).status).toBe('committed');
  expect(ingests).toBe(1);
});
test('a second apply is refused, so one process serves from exactly one service', async () => {
  const node = await program([process.execPath, path.resolve(import.meta.dir, '../../src/service.ts')], line => {
    if (line.bail === 'memory') return { items: [] };
    throw Error('unexpected ask ' + JSON.stringify(line));
  });
  try {
    expect(await node.call('apply', { root })).toBeNull();
    await expect(node.call('apply', { root })).rejects.toThrow('cartridge is already applied');
    // The refusal neither replaced nor closed the one service: it still serves.
    expect((await node.call('prd', { op: 'call', context: context(), input: { op: 'scan' } })).error).toBe(false);
  } finally { await node.close(); }
}, 10000);
