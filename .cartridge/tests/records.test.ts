import { expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { document, hash, members, scan } from '../../src/records';
import { plan } from '../../src/planner';
const record = path.resolve(import.meta.dir, '..');
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
  // Lifecycle fields on the live board legitimately change after migration.
  // Verify migration fidelity against its immutable committed snapshot, while
  // still requiring every original canonical identity on today's board.
  const migration = '3d1848d79e6bc5fc2f59906baee013f1ca698bd1';
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'prd-migration-proof-'));
  try {
    const archive = Bun.spawnSync(['git', 'archive', migration, '.cartridge'], { cwd: path.dirname(record), stdout: 'pipe', stderr: 'pipe' });
    expect(archive.exitCode, archive.stderr.toString()).toBe(0);
    const unpack = Bun.spawnSync(['tar', '-xf', '-', '-C', temporary], { stdin: archive.stdout, stdout: 'pipe', stderr: 'pipe' });
    expect(unpack.exitCode, unpack.stderr.toString()).toBe(0);
    const historicalRecord = path.join(temporary, '.cartridge');
    const manifest = JSON.parse(fs.readFileSync(path.join(record, 'reports/record-migration/manifest.json'), 'utf8'));
    expect(hash(fs.readFileSync(path.join(record, 'reports/record-migration/manifest.json')))).toBe(hash(fs.readFileSync(path.join(historicalRecord, 'reports/record-migration/manifest.json'))));
    const current = scan(path.join(record, 'boards/root'));
    const migrated = scan(path.join(historicalRecord, 'boards/root'));
    expect(manifest.prds.length).toBe(182);
    for (const original of manifest.prds) {
      const id = original.id.replace(/^@root\//, ''); expect(current.has(id)).toBe(true);
      const prd = migrated.get(id); expect(prd).toBeDefined();
      for (const [key, value] of Object.entries(original.frontmatter)) if (!['repo', 'review-status'].includes(key)) expect(prd!.fm[key] ?? null).toEqual(value ?? null);
    }
    for (const item of manifest.native_records) {
      const moved = manifest.moves.find((row: any) => row.source === item.source), data = document(path.join(temporary, moved.destination.replace(/^prd\.ctg\//, ''))).fm;
      for (const key of ['kind', 'status', 'state', 'owner', 'claim']) expect(data[key] ?? null).toEqual(item.frontmatter[key] ?? null);
    }
    for (const row of manifest.moves) if (row.source.endsWith('review-inputs.json')) expect(hash(fs.readFileSync(path.join(temporary, row.destination.replace(/^prd\.ctg\//, ''))))).toBe(row.before_sha256);
  } finally { fs.rmSync(temporary, { recursive: true, force: true }); }
});
