import fs from 'node:fs';
import path from 'node:path';
import { hash, inside, parseDocument, readSourceFile, SourceReadError } from './records';

export const SOURCE_RECORDS = 'cartridge-source-records/v1' as const;
type Failure = 'unavailable' | 'changed' | 'malformed' | 'capacity' | 'timeout';
export const sourceRecordFailure = (status: Failure) => ({ schema: SOURCE_RECORDS, status });
class ReadFailure extends Error { constructor(public status: Failure) { super(status); } }
export type RecordRequest = { action: 'index'; expected_source_revision: string } | {
  action: 'read'; expected_source_revision: string; path: string; expected_revision: string;
};
type Item = { path: string; title: string; bytes: number; revision: string; visibility: 'public' };
const MAX_FILE = 1048576, MAX_BYTES = 8 * MAX_FILE, MAX_ENTRIES = 4096, MAX_ITEMS = 128;
const hex = (value: unknown): value is string => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
const normal = (value: unknown, cap: number, depth: number): value is string => typeof value === 'string' && !!value && Buffer.byteLength(value) <= cap &&
  !path.isAbsolute(value) && !/[\\\x00-\x1f\x7f]/.test(value) && value.split('/').length <= depth &&
  value.split('/').every(p => !!p && !p.startsWith('.'));
const boardSelector = (value: unknown): value is string => typeof value === 'string' && !!value && Buffer.byteLength(value) <= 512 && !path.isAbsolute(value) && !value.includes('\\') && !value.includes('\0') && value.split('/').length <= 32 && value.split('/').every(p => !!p && p !== '.' && p !== '..');
const identity = (s: fs.Stats) => `${s.dev}:${s.ino}:${s.mtimeMs}:${s.ctimeMs}`;

