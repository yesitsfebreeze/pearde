import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execute } from '../../src/engine';
import { atomic, document, edit, git, hash, scan, withLocks } from '../../src/records';
import { plan } from '../../src/planner';
import { completionProblem, lane } from '../../src/lifecycle';
import { runProcess } from '../../src/process';

let root: string, board: string, code: string;
const cli = path.resolve(import.meta.dir, '../../src/cli.ts');
function init(repo: string) {
  fs.mkdirSync(repo, { recursive: true }); git(repo, ['init', '-q']); git(repo, ['config', 'user.email', 'test@example.invalid']); git(repo, ['config', 'user.name', 'Test']);
  atomic(path.join(repo, 'seed.txt'), 'seed\n'); git(repo, ['add', '.']); git(repo, ['commit', '-qm', 'seed']);
}
function prd(name: string, state = 'open', owner = board, needs: string[] = [], footprint = name + '.txt') {
  const file = path.join(owner, 'prds', name, 'prd.md');
  atomic(file, `---\nstate: ${state}\nrepo: ${JSON.stringify(code)}\ncomplexity: 2\npriority: 50\nneeds: ${JSON.stringify(needs)}\nfootprint: ${JSON.stringify([footprint])}\n---\n\n# ${name}\n\nA bounded fixture outcome.\n`);
  return file;
}
function spec(file: string, command = 'test "$(cat seed.txt)" = changed') {
  const target = path.join(path.dirname(file), 'specs/spec01.md');
  atomic(target, `---\ncomplexity: 2\nfootprint: [seed.txt]\n---\n\n# Spec\n\n## Acceptance\n\n- [x] Source changed\n\n## Verify and Proof\n\n\`\`\`sh\n${command}\n\`\`\`\n`);
  return target;
}
beforeEach(() => {
  root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-native-'));
  code = path.join(root, 'code'); init(code); const records = path.join(root, 'records'); init(records);
  board = path.join(records, '.cartridge/boards/root');
  atomic(path.join(board, 'settings.md'), `---\nname: fixture\nrepo: ${JSON.stringify(code)}\nrequire-repo: true\nworkers: 2\n---\n`);
  atomic(path.join(records, '.gitignore'), '**/.state/\n**/.lanes/\n');
});
afterEach(() => { fs.rmSync(root, { recursive: true, force: true }); });

