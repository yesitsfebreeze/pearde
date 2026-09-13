import { expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { atomic, git } from '../../src/records';

const owner = path.resolve(import.meta.dir, '../..');
const runner = path.resolve(owner, '../cartridge.ctg/.cartridge/tools/memo-run');
const memo = '.cartridge/memos/routine/planner-statusline.md';
function fixture() {
  const root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-statusline-'));
  const planner = path.join(root, 'planner'), code = path.join(root, 'code'), ui = path.join(code, 'ui');
  fs.mkdirSync(ui, { recursive: true }); git(code, ['init', '-q']);
  atomic(path.join(code, 'untracked.txt'), 'fixture\n');
  atomic(path.join(planner, memo), fs.readFileSync(path.join(owner, memo), 'utf8'));
  fs.symlinkSync(path.join(owner, 'src'), path.join(planner, 'src'));
  const boards = path.join(planner, '.cartridge/boards');
  atomic(path.join(boards, 'root/settings.md'), `---\nrepo: ${JSON.stringify(code)}\nmembers:\n- ui: ../ui\n---\n`);
  atomic(path.join(boards, 'ui/settings.md'), `---\nrepo: ${JSON.stringify(ui)}\n---\n`);
  for (const [name, state, complexity, origin] of [['one', 'done', 3, 'requested'], ['two', 'open', 1, 'derived']])
    atomic(path.join(boards, 'ui/prds', String(name), 'prd.md'), `---\nstate: ${state}\ncomplexity: ${complexity}\norigin: ${origin}\n---\n\n# ${name}\n`);
  atomic(path.join(boards, 'root/prds/three/prd.md'), '---\nstate: open\ncomplexity: 2\n---\n\n# Three\n');
  return { root, planner, code, ui, dispose() { fs.rmSync(root, { recursive: true, force: true }); } };
}
async function render(f: ReturnType<typeof fixture>, input: string, environment = false) {
  const child = Bun.spawn([runner, path.join(f.planner, memo)], {
    cwd: f.root, env: { ...process.env, PRD_STATUS_JSON: environment ? input : '', PRD_STATUS_LINK: 'off' },
    stdin: new Blob([environment ? '' : input]), stdout: 'pipe', stderr: 'pipe', timeout: 10000,
  });
  const [output, error, code] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited]);
  expect(code, error).toBe(0); expect(error).toBe(''); return output.trimEnd().split('\n');
}
test('statusline selects mapped code owner and labels recorded weighted progress', async () => {
  const f = fixture();
  try {
    const before = git(f.code, ['status', '--porcelain']);
    const lines = await render(f, JSON.stringify({ workspace: { current_dir: f.ui }, model: { display_name: 'Fixture model' } }));
    expect(lines).toHaveLength(2); expect(lines[0]).toContain('Fixture model'); expect(lines[0]).toContain('no-upstream'); expect(lines[0]).toContain('*1');
    expect(lines[1]).toContain('prd ui · recorded 1/2 done · weighted 75% · open 1 · derived open 1');
    expect(lines[1]).not.toContain('verified'); expect(git(f.code, ['status', '--porcelain'])).toBe(before);
    expect((await render(f, JSON.stringify({ cwd: f.code }), true))[1]).toContain('prd root · recorded 1/3 done · weighted 50%');
    expect((await render(f, JSON.stringify({ cwd: f.planner }), true))[1]).toContain('prd root');
  } finally { f.dispose(); }
});
test('statusline renders safe first line without a board and tolerates malformed input', async () => {
  const f = fixture();
  try {
    const lines = await render(f, JSON.stringify({ current_dir: f.root, display_name: '\u001b[31mModel\n\u0007safe\u001b]0;evil\u0007' }), true);
    expect(lines).toHaveLength(1); expect(lines[0]).toContain('Model'); expect(lines[0]).not.toMatch(/[\u0000-\u001f\u007f]/); expect(lines[0]).not.toContain('evil');
    expect((await render(f, '{invalid'))[0]).toContain(f.planner);
    expect((await render(f, JSON.stringify({ cwd: f.root }) + 'x'.repeat(65536)))[0]).toContain(f.planner);
  } finally { f.dispose(); }
});
test('statusline bounds transcript reading and uses latest assistant model and persona', async () => {
  const f = fixture();
  try {
    const transcript = path.join(f.root, 'transcript.jsonl');
    atomic(transcript, JSON.stringify({ type: 'assistant', message: { model: 'old-model', content: 'x'.repeat(1100000) } }) + '\n' +
      JSON.stringify({ type: 'assistant', message: { model: 'live-model\u001b[0m', content: [{ type: 'text', text: '▸prd · as reviewer' }] } }) + '\n');
    fs.mkdirSync(path.join(f.ui, '.obsidian'));
    const lines = await render(f, JSON.stringify({ cwd: f.ui, display_name: 'fallback', transcript_path: transcript }));
    expect(lines[0]).toContain('live-model'); expect(lines[0]).not.toContain('old-model'); expect(lines[0]).not.toContain('fallback');
    expect(lines[1]).toContain('reviewer'); expect(lines[1]).toContain('▸vault'); expect(lines.join('')).not.toContain('\u001b');
  } finally { f.dispose(); }
});
test('statusline shows local ahead and behind counts without contacting an upstream', async () => {
  const f = fixture();
  try {
    git(f.code, ['config', 'user.email', 'fixture@example.invalid']); git(f.code, ['config', 'user.name', 'Fixture']);
    git(f.code, ['add', '.']); git(f.code, ['commit', '-qm', 'baseline']);
    const branch = git(f.code, ['branch', '--show-current']);
    git(f.code, ['checkout', '-qb', 'fixture-upstream']);
    atomic(path.join(f.code, 'upstream.txt'), 'upstream\n'); git(f.code, ['add', '.']); git(f.code, ['commit', '-qm', 'upstream change']);
    git(f.code, ['checkout', '-q', branch]);
    atomic(path.join(f.code, 'local.txt'), 'local\n'); git(f.code, ['add', '.']); git(f.code, ['commit', '-qm', 'local change']);
    git(f.code, ['branch', '--set-upstream-to=fixture-upstream']);
    const lines = await render(f, JSON.stringify({ cwd: f.code }));
    expect(lines[0]).toContain('↑1 ↓1'); expect(lines[0]).not.toContain('no-upstream'); expect(lines[0]).not.toContain('*');
  } finally { f.dispose(); }
});