/** Public local records only. The tracker owns actual I/O lifetime beyond response timeout. */
export async function sourceRecords(boardsRoot: string, board: string, request: RecordRequest, deadlineMs = 500,
  track?: (work: Promise<any>) => void): Promise<any> {
  if (!boardSelector(board) || !Number.isInteger(deadlineMs) || deadlineMs < 1 || deadlineMs > 2000 ||
      !request || typeof request !== 'object' || Array.isArray(request) || !hex(request.expected_source_revision) ||
      !['index', 'read'].includes(request.action) || Object.keys(request).some(k => !['action', 'expected_source_revision', ...(request.action === 'read' ? ['path', 'expected_revision'] : [])].includes(k)) ||
      request.action === 'read' && (!normal(request.path, 4096, 32) || !request.path.startsWith('prds/') || !request.path.endsWith('/prd.md') || !hex(request.expected_revision))) return sourceRecordFailure('malformed');
  const deadline = performance.now() + deadlineMs;
  const check = () => { if (performance.now() >= deadline) throw new ReadFailure('timeout'); };
  const work = (async () => {
    try {
      const scope = await fs.promises.realpath(boardsRoot); check();
      const root = await fs.promises.realpath(path.resolve(scope, board)); check();
      if (!inside(scope, root) || Buffer.byteLength(root) > 4096) throw new ReadFailure('malformed');
      const directories = new Map<string, string>();
      async function directory(file: string) {
        check(); const stat = await fs.promises.lstat(file); check();
        if (!stat.isDirectory() || stat.isSymbolicLink()) throw new ReadFailure('unavailable');
        if (await fs.promises.realpath(file) !== file) throw new ReadFailure('changed'); check();
        const prior = directories.get(file), current = identity(stat);
        if (prior !== undefined && prior !== current) throw new ReadFailure('changed');
        directories.set(file, current);
      }
      await directory(root);
      const settings = path.join(root, 'settings.md');
      let used = 0;
      const recordBudget = MAX_BYTES - 65536; // Reserve the final authority read.
      const consume = (count: number) => { used += count; if (used > MAX_BYTES) throw new ReadFailure('capacity'); };
      const source = await readSourceFile(settings, 65536, check, consume);
      if (hash(source) !== request.expected_source_revision) throw new ReadFailure('changed');
      const prds = path.join(root, 'prds');
      let missingTree = false;
      try { await directory(prds); } catch (error: any) { if (error.code === 'ENOENT') missingTree = true; else throw error; }
      async function readRecord(relative: string): Promise<{ item: Item; text: string } | null> {
        const file = path.join(root, relative);
        const segments = relative.split('/').slice(0, -1); let parent = root;
        for (const segment of segments) { parent = path.join(parent, segment); await directory(parent); }
        if (used >= recordBudget) throw new ReadFailure('capacity');
        const bytes = await readSourceFile(file, Math.min(MAX_FILE, recordBudget - used), check, consume, recordBudget - used);
        if (used > MAX_BYTES) throw new ReadFailure('capacity');
        let text: string; try { text = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes); } catch { throw new ReadFailure('malformed'); }
        const header = /^(?:\uFEFF)?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text);
        if (/^(?:\uFEFF)?---(?:\r?\n|$)/.test(text) && !header) throw new ReadFailure('malformed');
        if (header && Buffer.byteLength(header[1]) > 16384) throw new ReadFailure('capacity');
        let doc: ReturnType<typeof parseDocument>; try { doc = parseDocument(text, file, true); } catch { throw new ReadFailure('malformed'); }
        const fm = doc.fm;
        if (Object.hasOwn(fm, 'private') && fm.private !== false || Object.hasOwn(fm, 'visibility') && fm.visibility !== 'public') return null;
        if (Buffer.byteLength(doc.title) > 512) throw new ReadFailure('capacity');
        return { item: { path: relative, title: doc.title, bytes: bytes.length, revision: hash(bytes), visibility: 'public' }, text };
      }
      async function stable() {
        check();
        for (const [file, before] of directories) { const stat = await fs.promises.lstat(file); check(); if (identity(stat) !== before || !stat.isDirectory() || stat.isSymbolicLink() || await fs.promises.realpath(file) !== file) throw new ReadFailure('changed'); check(); }
        if (missingTree) { try { await fs.promises.lstat(prds); throw new ReadFailure('changed'); } catch (error: any) { if (error.code !== 'ENOENT') throw error; } }
        const after = await readSourceFile(settings, 65536, check, consume, MAX_BYTES - used);
        if (hash(after) !== request.expected_source_revision) throw new ReadFailure('changed');
        check();
      }
      const base = { schema: SOURCE_RECORDS, root, source_revision: request.expected_source_revision };
      if (request.action === 'read') {
        if (missingTree) throw new ReadFailure('unavailable');
        const record = await readRecord(request.path);
        if (!record) throw new ReadFailure('unavailable');
        if (record.item.revision !== request.expected_revision) throw new ReadFailure('changed');
        await stable();
        const result = { ...base, status: 'available', action: 'read', ...record.item, text: record.text, complete: true };
        if (Buffer.byteLength(JSON.stringify(result)) > MAX_BYTES) throw new ReadFailure('capacity');
        check(); return result;
      }
      const items: Item[] = []; let entries = 0, partial = false, truncated = false;
      const pending = missingTree ? [] : [{ directory: prds, depth: 1 }];
      while (pending.length) {
        check(); const next = pending.pop()!; await directory(next.directory);
        const handle = await fs.promises.opendir(next.directory);
        try {
          check();
          for (;;) {
            check(); const entry = await handle.read(); check(); if (!entry) break;
            if (++entries > MAX_ENTRIES) { partial = truncated = true; pending.length = 0; break; }
            if (entry.name.startsWith('.')) continue;
            const file = path.join(next.directory, entry.name), relative = path.relative(root, file);
            if (!normal(relative, 4096, 32)) { partial = truncated = true; continue; }
            if (entry.isSymbolicLink()) { partial = true; continue; }
            if (entry.isDirectory()) {
              if (next.depth >= 31) { partial = truncated = true; continue; }
              pending.push({ directory: file, depth: next.depth + 1 });
            } else if (entry.name === 'prd.md') {
              try {
                const record = await readRecord(relative);
                if (record) {
                  if (items.length >= MAX_ITEMS) { partial = truncated = true; pending.length = 0; break; }
                  items.push(record.item);
                }
              } catch (error) {
                const status = error instanceof ReadFailure || error instanceof SourceReadError ? error.status : 'unavailable';
                if (status === 'timeout' || status === 'changed') throw error;
                partial = true;
                if (status === 'capacity') { truncated = true; if (used >= recordBudget) { pending.length = 0; break; } }
              }
            }
          }
        } finally { await handle.close(); }
      }
      await stable();
      items.sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
      const result = { ...base, status: partial ? 'partial' : 'available', action: 'index',
        index_revision: hash(JSON.stringify({ root, source_revision: request.expected_source_revision, items })), items,
        complete: !partial, truncated, ...(partial ? { reason: 'source index incomplete' } : {}) };
      if (Buffer.byteLength(JSON.stringify(result)) > MAX_FILE) throw new ReadFailure('capacity');
      check(); return result;
    } catch (error) { return sourceRecordFailure(error instanceof ReadFailure || error instanceof SourceReadError ? error.status : 'unavailable'); }
  })();
  track?.(work); let timer: ReturnType<typeof setTimeout> | undefined;
  try { return await Promise.race([work, new Promise(resolve => { timer = setTimeout(() => resolve(sourceRecordFailure('timeout')), deadlineMs); })]); }
  finally { clearTimeout(timer); }
}
