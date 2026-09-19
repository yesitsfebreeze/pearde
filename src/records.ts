import fs from 'node:fs';
import path from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { Database } from 'bun:sqlite';
import { parseDocument as parseYamlDocument, visit as visitYaml, isScalar } from 'yaml';

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
export function gitProbeError(root: string, args: string[]): string {
  const result = Bun.spawnSync(['git', '-C', root, ...args], { stdout: 'pipe', stderr: 'pipe', timeout: 60_000 });
  return result.exitCode ? result.stderr.toString().trim() : '';
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
  return parseDocument(text, file);
}
export function parseDocument(text: string, file: string, strictPublic = false) {
  const match = /^(?:\uFEFF)?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text);
  let fm: any = {};
  if (match && strictPublic) {
    if (Buffer.byteLength(match[1]) > 16384) throw Error('public frontmatter exceeds limit');
    const parsed = parseYamlDocument(match[1], { strict: true, uniqueKeys: true, stringKeys: true, logLevel: 'silent' });
    if (parsed.errors.length || parsed.warnings.length) throw Error('ambiguous public frontmatter');
    visitYaml(parsed, {
      Alias() { throw Error('public frontmatter aliases are unsupported'); },
      Pair(_key, pair) { if (isScalar(pair.key) && pair.key.value === '<<') throw Error('public frontmatter merges are unsupported'); },
    });
    fm = parsed.toJS({ maxAliasCount: 0 }) ?? {};
  } else if (match) fm = Bun.YAML.parse(match[1]) ?? {};
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
  if (Object.keys(changes).some(key => CONTROLLED.includes(key))) recordFields(file);
}
// state, claim and commit change only through engine ops. The engine records the values it wrote in one
// file per PRD under the owner board's gitignored .state/fields/, written by a single temp-file rename.
// A record without one (fresh clone) is trusted once. A crash between the record and value renames, or a
// git checkout of a record, reads as an outside change: restore the recorded values or adopt with a reason.
const CONTROLLED = ['state', 'claim', 'commit'];
const controlled = (file: string) => { const fm = document(file).fm; return Object.fromEntries(CONTROLLED.map(key => [key, fm[key] ?? null])); };
function ownerBoard(file: string) {
  let board = path.dirname(path.dirname(file));
  while (!fs.existsSync(path.join(board, 'settings.md'))) { if (path.dirname(board) === board) throw Error('PRD outside a board: ' + file); board = path.dirname(board); }
  return board;
}
const fieldsRoot = (board: string) => path.join(board, '.state/fields');
const fieldsFile = (file: string, board = ownerBoard(file)) => path.join(fieldsRoot(board), path.relative(path.join(board, 'prds'), path.dirname(file)) + '.json');
export function recordFields(file: string) { atomic(fieldsFile(file), JSON.stringify(controlled(file))); }
export function fieldsProblem(file: string, retried = false): string | null {
  const store = fieldsFile(file), current = controlled(file);
  if (!fs.existsSync(store)) {
    // Link, not rename: a bootstrap never overwrites values an engine op wrote meanwhile.
    const temporary = store + '.' + randomUUID() + '.tmp';
    fs.mkdirSync(path.dirname(store), { recursive: true }); fs.writeFileSync(temporary, JSON.stringify(current));
    try { fs.linkSync(temporary, store); } catch (error: any) { if (error.code !== 'EEXIST') throw error; } finally { fs.unlinkSync(temporary); }
  }
  const recorded = JSON.parse(fs.readFileSync(store, 'utf8'));
  const changed = CONTROLLED.filter(key => JSON.stringify(recorded[key] ?? null) !== JSON.stringify(current[key]));
  if (!changed.length) return null;
  // An engine write renames the record then the values; re-read once past that window.
  if (!retried) { Bun.sleepSync(50); return fieldsProblem(file, true); }
  return changed.map(key => key + ' changed outside the engine (recorded ' + JSON.stringify(recorded[key] ?? null) + ', found ' + JSON.stringify(current[key]) + ')').join('; ');
}
export const fieldsRefusal = (prd: Prd, problem: string) => prd.ref + ': ' + problem + '; restore the recorded values or run `prd adopt ' + prd.ref + ' --by <id> --reason "<text>" --board ' + prd.board + '` (the adoption is recorded in ' + adoptionLog(prd.board) + ')';
export const adoptionLog = (board: string) => path.join(fieldsRoot(board), 'adopted.log');
// Accept the current values of a changed record; every adoption appends one audit line.
export function adoptFields(prd: Prd, by: string, reason: string) {
  const store = fieldsFile(prd.file, prd.board), current = controlled(prd.file);
  const recorded = fs.existsSync(store) ? JSON.parse(fs.readFileSync(store, 'utf8')) : null;
  fs.mkdirSync(fieldsRoot(prd.board), { recursive: true });
  fs.appendFileSync(adoptionLog(prd.board), JSON.stringify({ at: new Date().toISOString(), ref: prd.ref, local: prd.local, old: recorded, new: current, by, reason }) + '\n');
  atomic(store, JSON.stringify(current));
  return { old: recorded, new: current };
}
// Drop values whose PRD is gone, so a later record at the same path never inherits them. The store is
// keyed by path, so a rehome (`mv prds/one prds/two`) is a drop plus a record the engine has never seen
// and trusts once. Dropping a non-idle record silently would destroy the last evidence of that claim, so
// log the values and warn: the drop is the only moment the engine can still see what it is losing.
export function dropOrphanFields(board: string) {
  const root = fieldsRoot(board), warnings: string[] = [];
  const walk = (dir: string): void => { if (fs.existsSync(dir)) for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) { walk(file); continue; }
    if (!entry.name.endsWith('.json')) continue;
    const local = path.relative(root, file).slice(0, -5);
    if (fs.existsSync(path.join(board, 'prds', local, 'prd.md'))) continue;
    const dropped = JSON.parse(fs.readFileSync(file, 'utf8'));
    const idle = (dropped.state ?? 'open') === 'open' && dropped.claim == null && dropped.commit == null;
    // Log before unlinking: a crash in between may repeat a line on the retry, which is harmless, where
    // the other order loses the only remaining copy of the values, which is the loss this exists to stop.
    if (!idle) fs.appendFileSync(adoptionLog(board), JSON.stringify({ at: new Date().toISOString(), local, dropped }) + '\n');
    fs.rmSync(file, { force: true });
    if (idle) continue;
    warnings.push(local + ': prds/' + local + '/prd.md is gone; recorded ' + JSON.stringify(dropped) + ' dropped and logged in ' + adoptionLog(board) + '. If the record was rehomed, its new path is trusted on first observation — compare it, and restore or `prd adopt` it if these values did not survive the move.');
  } };
  walk(root);
  return warnings;
}
const holder = (claim: unknown) => claim == null ? null : String(claim).split(/\s/)[0];
// Warn while an adopted claim that changed hands is still the live claim.
export function adoptionWarnings(board: string, prds: Map<string, Prd>) {
  const log = adoptionLog(board);
  if (!fs.existsSync(log)) return [];
  return fs.readFileSync(log, 'utf8').split('\n').filter(Boolean).flatMap(line => {
    const entry = JSON.parse(line), prd = [...prds.values()].find(p => p.board === board && p.local === entry.local);
    if (!prd || holder(entry.new?.claim) === null || holder(entry.old?.claim) === holder(entry.new?.claim) || JSON.stringify(prd.fm.claim ?? null) !== JSON.stringify(entry.new?.claim ?? null)) return [];
    return [prd.ref + ': claim changed hands by adoption (' + JSON.stringify(entry.old?.claim ?? null) + ' -> ' + JSON.stringify(entry.new?.claim ?? null) + ') by ' + entry.by + ' at ' + entry.at + ': ' + entry.reason];
  });
}
export function canonicalBoard(board: string) {
  const result = real(path.resolve(board));
  if (!fs.existsSync(path.join(result, 'settings.md'))) throw Error('no planning board at ' + result);
  return result;
}
function memberLocations(raw: any, limit = Infinity): [string, string][] {
  function* entries(): Generator<[string, unknown]> {
    for (const item of Array.isArray(raw) ? raw : [raw]) {
      if (Array.isArray(raw) && (typeof item !== 'object' || !item)) continue;
      for (const name of Object.keys(item)) yield [name, item[name]];
    }
  }
  const names = new Set();
  const result: [string, string][] = [];
  for (const [name, location] of entries()) {
    if (result.length >= limit) throw new DeclarationError('capacity');
    if (!/^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(name) || names.has(name) || typeof location !== 'string') throw Error('invalid or duplicate member board');
    names.add(name);
    result.push([name, location]);
  }
  return result;
}
export function members(board: string): [string, string][] {
  return memberLocations(document(path.join(board, 'settings.md')).fm.members ?? []).map(([name, location]) => {
    const target = canonicalBoard(path.resolve(board, location));
    if (!inside(path.dirname(board), target)) throw Error('member escapes centralized boards');
    return [name, target];
  });
}
export class SourceReadError extends Error {
  constructor(public status: 'unavailable' | 'malformed' | 'capacity' | 'changed') { super(status); }
}
/** Exact bounded bytes from one regular source file; callers own the shared deadline. */
export async function readSourceFile(file: string, limit: number, check: () => void, consume?: (bytes: number) => void, maxBytes = limit + 1): Promise<Buffer> {
  check(); const before = await fs.promises.lstat(file); check();
  if (!before.isFile() || before.isSymbolicLink()) throw new SourceReadError('malformed');
  if (before.size > limit) throw new SourceReadError('capacity');
  const handle = await fs.promises.open(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK);
  try {
    check(); const opened = await handle.stat(); check();
    if (!opened.isFile() || opened.dev !== before.dev || opened.ino !== before.ino) throw new SourceReadError('changed');
    if (opened.size > limit) throw new SourceReadError('capacity');
    const ceiling = Math.min(limit + 1, maxBytes);
    let buffer = Buffer.alloc(Math.min(opened.size + 1, ceiling)), count = 0;
    while (count < ceiling) {
      if (count === buffer.length) {
        const grown = Buffer.alloc(Math.min(ceiling, Math.max(1, buffer.length * 2)));
        buffer.copy(grown, 0, 0, count); buffer = grown;
      }
      check(); const read = await handle.read(buffer, count, buffer.length - count, null); consume?.(read.bytesRead); check();
      if (!read.bytesRead) break;
      count += read.bytesRead;
    }
    if (count > limit) throw new SourceReadError('capacity');
    const after = await handle.stat(); check(); const current = await fs.promises.lstat(file); check();
    if (count === buffer.length && after.size > count) throw new SourceReadError('capacity');
    if (after.size !== count || after.mtimeMs !== opened.mtimeMs || after.ctimeMs !== opened.ctimeMs ||
        current.dev !== opened.dev || current.ino !== opened.ino || current.size !== after.size ||
        current.mtimeMs !== after.mtimeMs || current.ctimeMs !== after.ctimeMs) throw new SourceReadError('changed');
    return buffer.subarray(0, count);
  } finally { await handle.close(); }
}
const DECLARATIONS = 'cartridge-source-declarations/v1' as const;
type DeclarationStatus = 'unavailable' | 'malformed' | 'capacity' | 'timeout';
export type SourceDeclarations = { schema: typeof DECLARATIONS; status: DeclarationStatus } | {
  schema: typeof DECLARATIONS; status: 'available'; root: string; revision: string;
  children: { name: string; root: string; kind: 'board' }[];
};
export const declarationFailure = (status: DeclarationStatus): SourceDeclarations => ({ schema: DECLARATIONS, status });
class DeclarationError extends Error {
  constructor(public status: DeclarationStatus) { super(status); }
}
/** Read declared edges without scanning descendants, acquiring locks or publishing effects. */
export async function sourceDeclarations(boardsRoot: string, relativeBoard: string, deadlineMs = 500,
  track?: (work: Promise<SourceDeclarations>) => void): Promise<SourceDeclarations> {
  if (typeof relativeBoard !== 'string' || !relativeBoard || Buffer.byteLength(relativeBoard) > 512 ||
      relativeBoard.includes('\\') || relativeBoard.includes('\0') || path.isAbsolute(relativeBoard) ||
      relativeBoard.split('/').length > 32 || relativeBoard.split('/').some(p => !p || p === '.' || p === '..') ||
      !Number.isInteger(deadlineMs) || deadlineMs < 1 || deadlineMs > 2000) return declarationFailure('malformed');
  const deadline = performance.now() + deadlineMs;
  const check = () => { if (performance.now() >= deadline) throw new DeclarationError('timeout'); };
  const cap = (text: string, limit: number) => { if (Buffer.byteLength(text) > limit) throw new DeclarationError('capacity'); };
  // Resolve missing suffixes, but never treat a dangling symlink as a missing ordinary path.
  async function destination(file: string): Promise<string> {
    check();
    try { await fs.promises.lstat(file); }
    catch (error: any) {
      if (error.code !== 'ENOENT') throw error;
      const parent = path.dirname(file);
      if (parent === file) throw error;
      return path.join(await destination(parent), path.basename(file));
    }
    return fs.promises.realpath(file);
  }
  const work = (async (): Promise<SourceDeclarations> => {
    try {
      const scope = await fs.promises.realpath(boardsRoot); check();
      const root = await fs.promises.realpath(path.resolve(scope, relativeBoard)); check(); cap(root, 4096);
      if (!inside(scope, root)) throw new DeclarationError('malformed');
      if (!(await fs.promises.stat(root)).isDirectory()) throw new DeclarationError('unavailable'); check();
      const file = path.join(root, 'settings.md');
      let data: Buffer;
      try { data = await readSourceFile(file, 65536, check); }
      catch (error) { if (error instanceof SourceReadError) throw new DeclarationError(error.status === 'changed' ? 'unavailable' : error.status); throw error; }
      check();
      let locations: [string, string][];
      try { locations = memberLocations(parseDocument(new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(data), file).fm.members ?? [], 64); }
      catch (error) { throw error instanceof DeclarationError ? error : new DeclarationError('malformed'); }
      const children: { name: string; root: string; kind: 'board' }[] = [];
      for (const [name, location] of locations.sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) {
        check(); cap(name, 64); cap(location, 4096);
        if (location.includes('\0')) throw new DeclarationError('malformed');
        const lexical = path.resolve(root, location); cap(lexical, 4096);
        if (!inside(scope, lexical) || !inside(path.dirname(root), lexical)) throw new DeclarationError('malformed');
        const target = await destination(lexical); check(); cap(target, 4096);
        if (!inside(scope, target) || !inside(path.dirname(root), target)) throw new DeclarationError('malformed');
        children.push({ name, root: target, kind: 'board' });
      }
      const answer: SourceDeclarations = { schema: DECLARATIONS, status: 'available', root, revision: hash(data), children };
      cap(JSON.stringify(answer), 262144); check(); return answer;
    } catch (error) { return declarationFailure(error instanceof DeclarationError ? error.status : 'unavailable'); }
  })();
  // A native caller keeps this actual IO lifetime in its capacity accounting,
  // even when the response deadline wins before an already-issued OS call ends.
  track?.(work);
  let timer: ReturnType<typeof setTimeout> | undefined;
  try { return await Promise.race([work, new Promise<SourceDeclarations>(resolve => { timer = setTimeout(() => resolve(declarationFailure('timeout')), deadlineMs); })]); }
  finally { clearTimeout(timer); }
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
  if (name.startsWith('@')) {
    const slash = name.indexOf('/');
    const own = [...prds.values()].filter(p => !p.alias && path.basename(p.board) === name.slice(1, slash) && p.local === name.slice(slash + 1));
    if (own.length === 1) return own[0];
  }
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
  if (!root || !fs.existsSync(root)) throw Error(prd.ref + ': source is not an existing Git repository');
  if (!repoRoot(root)) {
    // Distinguish a real gap (a path that is not a git tree) from git failing
    // from within the sandbox or with no usable environment: the earlier
    // swallow reported every probe failure as a missing repository, which
    // sent debugging to the wrong layer.
    const probe = gitProbeError(root, ['rev-parse', '--show-toplevel']);
    throw Error(prd.ref + ': source is not an existing Git repository' + (probe ? ' — git failed: ' + probe : ''));
  }
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
