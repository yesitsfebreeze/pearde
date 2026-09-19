import { afterEach, beforeEach, expect, test, spyOn } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { asp } from '../../src/asp';
import { atomic } from '../../src/records';
import { program } from './fixtures/host';
let root: string, boards: string;
const record = (name: string, text: string, board = 'root') => atomic(path.join(boards, board, 'prds', name, 'prd.md'), text);
beforeEach(() => {
  root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-asp-'));
  boards = path.join(root, '.cartridge/boards');
  atomic(path.join(boards, 'root/settings.md'), '---\nmembers:\n  child: ../child\n---\n');
  atomic(path.join(boards, 'child/settings.md'), '---\nname: child\n---\n');
  record('one', '---\nstate: claimed\nclaim: worker-one\ncomplexity: 3\nneeds: [two, secret]\n---\n# One\n- [x] Read record\n- [ ] Complete work\n');
  record('two', '---\nstate: done\n---\n# Two\n');
  record('secret', '---\nprivate: true\n---\n# SECRET\n');
  record('child-task', '# Child task\n', 'child');
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));
test('plan root contains public tasks and actually declared child boards', async () => {
  const result = await asp(boards, root, 'root', { op: 'expand', entity: 'plan:root' });
  expect(result.nodes.map(n => n.id)).toContain('plan:child');
  const one = result.nodes.find(n => n.id === 'task:root/one');
  expect(one.attributes).toMatchObject({ 'prd.state': 'claimed', 'prd.claim': 'worker-one', 'prd.complexity': 3, 'prd.checks_done': 1, 'prd.checks_total': 2 });
  expect(JSON.stringify(result)).not.toContain('secret');
  expect(result.edges).toContainEqual({ from: one.id, to: 'file:.cartridge/boards/root/prds/one/prd.md', kind: 'recorded-in', revision: one.revision });
});
test('task details link only public observed prerequisites and retain exact checked steps', async () => {
  const result = await asp(boards, root, 'root', { op: 'expand', entity: 'task:root/one' });
  const one = result.nodes.find(n => n.id === 'task:root/one');
  expect(one.attributes['prd.checks']).toEqual([{ done: true, text: 'Read record' }, { done: false, text: 'Complete work' }]);
  expect(one.attributes['prd.unresolved_dependencies']).toBe(1);
  expect(result.edges.find(e => e.kind === 'depends-on')?.to).toBe('task:root/two');
  expect(JSON.stringify(result)).not.toContain('secret');
  expect((await asp(boards, root, 'root', { op: 'expand', entity: 'task:root/secret' })).nodes).toEqual([]);
});
test('search is public only and a disconnected board is never exposed', async () => {
  atomic(path.join(boards, 'unrelated/settings.md'), '---\nname: unrelated\n---\n');
  record('foreign', '# Foreign task', 'unrelated');
  const result = await asp(boards, root, 'root', { op: 'search', query: 'task' });
  expect(result.nodes.map(n => n.id)).toContain('task:child/child-task');
  expect(JSON.stringify(result)).not.toContain('foreign');
  expect((await asp(boards, root, 'root', { op: 'search', query: 'SECRET' })).nodes).toEqual([]);
  await expect(asp(boards, root, 'root', { op: 'expand', entity: 'plan:unrelated' })).rejects.toThrow('outside');
});
test('collection pages expose every public record beyond the first fifty', async () => {
  for (let index = 0; index < 55; index++) record('task' + String(index).padStart(3, '0'), '# Task ' + index);
  const first = await asp(boards, root, 'root', { op: 'expand', entity: 'plan:root', limit: 256 });
  expect(first.nodes.some(n => n.id === 'plan:root#page=1')).toBe(true);
  expect(first.nodes.filter(n => n.id.startsWith('task:'))).toHaveLength(50);
  const second = await asp(boards, root, 'root', { op: 'expand', entity: 'plan:root#page=1', limit: 256 });
  expect(second.nodes.filter(n => n.id.startsWith('task:'))).toHaveLength(7);
});
test('native wire exposes ASP without a planning invocation or memory call', async () => {
  const wire = await program([process.execPath, path.resolve(import.meta.dir, '../../src/service.ts')], () => { throw Error('ASP must not ask other services'); });
  try {
    await wire.call('apply', { root });
    const answer = await wire.call('asp.prd', { op: 'expand', entity: 'task:root/one' });
    expect(answer.nodes.find((n: any) => n.id === 'task:root/one').attributes['prd.state']).toBe('claimed');
  } finally { await wire.close(); }
});

test('search overlaps independent board reads and preserves public results', async () => {
 const original=fs.promises.opendir;let active=0,peak=0;
 const spy=spyOn(fs.promises,'opendir').mockImplementation(async(...args:any[])=>{
  active++;peak=Math.max(peak,active);
  try {await Bun.sleep(10);return await (original as any)(...args);} finally {active--;}
 });
 try {
  const result=await asp(boards,root,'root',{op:'search',query:'task',limit:32});
  expect(peak).toBeGreaterThan(1);expect(peak).toBeLessThanOrEqual(4);
  expect(result.nodes.map(n=>n.id)).toContain('task:child/child-task');
  expect(JSON.stringify(result)).not.toContain('SECRET');
 } finally {spy.mockRestore();}
});
