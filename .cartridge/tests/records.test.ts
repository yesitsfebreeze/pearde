import { expect, test } from 'bun:test';
import fs from 'node:fs';
import path from 'node:path';
import { document, hash, members, scan } from '../../src/records';
import { plan } from '../../src/planner';
const record = path.resolve(import.meta.dir, '..'), workspace = path.resolve(record, '../..');
test('central records retain explicit owners and a resolvable acyclic dependency graph', () => {
  const root = path.join(record, 'boards/root');
  for (const owner of [root, ...members(root).map(([, b]) => b)]) {
    const config = document(path.join(owner, 'settings.md')).fm;
    expect(config['require-repo']).toBe(true); expect(path.isAbsolute(config.repo)).toBe(true); expect(fs.existsSync(config.repo)).toBe(true);
  }
  for (const p of scan(root).values()) {
    expect(path.isAbsolute(p.fm.repo)).toBe(true); expect(fs.existsSync(p.fm.repo)).toBe(true);
    expect(['open', 'analyzing', 'refine', 'question', 'specced', 'claimed', 'blocked', 'done', 'failed']).toContain(p.state);
  }
  const current = plan(root); expect(current.notes).toEqual([]); expect(current.rows.filter(r => r.held?.includes('outside this graph'))).toEqual([]);
}, 30000);
test('migration preserves original PRD fields, native states and historical review inputs', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(record, 'reports/record-migration/manifest.json'), 'utf8'));
  const current = scan(path.join(record, 'boards/root'));
  expect(manifest.prds.length).toBe(182);
  for (const original of manifest.prds) {
    const prd = current.get(original.id.replace(/^@root\//, '')); expect(prd).toBeDefined();
    for (const [key, value] of Object.entries(original.frontmatter)) if (!['repo', 'review-status'].includes(key)) expect(prd!.fm[key] ?? null).toEqual(value ?? null);
  }
  for (const item of manifest.native_records) {
    const moved = manifest.moves.find((row: any) => row.source === item.source), data = document(path.join(workspace, moved.destination)).fm;
    for (const key of ['kind', 'status', 'state', 'owner', 'claim']) expect(data[key] ?? null).toEqual(item.frontmatter[key] ?? null);
  }
  for (const row of manifest.moves) if (row.source.endsWith('review-inputs.json')) expect(hash(fs.readFileSync(path.join(workspace, row.destination)))).toBe(row.before_sha256);
});
