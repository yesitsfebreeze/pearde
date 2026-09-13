import fs from 'node:fs';
import path from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { Database } from 'bun:sqlite';

export const hash = (value: string | Buffer) => createHash('sha256').update(value).digest('hex');
export const list = (value: unknown): string[] => value == null ? [] : (Array.isArray(value) ? value : [value]).map(String);
export const inside = (root: string, file: string) => file === root || file.startsWith(root + path.sep);
export function real(file: string): string {
  if (fs.existsSync(file)) return fs.realpathSync(file);
  const parent = path.dirname(file);
  return parent === file ? file : path.join(real(parent), path.basename(file));
}
export function contained(root: string, relative: string): string {
  const file = real(path.resolve(root, relative));
  if (!inside(real(root), file)) throw Error('path escapes its board or repository');
  return file;
}
export function relative(value: string): string {
  if (!value || /^[\/~\-]/.test(value) || value.includes('\\') || value.split('/').some(p => !p || p === '.' || p === '..') || !/^[@A-Za-z0-9_. /-]+$/.test(value)) throw Error('expected a board-relative PRD path');
  return value;
}
export function git(root: string, args: string[], check = true): string {
  const result = Bun.spawnSync(['git', '-C', root, ...args], { stdout: 'pipe', stderr: 'pipe', timeout: 60_000 });
  if (check && result.exitCode) throw Error(result.stderr.toString().trim() || 'Git command failed');
  return result.exitCode ? '' : result.stdout.toString().trim();
}
export function repoRoot(root: string): string {
  return git(root, ['rev-parse', '--show-toplevel'], false);
}
export function atomic(file: string, value: string) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = file + '.' + randomUUID() + '.tmp';
  try { fs.writeFileSync(temporary, value, { flag: 'wx' }); fs.renameSync(temporary, file); }
  finally { if (fs.existsSync(temporary)) fs.unlinkSync(temporary); }
}
export function document(file: string) {
  if (fs.statSync(file).size > 1024 * 1024) throw Error('record exceeds the 1 MiB read limit');
  const text = fs.readFileSync(file, 'utf8');
  const match = /^(?:\uFEFF)?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text);
  const fm = match ? Bun.YAML.parse(match[1]) ?? {} : {};
  if (!fm || typeof fm !== 'object' || Array.isArray(fm)) throw Error(file + ': frontmatter must be an object');
  const body = match ? text.slice(match[0].length) : text;
  return { fm: fm as Record<string, any>, text, body, title: /^#\s+(.+)$/m.exec(body)?.[1] ?? path.basename(path.dirname(file)) };
}
// Change only requested keys. Preserve the user's other frontmatter, comments and prose.
export function edit(file: string, changes: Record<string, unknown>, expected?: string) {
  const { text } = document(file);
  if (expected && hash(text) !== expected) throw Error('record changed since it was read; rescan before retrying');
  const match = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text);
  let head = match ? match[1] + '\n' : '';
  for (const [key, value] of Object.entries(changes)) {
    if (!/^[a-z][a-z0-9-]*$/.test(key)) throw Error('invalid frontmatter key');
    const block = new RegExp('^' + key + ':[^\\n]*(?:\\n(?!(?:[A-Za-z][\\w-]*:|#))[^\\n]*)*\\n?', 'm');
    const replacement = value == null ? '' : `${key}: ${JSON.stringify(value)}\n`;
    head = block.test(head) ? head.replace(block, replacement) : head + replacement;
  }
  atomic(file, '---\n' + head.trimEnd() + '\n---\n' + (match ? text.slice(match[0].length) : text));
}
export function canonicalBoard(board: string) {
  const result = real(path.resolve(board));
  if (!fs.existsSync(path.join(result, 'settings.md'))) throw Error('no planning board at ' + result);
  return result;
}
export function members(board: string): [string, string][] {
  const raw = document(path.join(board, 'settings.md')).fm.members ?? [];
  const entries = Array.isArray(raw) ? raw.flatMap(item => typeof item === 'object' && item ? Object.entries(item) : []) : Object.entries(raw);
  const names = new Set();
  return entries.map(([name, location]) => {
    if (!/^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(name) || names.has(name) || typeof location !== 'string') throw Error('invalid or duplicate member board');
    names.add(name);
    const target = canonicalBoard(path.resolve(board, location));
    if (!inside(path.dirname(board), target)) throw Error('member escapes centralized boards');
    return [name, target];
  });
}
export type Prd = ReturnType<typeof document> & { ref: string; local: string; alias: string; board: string; file: string; dir: string; state: string; revision: string; children: string[] };
export function scan(board: string): Map<string, Prd> {
  board = canonicalBoard(board);
  const result = new Map<string, Prd>(), seen = new Set<string>();
  function visit(owner: string, alias = '', chain = new Set<string>()) {
    if (chain.has(owner)) throw Error('member board cycle at ' + owner);
    const next = new Set(chain).add(owner);
    const root = contained(owner, 'prds');
    function walk(dir: string) {
      if (!fs.existsSync(dir)) return;
      for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
        if (entry.name.startsWith('.')) continue;
        const file = contained(owner, path.relative(owner, path.join(dir, entry.name)));
        if (entry.isSymbolicLink()) throw Error('symlink in PRD records: ' + file);
        if (entry.isDirectory()) walk(file);
        else if (entry.name === 'prd.md' && !seen.has(file)) {
          seen.add(file);
          const local = path.relative(root, path.dirname(file));
          const ref = alias ? '@' + alias + '/' + local : local;
          const doc = document(file);
          result.set(ref, { ...doc, ref, local, alias, board: owner, file, dir: path.dirname(file), state: String(doc.fm.state ?? 'open'), revision: hash(doc.text), children: [] });
        }
      }
    }
    walk(root);
    for (const [name, target] of members(owner)) visit(target, alias ? alias + '/' + name : name, next);
  }
  visit(board);
  for (const prd of result.values()) prd.children = [...result.values()].filter(p => p.board === prd.board && path.dirname(p.local) === prd.local).map(p => p.ref);
  return result;
}
export function resolve(prds: Map<string, Prd>, name: string, owner?: Prd): Prd {
  relative(name);
  name = name.replace(/^prds\//, '').replace(/\/prd\.md$/, '');
  const local = owner?.alias && !name.startsWith('@') ? '@' + owner.alias + '/' + name : name;
  if (prds.has(local)) return prds.get(local)!;
  if (prds.has(name)) return prds.get(name)!;
  let matches = [...prds.values()].filter(p => path.basename(p.local) === name && (!owner || p.board === owner.board));
  if (!matches.length && owner) matches = [...prds.values()].filter(p => path.basename(p.local) === name);
  if (matches.length !== 1) throw Error('PRD missing, ambiguous, or outside this graph: ' + name);
  return matches[0];
}
export function codeRepo(prd: Prd): string {
  const settings = document(path.join(prd.board, 'settings.md')).fm;
  const raw = prd.fm.repo ?? settings.repo;
  if (!raw && settings['require-repo']) throw Error(prd.ref + ': must name a source repository');
  const root = real(raw ? path.resolve(prd.board, String(raw)) : repoRoot(prd.board));
  if (!root || !fs.existsSync(root) || !repoRoot(root)) throw Error(prd.ref + ': source is not an existing Git repository');
  return root;
}
export function specs(prd: Prd) {
  const directory = contained(prd.board, path.relative(prd.board, path.join(prd.dir, 'specs')));
  return fs.existsSync(directory) ? fs.readdirSync(directory).filter(p => p.endsWith('.md')).sort().map(p => ({ file: contained(prd.board, path.relative(prd.board, path.join(directory, p))), ...document(path.join(directory, p)) })) : [];
}
export const openBoxes = (text: string) => /^\s*(?:[-*+]|\d{1,9}[.)])\s*\[\s*\]/m.test(text);
export function snapshot(prds: Map<string, Prd>) {
  return Object.fromEntries([...prds].sort(([a], [b]) => a.localeCompare(b)).map(([ref, p]) => [ref, { ref, state: p.state, repo: p.fm.repo ?? null, path: p.file, revision: p.revision, commit: p.fm.commit ?? null, claim: p.fm.claim ?? null }]));
}
// SQLite owns the process lock: crashes release the transaction without PID recovery.
// All board aliases in a record repository resolve to this same canonical lock.
export async function withLocks<T>(keys: string[], work: () => Promise<T>, timeout = 60_000): Promise<T> {
  const locks: Database[] = [];
  try {
    for (const key of [...new Set(keys.map(real))].sort()) {
      fs.mkdirSync(path.dirname(key), { recursive: true });
      const db = new Database(key, { create: true });
      const deadline = Date.now() + timeout;
      for (;;) {
        try { db.exec('BEGIN EXCLUSIVE'); locks.push(db); break; }
        catch (error) {
          if (Date.now() >= deadline || !(error instanceof Error) || !error.message.includes('locked')) { db.close(); throw Error('another run or mutation owns the planning record'); }
          await Bun.sleep(25);
        }
      }
    }
    return await work();
  } finally { for (const db of locks.reverse()) { db.exec('ROLLBACK'); db.close(); } }
}
export function mutationKeys(board: string) {
  const owners = [board, ...[...scan(board).values()].map(p => p.board)];
  return owners.map(owner => path.join(repoRoot(owner) || owner, '.cartridge/.state/prd-mutation.sqlite'));
}