test('scan preserves prose, counts members once and resolves cross-owner prerequisites', async () => {
  const member = path.join(path.dirname(board), 'member');
  atomic(path.join(member, 'settings.md'), '---\nname: member\n---\n');
  edit(path.join(board, 'settings.md'), { members: [{ member: '../member' }] });
  prd('one', 'open', member); prd('two', 'open', board, ['@member/one']);
  expect(scan(board).size).toBe(2);
  expect(plan(board).rows.find(p => p.rel === 'two')?.held).toContain('not done');
  expect((await execute('claim', board, ['@member/one', 'worker'])).exit_code).toBe(0);
  expect(document(path.join(member, 'prds/one/prd.md')).fm.state).toBe('analyzing');
});
test('isolated member cannot claim an unscanned prerequisite', async () => {
  prd('one', 'open', board, ['@outside/task']);
  const answer = await execute('claim', board, ['one', 'worker']);
  expect(answer.exit_code).toBe(2); expect(answer.error).toContain('outside this graph'); expect(answer.changed).toEqual([]);
});
test('dependency cycles and held footprints are not dispatchable', async () => {
  prd('one', 'open', board, ['two']); prd('two', 'open', board, ['one']);
  expect(plan(board).notes[0]).toContain('cycle'); expect(plan(board).rows.every(r => !r.dispatchable)).toBe(true);
  edit(path.join(board, 'prds/one/prd.md'), { needs: [], footprint: ['shared'] });
  edit(path.join(board, 'prds/two/prd.md'), { needs: [], footprint: ['shared/child'] });
  expect(plan(board).waves.length).toBe(2);
  expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(0);
  expect((await execute('claim', board, ['two', 'other'])).error).toContain('footprint');
});
test('pagination and planning do not mutate source records', async () => {
  prd('one'); prd('two'); const before = fs.readFileSync(path.join(board, 'prds/one/prd.md'));
  const answer = await execute('plan', board, ['--limit', '1', '--workers', '2']);
  expect(answer.data.total).toBe(2); expect(answer.data.next_offset).toBe(1); expect(answer.changed).toEqual([]);
  expect(fs.readFileSync(path.join(board, 'prds/one/prd.md'))).toEqual(before);
});
test('claim is serialized across processes and board aliases', async () => {
  const member = path.join(path.dirname(board), 'member'); atomic(path.join(member, 'settings.md'), '---\nname: member\n---\n');
  edit(path.join(board, 'settings.md'), { members: [{ member: '../member' }] }); prd('one', 'open', member);
  const results = await Promise.all([[board, '@member/one'], [member, 'one']].map(async ([owner, ref], i) => {
    const child = Bun.spawn([process.execPath, cli, 'claim', ref, 'worker-' + i, '--board', owner, '--json']);
    const output = await new Response(child.stdout).json(); await child.exited; return output;
  }));
  expect(results.map(r => r.exit_code).sort()).toEqual([0, 2]); expect(results.find(r => r.exit_code)?.changed).toEqual([]);
});
test('edits preserve unrelated fields, comments and body and reject stale revisions', () => {
  const file = prd('one'); const text = fs.readFileSync(file, 'utf8').replace('priority: 50', '# authored comment\npriority: 50'); atomic(file, text);
  edit(file, { state: 'analyzing', claim: 'worker' }, hash(text));
  const current = fs.readFileSync(file, 'utf8'); expect(current).toContain('# authored comment'); expect(current).toContain('A bounded fixture outcome.'); expect(document(file).fm.priority).toBe(50);
  expect(() => edit(file, { state: 'done' }, hash(text))).toThrow('changed');
});
test('PRD symlinks and oversized reads are refused', async () => {
  prd('one'); fs.symlinkSync(code, path.join(board, 'prds/escape')); expect(() => scan(board)).toThrow('escapes'); fs.unlinkSync(path.join(board, 'prds/escape'));
  atomic(path.join(board, 'huge.md'), 'x'.repeat(1048577)); expect((await execute('read', board, ['huge.md'])).error).toContain('1 MiB');
});
test('invalid source mapping and missing specs cannot create a lane', async () => {
  const file = prd('one', 'specced'); expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(2);
  spec(file); edit(file, { repo: path.join(root, 'missing') }); expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(2);
  expect(fs.existsSync(path.join(board, '.lanes/one'))).toBe(false);
});
test('real collect verifies an isolated lane and commits integration evidence', async () => {
  const file = prd('one', 'specced', board, [], 'seed.txt'); spec(file);
  git(path.join(root, 'records'), ['add', '.']); git(path.join(root, 'records'), ['commit', '-qm', 'records']);
  const claimed = await execute('claim', board, ['one', 'worker']); expect(claimed.error).toBe('');
  const work = lane(scan(board).get('one')!); atomic(path.join(work.directory, 'seed.txt'), 'changed\n');
  const answer = await execute('collect', board, ['one']); expect(answer.error).toBe(''); expect(answer.exit_code).toBe(0);
  expect(fs.readFileSync(path.join(code, 'seed.txt'), 'utf8')).toBe('changed\n'); expect(answer.verification[0].verified).toBe(true);
  expect(completionProblem(scan(board).get('one')!)).toBeNull();
  atomic(path.join(path.dirname(file), 'specs/spec01.md'), fs.readFileSync(path.join(path.dirname(file), 'specs/spec01.md'), 'utf8') + '\nChanged proof.\n');
  expect(completionProblem(scan(board).get('one')!)).toContain('changed');
});
test('failed proof preserves source HEAD and never marks done', async () => {
  const file = prd('one', 'specced', board, [], 'seed.txt'); spec(file, 'exit 17'); const head = git(code, ['rev-parse', 'HEAD']);
  await execute('claim', board, ['one', 'worker']); const answer = await execute('collect', board, ['one']);
  expect(answer.exit_code).toBe(2); expect(git(code, ['rev-parse', 'HEAD'])).toBe(head); expect(scan(board).get('one')!.state).toBe('claimed');
});
test('forged done state and old commit cannot substitute for collection evidence', () => {
  const file = prd('one', 'done'); edit(file, { commit: git(code, ['rev-parse', 'HEAD']) }); expect(completionProblem(scan(board).get('one')!)).not.toBeNull();
});
test('run dry needs no adapter and failed workers are not treated as completion', async () => {
  prd('one'); expect((await execute('run', board, ['--dry'])).data.status).toBe('preview');
  const adapters = path.join(root, 'adapters'); atomic(path.join(adapters, 'test.json'), JSON.stringify({ command: [process.execPath, '-e', 'process.exit(0)'] }));
  const previous = process.env.PRD_ADAPTER_DIR; process.env.PRD_ADAPTER_DIR = adapters;
  try { const answer = await execute('run', board, ['--adapter', 'test', '--deadline', '2']); expect(answer.data.failed[0].reason).toContain('without persisted'); expect(scan(board).get('one')!.state).toBe('analyzing'); }
  finally { if (previous === undefined) delete process.env.PRD_ADAPTER_DIR; else process.env.PRD_ADAPTER_DIR = previous; }
});
test('deadline kills owned worker groups and leaves a stopped checkpoint', async () => {
  prd('one'); const adapters = path.join(root, 'adapters'); atomic(path.join(adapters, 'test.json'), JSON.stringify({ command: [process.execPath, '-e', 'setTimeout(()=>{},30000)'] }));
  const previous = process.env.PRD_ADAPTER_DIR; process.env.PRD_ADAPTER_DIR = adapters;
  try { const answer = await execute('run', board, ['--adapter', 'test', '--deadline', '0.15']); expect(answer.data.status).toBe('stopped'); expect(JSON.parse(fs.readFileSync(path.join(board, '.state/run.json'), 'utf8')).live).toEqual([]); }
  finally { if (previous === undefined) delete process.env.PRD_ADAPTER_DIR; else process.env.PRD_ADAPTER_DIR = previous; }
});
test('process timeout remains enforced after stdout closes', async () => {
  const started = Date.now();
  const answer = await runProcess([process.execPath, '-e', 'require("fs").closeSync(1); require("fs").closeSync(2); setTimeout(()=>{},30000)'], { cwd: root, timeout: 100 });
  expect(answer.state).toBe('timed_out'); expect(Date.now() - started).toBeLessThan(3000);
});
test('process output has a hard byte limit', async () => {
  const answer = await runProcess([process.execPath, '-e', 'console.log("x".repeat(100000))'], { cwd: root, cap: 1024 });
  expect(answer.state).toBe('output_limit'); expect(Buffer.byteLength(answer.output)).toBeLessThanOrEqual(1024);
});
test('rolling coordinator rescans analysis, dependencies and parent collection', async () => {
  prd('parent'); prd('parent/one', 'open', board, [], 'parent-one.txt');
  prd('two', 'open', board, ['parent'], 'two.txt');
  git(path.join(root, 'records'), ['add', '.']); git(path.join(root, 'records'), ['commit', '-qm', 'fixture']);
  const adapters = path.join(root, 'adapters');
  atomic(path.join(adapters, 'test.json'), JSON.stringify({ command: [process.execPath, path.join(import.meta.dir, 'fixtures/worker.ts'), '{board}', '{rel}'] }));
  const previous = process.env.PRD_ADAPTER_DIR; process.env.PRD_ADAPTER_DIR = adapters;
  try {
    const answer = await execute('run', board, ['--adapter', 'test', '--workers', '2', '--deadline', '20']);
    expect(answer.data.failed).toEqual([]); expect(answer.data.status).toBe('completed');
    expect(answer.verification.length).toBe(3); expect(answer.verification.every((p: any) => p.verified)).toBe(true);
  } finally { if (previous === undefined) delete process.env.PRD_ADAPTER_DIR; else process.env.PRD_ADAPTER_DIR = previous; }
}, 30000);
const tamper = (file: string, from: RegExp, to: string) => fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace(from, to));
test('hand edits to state or claim are reported and refused until adopted', async () => {
  const file = prd('one'); expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(0);
  expect((await execute('check', board)).data.problems).toEqual([]);
  tamper(file, /state: "analyzing"\n/, 'state: open\n'); tamper(file, /claim: .*\n/, '');
  const checked = await execute('check', board);
  expect(checked.exit_code).toBe(2); expect(checked.data.problems.join('\n')).toMatch(/^one: state changed outside the engine.*claim changed.*prd adopt one --by <id> --reason "<text>" --board .*adoption is recorded/m);
  for (const [op, args] of [['claim', ['one', 'other']], ['release', ['one', 'open']], ['collect', ['one']], ['specced', ['one']], ['refine', ['one']]] as const) {
    const answer = await execute(op, board, [...args]); expect(answer.exit_code).toBe(2); expect(answer.error).toContain('one: state changed outside the engine');
  }
  expect((await execute('adopt', board, ['one'])).error).toContain('--by');
  expect((await execute('adopt', board, ['one', '--by', 'coordinator'])).error).toContain('--reason');
  const adopted = await execute('adopt', board, ['one', '--by', 'coordinator', '--reason', 'reset by analyst']);
  expect(adopted.exit_code).toBe(0); expect(adopted.output).toContain('"state":"analyzing"'); expect(adopted.output).toContain('"state":"open"');
  const log = fs.readFileSync(path.join(board, '.state/fields/adopted.log'), 'utf8').trim().split('\n').map(line => JSON.parse(line));
  expect(log).toHaveLength(1); expect(log[0]).toMatchObject({ ref: 'one', by: 'coordinator', reason: 'reset by analyst', old: { state: 'analyzing' }, new: { state: 'open', claim: null } });
  expect((await execute('check', board)).data).toMatchObject({ problems: [], warnings: [] });
  expect((await execute('claim', board, ['one', 'other'])).exit_code).toBe(0);
});
test('a hand-written commit is reported', async () => {
  const file = prd('one'); expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(0);
  tamper(file, /\n---\n/, '\ncommit: "abc1234"\n---\n');
  expect((await execute('check', board)).data.problems.join('\n')).toMatch(/^one: commit changed outside the engine \(recorded null, found "abc1234"\)/m);
});
test('an adopted claim that changed hands warns until it is released', async () => {
  const file = prd('one'); expect((await execute('claim', board, ['one', 'alice'])).exit_code).toBe(0);
  tamper(file, /claim: .*\n/, 'claim: "mallory now"\n');
  expect((await execute('adopt', board, ['one', '--by', 'bob', '--reason', 'handover'])).exit_code).toBe(0);
  const checked = await execute('check', board);
  expect(checked.exit_code).toBe(0); expect(checked.data.warnings.join('\n')).toMatch(/^one: claim changed hands by adoption .*by bob .*handover/m);
  expect((await execute('release', board, ['one', 'open'])).exit_code).toBe(0);
  expect((await execute('check', board)).data.warnings).toEqual([]);
});
test('a PRD re-added at a removed path inherits no recorded values', async () => {
  expect((await execute('add', board, ['one'])).exit_code).toBe(0); expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(0);
  fs.rmSync(path.join(board, 'prds/one'), { recursive: true });
  expect((await execute('check', board)).data.problems).toEqual([]); expect(fs.existsSync(path.join(board, '.state/fields/one.json'))).toBe(false);
  expect((await execute('add', board, ['one'])).exit_code).toBe(0); expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(0);
  fs.rmSync(path.join(board, 'prds/one'), { recursive: true });
  expect((await execute('add', board, ['one'])).exit_code).toBe(0);
  expect((await execute('check', board)).data.problems).toEqual([]); expect((await execute('claim', board, ['one', 'other'])).exit_code).toBe(0);
});
test('dropping the values of a removed or rehomed record is logged and warned once', async () => {
  expect((await execute('add', board, ['one'])).exit_code).toBe(0);
  expect((await execute('claim', board, ['one', 'alice'])).exit_code).toBe(0);
  fs.renameSync(path.join(board, 'prds/one'), path.join(board, 'prds/two'));
  const moved = path.join(board, 'prds/two/prd.md');
  tamper(moved, /state: .*\n/, 'state: open\n'); tamper(moved, /claim: .*\n/, '');
  const checked = await execute('check', board);
  expect(checked.exit_code).toBe(0); expect(checked.data.problems).toEqual([]);
  expect(checked.data.warnings.join('\n')).toMatch(/^one: prds\/one\/prd\.md is gone; recorded .*"analyzing".*"alice.*dropped and logged in .*adopted\.log/m);
  const log = fs.readFileSync(path.join(board, '.state/fields/adopted.log'), 'utf8').trim().split('\n').map(line => JSON.parse(line));
  expect(log).toHaveLength(1); expect(log[0]).toMatchObject({ local: 'one', dropped: { state: 'analyzing' } });
  expect((await execute('check', board)).data.warnings).toEqual([]);
  expect((await execute('add', board, ['three'])).exit_code).toBe(0);
  fs.rmSync(path.join(board, 'prds/three'), { recursive: true });
  expect((await execute('check', board)).data.warnings).toEqual([]);
  // A member board left with no record of its own is still swept: rehoming its last PRD to the root board
  // must not hide the drop just because nothing on that board survives in the graph.
  const member = path.join(path.dirname(board), 'member');
  atomic(path.join(member, 'settings.md'), '---\nname: member\n---\n');
  edit(path.join(board, 'settings.md'), { members: [{ member: '../member' }] });
  prd('m1', 'open', member);
  expect((await execute('claim', member, ['m1', 'alice'])).exit_code).toBe(0);
  fs.renameSync(path.join(member, 'prds/m1'), path.join(board, 'prds/m1'));
  const rehomed = path.join(board, 'prds/m1/prd.md');
  tamper(rehomed, /state: .*\n/, 'state: open\n'); tamper(rehomed, /claim: .*\n/, '');
  const swept = await execute('check', board);
  expect(swept.exit_code).toBe(0); expect(swept.data.problems).toEqual([]);
  expect(swept.data.warnings.join('\n')).toMatch(/^m1: prds\/m1\/prd\.md is gone; recorded .*"analyzing".*"alice.*dropped and logged in .*adopted\.log/m);
  expect(fs.existsSync(path.join(member, '.state/fields/m1.json'))).toBe(false);
  expect(fs.readFileSync(path.join(member, '.state/fields/adopted.log'), 'utf8')).toContain('"local":"m1"');
  expect((await execute('check', board)).data.warnings).toEqual([]);
});
test('check reports an unwritable field store instead of a raw errno', async () => {
  expect((await execute('add', board, ['one'])).exit_code).toBe(0);
  const fields = path.join(board, '.state/fields'); fs.rmSync(path.join(fields, 'one.json'));
  fs.chmodSync(fields, 0o555);
  try {
    const checked = await execute('check', board);
    expect(checked.exit_code).toBe(2); expect(checked.data.problems.join('\n')).toContain('the engine field store is unavailable (EACCES)');
  } finally { fs.chmodSync(fields, 0o755); }
});
test('body edits, untracked records and engine transitions raise no field problem', async () => {
  const file = prd('one'); prd('two', 'claimed');
  expect((await execute('check', board)).data.problems).toEqual([]);
  expect((await execute('claim', board, ['one', 'worker'])).exit_code).toBe(0);
  edit(file, { footprint: ['elsewhere.txt'] }); fs.appendFileSync(file, '\nMore prose.\n');
  expect((await execute('release', board, ['one', 'open'])).exit_code).toBe(0);
  expect((await execute('check', board)).data).toMatchObject({ problems: [], warnings: [] });
});
