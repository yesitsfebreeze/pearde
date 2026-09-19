import { afterEach, beforeEach, expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execute } from '../../src/engine';
import { atomic, document, edit, git, scan } from '../../src/records';
import { lane, verifiedStatus } from '../../src/lifecycle';

let root: string, code: string, records: string, board: string;
const q = (value: string) => "'" + value.replaceAll("'", "'\\''") + "'";
function init(repo: string) {
  fs.mkdirSync(repo, { recursive: true }); git(repo, ['init', '-q']); git(repo, ['config', 'user.email', 'test@example.invalid']); git(repo, ['config', 'user.name', 'Test']);
  atomic(path.join(repo, '.gitignore'), '**/.state/\n**/.lanes/\n'); atomic(path.join(repo, 'seed.txt'), 'good\n');
  git(repo, ['add', '.']); git(repo, ['commit', '-qm', 'seed']);
}
function row(name = 'one', command = 'test "$(cat seed.txt)" = good', needs: string[] = []) {
  const file = path.join(board, 'prds', name, 'prd.md');
  atomic(file, `---\nstate: specced\nrepo: ${JSON.stringify(code)}\nneeds: ${JSON.stringify(needs)}\nfootprint: [seed.txt, README.md, help.md]\n---\n# ${name}\n\n## Acceptance\n- [x] Contract holds.\n`);
  atomic(path.join(path.dirname(file), 'specs/spec01.md'), `---\nfootprint: [seed.txt, README.md, help.md]\n---\n# Contract\n\n## Acceptance\n- [x] Proof passes.\n\n## Verify\n\n\`\`\`sh\n${command}\n\`\`\`\n`);
  return file;
}
const record = (name = 'one') => scan(board).get(name)!;
const receipt = (name = 'one') => path.join(record(name).dir, 'collection.md');
async function collect(name = 'one', ...args: string[]) {
  const result = await execute('collect', board, [name, ...args]);
  expect(result.error).toBe(''); expect(result.exit_code).toBe(0); return result;
}
function commit(repo: string, file: string, contents: string) { atomic(path.join(repo, file), contents); git(repo, ['add', '--', file]); git(repo, ['commit', '-qm', 'change', '--', file]); }
beforeEach(() => {
  root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-proof-')); code = path.join(root, 'code'); records = path.join(root, 'records'); init(code); init(records);
  board = path.join(records, '.cartridge/boards/root'); atomic(path.join(board, 'settings.md'), `---\nrepo: ${JSON.stringify(code)}\n---\n`);
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

test('explicit reverify refreshes committed drift and preserves prior receipt', async () => {
  row('one', 'test -s seed.txt'); await collect(); const prior = fs.readFileSync(receipt(), 'utf8'), original = record().fm.commit;
  commit(code, 'seed.txt', 'later\n'); expect((await execute('collect', board, ['one'])).error).toContain('footprint changed');
  const result = await collect('one', '--reverify'); const proof = document(receipt());
  expect(proof.fm.commit).toBe(git(code, ['rev-parse', 'HEAD'])); expect(proof.fm['original-commit']).toBe(original);
  expect(fs.readFileSync(path.join(record().dir, 'collection-history', proof.fm['previous-receipt'] + '.md'), 'utf8')).toBe(prior);
  expect(result.verification[0].verification_target).toBe('committed'); expect(verifiedStatus(record()).verified).toBe(true);
  await collect('one', '--reverify'); expect(fs.readdirSync(path.join(record().dir, 'collection-history'))).toHaveLength(2);
});

test('reverify refuses changed contract missing proof and active ownership', async () => {
  row(); await collect(); const prior = fs.readFileSync(receipt(), 'utf8'), spec = path.join(record().dir, 'specs/spec01.md'), original = fs.readFileSync(spec, 'utf8');
  fs.appendFileSync(spec, '\nChanged contract.\n'); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('specification changed'); atomic(spec, original);
  fs.rmSync(receipt()); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('no recorded'); atomic(receipt(), prior);
  fs.mkdirSync(lane(record()).directory, { recursive: true }); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('active lane'); fs.rmdirSync(lane(record()).directory);
  edit(record().file, { claim: 'other' }); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('still has a claim'); expect(fs.readFileSync(receipt(), 'utf8')).toBe(prior);
});

test('reverify refuses unresolved dependencies and failing proof', async () => {
  row('dep'); await collect('dep'); row('one', 'test "$(cat seed.txt)" = good', ['dep']); await collect(); const prior = fs.readFileSync(receipt(), 'utf8');
  commit(code, 'seed.txt', 'bad\n'); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('dependency');
  expect((await execute('collect', board, ['dep', '--reverify'])).error).toContain('verification'); expect(fs.readFileSync(receipt(), 'utf8')).toBe(prior); expect(verifiedStatus(record()).verified).toBe(false);
});

test('committed collection preserves dirty tails and reports workspace drift', async () => {
  commit(code, 'README.md', 'committed readme\n'); commit(code, 'help.md', 'committed help\n'); row('one', 'test -s seed.txt');
  expect((await execute('claim', board, ['one', 'implementer'])).error).toBe('');
  atomic(path.join(lane(record()).directory, 'seed.txt'), 'implemented in lane\n');
  atomic(path.join(code, 'README.md'), 'committed readme\npreserved dirty tail\n'); atomic(path.join(code, 'help.md'), 'committed help\npreserved help tail\n');
  const before = git(code, ['rev-parse', 'HEAD']), result = await collect('one', '--committed');
  expect(git(code, ['rev-parse', 'HEAD'])).not.toBe(before); expect(fs.readFileSync(path.join(code, 'seed.txt'), 'utf8')).toBe('implemented in lane\n'); expect(fs.readFileSync(path.join(code, 'README.md'), 'utf8')).toContain('preserved dirty tail'); expect(fs.readFileSync(path.join(code, 'help.md'), 'utf8')).toContain('preserved help tail');
  expect(result.verification[0].verified).toBe(true); expect(result.verification[0].workspace_verified).toBe(false);
  expect(result.verification[0].workspace_drift.map((item: any) => item.path)).toEqual(['README.md', 'help.md']);
  expect(git(code, ['diff', '--cached', '--name-only'])).toBe(''); expect(result.output).toContain('verification_target=committed, workspace_verified=false');
});

test('legacy receipts remain strict and later committed drift needs reverify', async () => {
  row('legacy', 'test -s seed.txt'); await collect('legacy'); atomic(path.join(code, 'seed.txt'), 'dirty\n');
  expect(verifiedStatus(record('legacy')).verified).toBe(false); await collect('legacy', '--reverify'); expect(verifiedStatus(record('legacy')).verified).toBe(true); expect(verifiedStatus(record('legacy')).workspace_verified).toBe(false);
  commit(code, 'seed.txt', 'later committed\n'); expect(verifiedStatus(record('legacy')).verified).toBe(false); await collect('legacy', '--reverify'); expect(verifiedStatus(record('legacy')).workspace_verified).toBe(true);
  expect((await execute('status', board, ['--committed'])).error).toContain('require collect');
});

test('reverification refreshes child rollups without automatic vouchers', async () => {
  const parent = path.join(board, 'prds/parent/prd.md'); atomic(parent, `---\nstate: open\nrepo: ${JSON.stringify(code)}\n---\n# Parent\n`);
  row('parent/child', 'test -s seed.txt'); await collect('parent/child', '--committed'); await collect('parent', '--committed'); const old = fs.readFileSync(receipt('parent'), 'utf8');
  commit(code, 'seed.txt', 'later\n'); expect((await execute('collect', board, ['parent', '--reverify'])).error).toContain('footprint');
  await collect('parent/child', '--reverify'); expect(verifiedStatus(record('parent')).verified).toBe(false); await collect('parent', '--reverify'); expect(verifiedStatus(record('parent')).verified).toBe(true);
  expect(fs.readFileSync(receipt('parent'), 'utf8')).not.toBe(old); atomic(path.join(code, 'seed.txt'), 'dirty\n'); expect(verifiedStatus(record('parent')).workspace_verified).toBe(false);
  const legacy = path.join(board, 'prds/legacy-parent/prd.md'); atomic(legacy, `---\nstate: open\nrepo: ${JSON.stringify(code)}\n---\n# Legacy parent\n`);
  row('legacy-parent/child', 'test -s seed.txt'); await collect('legacy-parent/child', '--committed');
  expect((await execute('collect', board, ['legacy-parent'])).error).toContain('child workspace differs');
}, 20000);

test('verification races cancellation and history tampering fail closed', async () => {
  const marker = path.join(root, 'race'); row('one', `test -s seed.txt\nif test -f ${q(marker)}; then git -C ${q(code)} -c user.name=Test -c user.email=test@example.invalid commit --allow-empty -qm race; fi`); await collect(); const prior = fs.readFileSync(receipt(), 'utf8');
  atomic(marker, 'race'); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('HEAD changed'); expect(fs.readFileSync(receipt(), 'utf8')).toBe(prior); fs.rmSync(marker);
  const cancel = new AbortController(); cancel.abort(); expect((await execute('collect', board, ['one', '--reverify'], cancel.signal)).error).toContain('cancelled'); expect(fs.readFileSync(receipt(), 'utf8')).toBe(prior);
  const hook = path.join(records, '.git/hooks/pre-commit'); atomic(hook, '#!/bin/sh\nexit 1\n'); fs.chmodSync(hook, 0o755);
  expect((await execute('collect', board, ['one', '--reverify'])).exit_code).toBe(2); expect(fs.readFileSync(receipt(), 'utf8')).toBe(prior); expect(git(records, ['diff', '--cached', '--name-only'])).toBe(''); fs.rmSync(hook);
  await collect('one', '--reverify'); const archive = path.join(record().dir, 'collection-history', document(receipt()).fm['previous-receipt'] + '.md'); fs.appendFileSync(archive, 'tampered'); expect(verifiedStatus(record()).verified).toBe(false); expect((await execute('collect', board, ['one', '--reverify'])).error).toContain('history');
  expect(git(code, ['worktree', 'list']).split('\n')).toHaveLength(1);
});

test('committed verification tests committed bytes rather than dirty workspace', async () => {
  commit(code, 'seed.txt', 'bad\n'); row(); atomic(path.join(code, 'seed.txt'), 'good\n'); const before = git(code, ['rev-parse', 'HEAD']);
  expect((await execute('collect', board, ['one', '--committed'])).error).toContain('verification'); expect(record().state).toBe('specced'); expect(git(code, ['rev-parse', 'HEAD'])).toBe(before); expect(fs.readFileSync(path.join(code, 'seed.txt'), 'utf8')).toBe('good\n'); expect(fs.existsSync(receipt())).toBe(false);
});
