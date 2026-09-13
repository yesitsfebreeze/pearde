import path from 'node:path';
import { codeRepo, document, hash, list, openBoxes, real, resolve, scan, snapshot, specs, type Prd } from './records';

export const liveStates = new Set(['open', 'analyzing', 'refine', 'question', 'specced', 'claimed', 'blocked', 'failed']);
export function feet(prd: Prd): string[] {
  const root = codeRepo(prd);
  const paths = [...list(prd.fm.footprint), ...specs(prd).flatMap(s => list(s.fm.footprint))];
  return [...new Set(paths.map(p => real(path.resolve(root, p.replace(/^@[^/]+\//, '')))))];
}
export function clash(a: string[], b: string[]) {
  // An unspecified footprint reserves the repository, supplied by the caller.
  return a.some(x => b.some(y => x === y || x.startsWith(y + '/') || y.startsWith(x + '/')));
}
export function dependencies(prd: Prd, prds: Map<string, Prd>) {
  const refs = new Set(prd.children), problems: string[] = [];
  for (const need of list(prd.fm.needs)) {
    try { refs.add(resolve(prds, need, prd).ref); }
    catch (error) { problems.push(String(error)); }
  }
  return { refs: [...refs], problems };
}
export function refusal(prd: Prd, prds: Map<string, Prd>): string | null {
  if (prd.fm.claim) return 'unclaimed: held by ' + prd.fm.claim;
  if (!['open', 'specced'].includes(prd.state)) return 'state: ' + prd.state;
  try { codeRepo(prd); } catch (error) { return String(error); }
  const deps = dependencies(prd, prds);
  if (deps.problems.length) return deps.problems.join('; ');
  const undone = deps.refs.filter(ref => prds.get(ref)?.state !== 'done');
  if (undone.length) return 'needs: not done — ' + undone.join(', ');
  if (prd.state === 'specced' && !prd.children.length && !specs(prd).length) return 'leaf: no published specs';
  const ownFeet = feet(prd);
  for (const other of prds.values()) {
    if (other.ref === prd.ref || !other.fm.claim) continue;
    if (clash(ownFeet.length ? ownFeet : [codeRepo(prd)], feet(other).length ? feet(other) : [codeRepo(other)])) return 'footprint: overlaps held ' + other.ref;
  }
  return null;
}
export function weight(prd: Prd) {
  const values = specs(prd).map(s => Number(s.fm.complexity)).filter(n => Number.isFinite(n) && n > 0);
  const own = Number(prd.fm.complexity);
  return values.length ? values.reduce((a, b) => a + b, 0) : Number.isFinite(own) && own > 0 ? own : 1;
}
export function plan(board: string, workers = 0, scope?: string) {
  const prds = scan(board), settings = document(path.join(board, 'settings.md')).fm;
  const slots = workers || Number(settings.workers) || 3;
  if (!Number.isInteger(slots) || slots < 1 || slots > 32) throw Error('workers must be between 1 and 32');
  const selection = scope ? resolve(prds, scope).ref : null;
  const active = [...prds.values()].filter(p => liveStates.has(p.state) && (!selection || p.ref === selection || p.ref.startsWith(selection + '/')));
  const timing = new Map<string, { start: number; end: number }>(), visiting = new Set<string>(), cycles = new Set<string>();
  function time(prd: Prd): { start: number; end: number } {
    if (timing.has(prd.ref)) return timing.get(prd.ref)!;
    if (visiting.has(prd.ref)) { for (const ref of visiting) cycles.add(ref); return { start: 0, end: 0 }; }
    visiting.add(prd.ref);
    const start = Math.max(0, ...dependencies(prd, prds).refs.filter(r => prds.get(r)?.state !== 'done').map(r => time(prds.get(r)!).end));
    visiting.delete(prd.ref);
    const value = { start, end: start + weight(prd) }; timing.set(prd.ref, value); return value;
  }
  active.forEach(time);
  const notes: string[] = [];
  const rows = active.map(prd => {
    let paths: string[] = [], reason = cycles.has(prd.ref) ? 'dependency cycle' : refusal(prd, prds);
    try { paths = feet(prd); if (!paths.length) paths = [codeRepo(prd)]; } catch (error) { reason = String(error); }
    const published = specs(prd);
    const ownerSlots = Number(document(path.join(prd.board, 'settings.md')).fm.workers ?? slots);
    if (!Number.isInteger(ownerSlots) || ownerSlots < 1 || ownerSlots > 32) throw Error('invalid member worker limit');
    const collect = prd.children.length > 0 && !dependencies(prd, prds).refs.some(r => prds.get(r)?.state !== 'done') || published.length > 0 && !openBoxes(prd.text) && published.every(s => !openBoxes(s.text));
    return {
      board: path.basename(board), path: board, rel: prd.ref, owner_path: prd.board, identity: prd.dir,
      addr: prd.ref.startsWith('@') ? prd.ref : '@' + path.basename(board) + '/' + prd.ref,
      state: prd.state, title: prd.title, start: timing.get(prd.ref)!.start, end: timing.get(prd.ref)!.end,
      prio: Number(prd.fm.priority) || 0, est: weight(prd), held: reason,
      collect,
      feet: paths, dispatchable: !reason, revision: prd.revision, owner_slots: Math.min(slots, ownerSlots),
      role: collect ? 'collector' : prd.state === 'open' ? 'analyst' : 'implementer',
    };
  }).sort((a, b) => a.start - b.start || b.prio - a.prio || a.rel.localeCompare(b.rel));
  const waves: string[][] = [], waveFeet: string[][] = [], waveOwners: Record<string, number>[] = [];
  for (const row of rows.filter(r => r.dispatchable)) {
    let index = waves.findIndex((wave, i) => wave.length < slots && (waveOwners[i][row.owner_path] ?? 0) < row.owner_slots && !clash(waveFeet[i], row.feet));
    if (index < 0) { index = waves.length; waves.push([]); waveFeet.push([]); waveOwners.push({}); }
    waves[index].push(row.addr); waveFeet[index].push(...row.feet);
    waveOwners[index][row.owner_path] = (waveOwners[index][row.owner_path] ?? 0) + 1;
  }
  if (cycles.size) notes.push('dependency cycle: ' + [...cycles].sort().join(', '));
  return { slots, rows, waves, notes, demand: rows.filter(r => r.dispatchable).length, snapshot: hash(JSON.stringify(snapshot(prds))) };
}
export function gantt(board: string) {
  const data = plan(board);
  const lines = ['gantt', '    title PRD dependency plan (relative complexity units)', '    dateFormat X', '    axisFormat %s'];
  for (const [index, row] of data.rows.entries()) lines.push(`    ${row.title.replace(/[\n:;#]/g, ' ')} :${row.held ? 'crit,' : ''}p${index}, ${row.start}, ${Math.max(1, row.est)}s`);
  return '```mermaid\n' + lines.join('\n') + '\n```\n';
}
