import { afterEach, beforeEach, expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { atomic, document, edit, git, scan } from '../../src/records';
import { execute } from '../../src/engine';
import { completionProblem, lane } from '../../src/lifecycle';
import { plan } from '../../src/planner';
import { runProcess } from '../../src/process';
import { Service } from '../../src/service';

let root: string, records: string, board: string, code: string, previousAdapter: string | undefined;
function repository(dir: string) {
  fs.mkdirSync(dir, { recursive: true }); git(dir, ['init', '-q']); git(dir, ['config', 'user.name', 'Parity fixture']); git(dir, ['config', 'user.email', 'fixture@example.invalid']);
  atomic(path.join(dir, 'seed.txt'), 'seed\n'); git(dir, ['add', '.']); git(dir, ['commit', '-qm', 'baseline']); return dir;
}
function item(name: string, state = 'open', owner = board, source = code, footprint = 'seed.txt') {
  const file = path.join(owner, 'prds', name, 'prd.md');
  atomic(file, `---\nstate: ${state}\nrepo: ${JSON.stringify(source)}\nfootprint: ${JSON.stringify([footprint])}\n---\n\n# ${name}\n`); return file;
}
function contract(file: string, open = false, command = 'test "$(cat seed.txt)" = seed') {
  const target = path.join(path.dirname(file), 'specs/spec01.md');
  atomic(target, `---\nfootprint: [seed.txt]\n---\n\n# Contract\n\n## Acceptance\n\n- [${open ? ' ' : 'x'}] Verified output\n\n## Verify\n\n\`\`\`sh\n${command}\n\`\`\`\n`); return target;
}
function adapter(script: string) {
  const dir = path.join(root, 'adapters'), worker = path.join(root, 'worker.ts'); atomic(worker, script);
  atomic(path.join(dir, 'fixture.json'), JSON.stringify({ command: [process.execPath, worker, '{board}', '{rel}'] })); process.env.PRD_ADAPTER_DIR = dir;
}
beforeEach(() => {
  previousAdapter = process.env.PRD_ADAPTER_DIR; root = fs.mkdtempSync(path.join(os.tmpdir(), 'prd-parity-'));
  records = repository(path.join(root, 'records')); code = repository(path.join(root, 'code')); board = path.join(records, '.cartridge/boards/root');
  atomic(path.join(board, 'settings.md'), `---\nname: root\nrepo: ${JSON.stringify(code)}\nrequire-repo: true\n---\n`);
  atomic(path.join(records, '.gitignore'), '**/.state/\n**/.lanes/\n');
});
afterEach(() => { if (previousAdapter === undefined) delete process.env.PRD_ADAPTER_DIR; else process.env.PRD_ADAPTER_DIR = previousAdapter; fs.rmSync(root, { recursive: true, force: true }); });

test('plan addresses round-trip and member children inherit their actual source owner', async () => {
  const member = path.join(path.dirname(board), 'member'), other = repository(path.join(root, 'other'));
  atomic(path.join(member, 'settings.md'), `---\nname: member\nrepo: ${JSON.stringify(other)}\n---\n`);
  edit(path.join(board, 'settings.md'), { members: [{ member: '../member' }] }); item('parent', 'open', member, other); item('root-task');
  const added = await execute('add', board, ['Small child', '--parent', '@member/parent']); expect(added.error).toBe('');
  expect(added.changed[0].ref).toBe('@member/parent/small-child'); expect(added.changed[0].after.repo).toBe(fs.realpathSync(other));
  for (const selected of [board, member]) for (const row of plan(selected).rows) {
    const read = await execute('read', selected, [row.addr]); expect(read.error, row.addr).toBe('');
    if (row.dispatchable) expect((await execute('claim', selected, [row.addr, 'fixture', '--dry'])).error).toBe('');
  }
});

test('parent proof validates child contracts and current source across repositories', async () => {
  const other = repository(path.join(root, 'other')); item('parent'); const child = item('parent/child', 'specced', board, other); const spec = contract(child);
  git(records, ['add', '.']); git(records, ['commit', '-qm', 'contracts']);
  expect((await execute('claim', board, ['parent/child', 'fixture'])).error).toBe('');
  expect((await execute('collect', board, ['parent/child'])).error).toBe('');
  const collected = await execute('collect', board, ['parent']); expect(collected.error).toBe(''); expect(collected.verification[0].verified).toBe(true);
  expect(completionProblem(scan(board).get('parent')!)).toBeNull();
  const original = fs.readFileSync(spec, 'utf8'); atomic(spec, original + '\nChanged acceptance contract.\n');
  expect(completionProblem(scan(board).get('parent')!)).toContain('changed'); atomic(spec, original);
  atomic(path.join(other, 'seed.txt'), 'uncommitted break\n'); expect(completionProblem(scan(board).get('parent')!)).toContain('source footprint changed');
  atomic(path.join(other, 'seed.txt'), 'seed\n'); expect(completionProblem(scan(board).get('parent')!)).toBeNull();
});

test('unverified pre-existing done records fail and persist their reason', async () => {
  item('forged', 'done'); adapter('throw Error("No worker should run");');
  const answer = await execute('run', board, ['--adapter', 'fixture']);
  expect(answer.exit_code).toBe(2); expect(answer.data.status).toBe('failed'); expect(answer.data.failed[0].ref).toBe('forged');
  const checkpoint = JSON.parse(fs.readFileSync(path.join(board, '.state/run.json'), 'utf8'));
  expect(checkpoint.status).toBe('failed'); expect(checkpoint.failed[0].reason).toContain('contract');
});

const implementation = `import fs from 'node:fs'; import path from 'node:path';
const [board, rel] = process.argv.slice(2); if(rel === 'bad') process.exit(0);
const file=path.join(board,'prds',rel,'specs/spec01.md'); fs.writeFileSync('seed.txt','changed\\n'); fs.writeFileSync(file,fs.readFileSync(file,'utf8').replace('- [ ]','- [x]'));
`;
test('coordinator independently collects a finished owned claim and preserves foreign claims', async () => {
  contract(item('good', 'specced'), true, 'test "$(cat seed.txt)" = changed');
  const foreign = item('foreign', 'claimed', board, code, 'foreign.txt'); edit(foreign, { claim: 'other-worker' });
  adapter(implementation); const answer = await execute('run', board, ['good', '--adapter', 'fixture', '--deadline', '10']);
  expect(answer.error).toBe(''); expect(answer.data.status).toBe('completed'); expect(answer.verification[0].verified).toBe(true);
  expect(scan(board).get('good')!.fm.claim).toBeUndefined(); expect(document(foreign).fm.claim).toBe('other-worker');
});

test('partly failed runs publish only independently verified successful receipts to memory', async () => {
  contract(item('good', 'specced'), true, 'test "$(cat seed.txt)" = changed'); item('bad', 'open', board, code, 'bad.txt'); adapter(implementation);
  const writes: any[] = [], service = new Service({ root: records, adapter: 'fixture', job_timeout_seconds: 10 }, { publish() {}, async call(name, args) { expect(name).toBe('memory'); writes.push(args); return { status: 'committed' }; } });
  try {
    const context = { session: 'parity', run: 'partial', call: 'one', cwd: code };
    const started = await service.dispatch({ op: 'call', context, input: { op: 'run', args: ['--workers', '2'] } }); expect(started.error).toBe(false);
    await Promise.allSettled([...service.tasks]); const job = [...service.jobs.values()][0];
    expect(job.state).toBe('failed'); expect(job.verification).toHaveLength(1); expect(job.verification[0].ref).toBe('good'); expect(job.memory.status).toBe('committed');
    expect(writes).toHaveLength(1); expect(writes[0].raw).toBe(true); expect(writes[0].text).toContain('good');
    const oversized = service.publicJob({ ...job, changed: Array(10000).fill({ ref: '日本語'.repeat(100) }) });
    expect(Buffer.byteLength(JSON.stringify(oversized))).toBeLessThanOrEqual(service.outputCap); expect(oversized.changed_count).toBe(10000);
  } finally { await service.close(); }
}, 20000);

for (const cancel of [false, true]) test(`owned descendants are confirmed stopped after ${cancel ? 'cancellation' : 'normal leader exit'}`, async () => {
  const pidFile = path.join(root, 'child.pid');
  const childSource = `process.on('SIGTERM',()=>{});require('fs').writeFileSync(${JSON.stringify(pidFile)},String(process.pid));setInterval(()=>{},1000);`;
  const leader = `const fs=require('fs'),cp=require('child_process');cp.spawn(process.execPath,['-e',${JSON.stringify(childSource)}],{stdio:'ignore'}).unref();const timer=setInterval(()=>{if(fs.existsSync(${JSON.stringify(pidFile)})){clearInterval(timer);${cancel ? 'setInterval(()=>{},1000)' : 'process.exit(0)'}}},10);`;
  const controller = new AbortController(); let pid = 0;
  try {
    const work = runProcess([process.execPath, '-e', leader], { cwd: root, signal: controller.signal, timeout: 3000, grace: 60 });
    for (let i = 0; !fs.existsSync(pidFile) && i < 200; i++) await Bun.sleep(10);
    pid = Number(fs.readFileSync(pidFile, 'utf8')); expect(pid).toBeGreaterThan(1); if (cancel) controller.abort();
    const result = await work; expect(result.state).toBe(cancel ? 'cancelled' : 'completed');
    const state = Bun.spawnSync(['ps', '-o', 'stat=', '-p', String(pid)]).stdout.toString().trim(); expect(state === '' || state.startsWith('Z')).toBe(true);
  } finally { if (pid > 1) { try { process.kill(pid, 'SIGKILL'); } catch {} } }
}, 10000);

test('collection refuses a contract changed by its own verification before committing code', async () => {
  const file = item('changing', 'specced');
  const target = path.join(path.dirname(file), 'specs/spec01.md');
  const script = `printf '\\nReplaced while verifying\\n' >> ${JSON.stringify(target)}\nprintf changed > seed.txt`;
  contract(file, false, script); const head = git(code, ['rev-parse', 'HEAD']);
  const answer = await execute('collect', board, ['changing']);
  expect(answer.exit_code).toBe(2); expect(answer.error).toContain('contract changed during verification');
  expect(git(code, ['rev-parse', 'HEAD'])).toBe(head); expect(scan(board).get('changing')!.state).toBe('specced');
}, 15000);

for (const change of ['modify', 'delete', 'rename', 'leading-space']) test(`collection rejects already committed out-of-footprint ${change}`, async () => {
  atomic(path.join(code, 'outside.txt'), 'keep\n'); git(code, ['add', '.']); git(code, ['commit', '-qm', 'outside baseline']);
  contract(item('scoped', 'specced'));
  expect((await execute('claim', board, ['scoped', 'fixture'])).exit_code).toBe(0);
  const tree = lane(scan(board).get('scoped')!).directory, head = git(code, ['rev-parse', 'HEAD']);
  if (change === 'modify') atomic(path.join(tree, 'outside.txt'), 'unapproved\n');
  else if (change === 'delete') fs.unlinkSync(path.join(tree, 'outside.txt'));
  else if (change === 'leading-space') atomic(path.join(tree, ' seed.txt'), 'unapproved\n');
  else fs.renameSync(path.join(tree, 'outside.txt'), path.join(tree, 'seed.txt'));
  git(tree, ['add', '.']); git(tree, ['commit', '-qm', 'worker changes']);
  const answer = await execute('collect', board, ['scoped']);
  expect(answer.exit_code).toBe(2); expect(answer.error).toContain('committed path is outside');
  expect(git(code, ['rev-parse', 'HEAD'])).toBe(head); expect(fs.readFileSync(path.join(code, 'outside.txt'), 'utf8')).toBe('keep\n');
  expect(scan(board).get('scoped')!.state).toBe('claimed'); expect(fs.existsSync(tree)).toBe(true);
}, 15000);

test('all serialized tool results obey the byte cap and retain omitted diagnostics', async () => {
  const service = new Service({ root: records, max_output_bytes: 1024 });
  try {
    const answer = await service.dispatch({ op: 'call', context: { session: 's', run: 'r', call: 'c', cwd: code }, input: { op: 'read', args: ['one', '--' + '界'.repeat(2000)] } });
    expect(Buffer.byteLength(JSON.stringify(answer))).toBeLessThanOrEqual(1024); expect(answer.error).toBe(true);
    const summary = JSON.parse(answer.content);
    const retained = JSON.parse(fs.readFileSync(path.join(service.state, 'responses', summary.response_id + '.json'), 'utf8'));
    expect(JSON.parse(retained.content).error).toContain('界'.repeat(2000));
    const escaped = service.result({ state: 'completed', output: '"'.repeat(600) });
    expect(Buffer.byteLength(JSON.stringify(escaped))).toBeLessThanOrEqual(1024); expect(JSON.parse(escaped.content).truncated).toBe(true);
  } finally { await service.close(); }
});

test('planned waves honor member capacity with disjoint footprints', () => {
  const member = path.join(path.dirname(board), 'member');
  atomic(path.join(member, 'settings.md'), `---\nname: member\nrepo: ${JSON.stringify(code)}\nworkers: 1\n---\n`);
  edit(path.join(board, 'settings.md'), { members: [{ member: '../member' }] });
  item('one', 'open', member, code, 'one.txt'); item('two', 'open', member, code, 'two.txt'); item('root', 'open', board, code, 'root.txt');
  const planned = plan(board, 3); expect(planned.waves).toHaveLength(2);
  expect(planned.waves.every(w => w.filter(a => a.startsWith('@member/')).length <= 1)).toBe(true);
});
