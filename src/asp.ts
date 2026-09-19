import path from 'node:path';
import { inside, parseDocument, sourceDeclarations } from './records';
import { sourceRecords } from './source-records';

const PAGE = 50;
const checks = (text: string) => [...text.matchAll(/^\s*(?:[-*+]|\d+[.)])\s*\[([ xX])\]\s*(.+)$/gm)]
  .map(match => ({ done: match[1].toLowerCase() === 'x', text: match[2].slice(0, 512) }));
const publicFields = (doc: ReturnType<typeof parseDocument>) => {
  const items = checks(doc.text), number = Number(doc.fm.complexity);
  return { state: typeof doc.fm.state === 'string' ? doc.fm.state.slice(0, 64) : 'open',
    claim: typeof doc.fm.claim === 'string' ? doc.fm.claim.slice(0, 512) : null,
    complexity: Number.isFinite(number) && number > 0 ? number : null,
    checks_done: items.filter(item => item.done).length, checks_total: items.length };
};
const keyOf = (record: any) => record.path.slice('prds/'.length, -'/prd.md'.length);
const valid = (name: string) => /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(name);

/** Public records only, through the same bounded reader as source.board. No Git, writes or memory recall. */
export async function asp(boards: string, project: string, defaultBoard: string, request: any) {
  if (!request || !['expand', 'search'].includes(request.op)) throw Error('ASP supports expand and search');
  const limit = request.limit ?? 50;
  if (!Number.isInteger(limit) || limit < 1 || limit > 256) throw Error('ASP limit must be between 1 and 256');
  const deadline = performance.now() + 1800;
  const remaining = () => Math.max(1, Math.min(1500, Math.floor(deadline - performance.now())));
  const declared = new Map<string, any>();
  async function declaration(board: string): Promise<any> {
    if (declared.has(board)) return declared.get(board);
    if (!valid(board) || performance.now() >= deadline) throw Error('PRD ASP request deadline exceeded');
    const result = await sourceDeclarations(boards, board, remaining());
    if (result.status !== 'available') throw Error('PRD board ' + result.status);
    declared.set(board, result); return result;
  }
  const root = await declaration(defaultBoard);
  const reachable = new Map<string, any>([[defaultBoard, root]]);
  // The configured board and its declared graph define the public ASP scope.
  const queue = [defaultBoard];
  for (let index = 0; index < queue.length && queue.length <= 64; index++) {
    const board = queue[index], held = await declaration(board);
    reachable.set(board, held);
    for (const child of held.children) {
      const name = path.relative(boards, child.root);
      if (!valid(name) || !inside(boards, child.root)) continue;
      if (!queue.includes(name)) queue.push(name);
    }
  }
  if (queue.length > 64) throw Error('PRD board graph exceeds 64 boards');
  const indexed = new Map<string, any>();
  async function index(board: string): Promise<any> {
    if (indexed.has(board)) return indexed.get(board);
    if (!reachable.has(board)) throw Error('PRD board is outside the declared graph');
    const result = await sourceRecords(boards, board, { action: 'index', expected_source_revision: reachable.get(board).revision },
      remaining(), undefined, { maxItems: 1024, item: publicFields });
    if (!['available', 'partial'].includes(result.status)) throw Error('PRD records ' + result.status);
    indexed.set(board, result); return result;
  }
  const nodes: any[] = [], edges: any[] = [];
  const add = (node: any) => { if (!nodes.some(existing => existing.id === node.id)) nodes.push(node); };
  const edge = (from: string, to: string, kind: string, revision: string) => edges.push({ from, to, kind, revision });
  const expanded = (revision: string) => ({
    nodes: nodes.map(node => ({ ...node, revision })),
    edges: edges.map(link => ({ ...link, revision })),
  });
  const planId = (board: string) => 'plan:' + (board === defaultBoard ? 'root' : board);
  const taskId = (board: string, record: any) => 'task:' + board + '/' + keyOf(record);
  function task(board: string, record: any) {
    const id = taskId(board, record);
    const canonical = path.relative(project, path.join(reachable.get(board).root, record.path));
    const attributes: Record<string, any> = {
      'prd.state': record.state, 'prd.claim': record.claim, 'prd.complexity': record.complexity,
      'prd.scope': { summary: `${record.state} · ${record.checks_done}/${record.checks_total} checks` },
      'prd.checks_done': record.checks_done, 'prd.checks_total': record.checks_total,
      'prd.board': board, 'prd.record': record.path, 'prd.record_revision': record.revision,
    };
    const node = { id, name: record.title, revision: record.revision, tags: ['task', record.state], attributes };
    add(node);
    if (canonical && !canonical.startsWith('..') && !path.isAbsolute(canonical)) {
      const file = 'file:' + canonical.split(path.sep).join('/');
      add({ id: file, name: path.basename(record.path), revision: record.revision });
      edge(id, file, 'recorded-in', record.revision);
    }
    return node;
  }
  if (request.op === 'search') {
    if (typeof request.query !== 'string' || request.query.length > 4096) throw Error('ASP query must be a string of at most 4096 characters');
    const query = request.query.toLocaleLowerCase();
    for (let start = 0; start < queue.length; start += 4) {
      if (nodes.filter(node => node.id.startsWith('task:')).length >= limit) break;
      const batch = queue.slice(start, start + 4);
      const results = await Promise.allSettled(batch.map(board => index(board)));
      for (const [offset, result] of results.entries()) {
        if (result.status === 'rejected') throw result.reason;
        const board = batch[offset];
        for (const record of result.value.items) {
          if (!(record.title + ' ' + keyOf(record) + ' ' + record.state).toLocaleLowerCase().includes(query)) continue;
          if (nodes.filter(node => node.id.startsWith('task:')).length >= limit) break;
          task(board, record);
        }
      }
    }
    return { nodes, edges };
  }
  const entity = request.entity;
  if (typeof entity !== 'string') throw Error('ASP expand requires an entity');
  if (entity.startsWith('plan:')) {
    const match = /^plan:([A-Za-z0-9][A-Za-z0-9_.-]*)(?:#page=(\d+))?$/.exec(entity);
    if (!match) throw Error('Malformed plan identity');
    const board = match[1] === 'root' ? defaultBoard : match[1];
    const result = await index(board), page = Number(match[2] ?? 0);
    const start = page * PAGE;
    if (!Number.isSafeInteger(start) || page && start >= result.items.length) throw Error('Plan page unavailable');
    const revision = result.index_revision;
    add({ id: entity, name: board + (page ? ' tasks ' + (start + 1) + '–' + Math.min(start + PAGE, result.items.length) : ' plan'), revision,
      attributes: { 'prd.total': result.items.length, 'prd.partial': !result.complete, 'prd.page': page, 'prd.page_size': PAGE,
        'prd.scope': { summary: `${result.items.length} tasks${result.complete ? '' : ' · partial'}` } } });
    if (!page) {
      for (const child of reachable.get(board).children) {
        const name = path.relative(boards, child.root);
        if (!reachable.has(name)) continue;
        add({ id: planId(name), name: name + ' plan', revision: reachable.get(name).revision });
        edge(entity, planId(name), 'contains', revision);
      }
      for (let next = 1; next * PAGE < result.items.length; next++) {
        const id = planId(board) + '#page=' + next;
        add({ id, name: 'Tasks ' + (next * PAGE + 1) + '–' + Math.min((next + 1) * PAGE, result.items.length), revision });
        edge(entity, id, 'contains', revision);
      }
    }
    for (const record of result.items.slice(start, start + Math.min(PAGE, limit))) {
      task(board, record); edge(entity, taskId(board, record), 'contains', revision);
    }
    return expanded(revision);
  }
  if (entity.startsWith('task:')) {
    const match = /^task:([^/]+)\/(.+)$/.exec(entity);
    if (!match || !valid(match[1])) throw Error('Malformed task identity');
    const board = match[1], result = await index(board);
    const record = result.items.find((item: any) => keyOf(item) === match[2]);
    if (!record) return { nodes, edges };
    const read = await sourceRecords(boards, board, { action: 'read', expected_source_revision: reachable.get(board).revision,
      path: record.path, expected_revision: record.revision }, remaining());
    if (read.status !== 'available') throw Error('PRD record ' + read.status);
    const doc = parseDocument(read.text, read.path, true), selected = task(board, record);
    const items = checks(read.text);
    selected.attributes['prd.checks'] = items.slice(0, 128);
    selected.attributes['prd.partial'] = items.length > 128;
    const needs = Array.isArray(doc.fm.needs) ? doc.fm.needs : doc.fm.needs == null ? [] : [doc.fm.needs];
    let unresolved = 0;
    for (const need of needs.slice(0, 32)) {
      if (typeof need !== 'string') { unresolved++; continue; }
      const parts = /^@([^/]+)\/(.+)$/.exec(need);
      const targetBoard = parts ? parts[1] : board;
      if (!reachable.has(targetBoard)) { unresolved++; continue; }
      const targetKey = (parts ? parts[2] : need).replace(/^prds\//, '').replace(/\/prd\.md$/, '');
      const targetIndex = await index(targetBoard);
      let matches = targetIndex.items.filter((item: any) => keyOf(item) === targetKey);
      if (!matches.length) matches = targetIndex.items.filter((item: any) => path.basename(keyOf(item)) === targetKey);
      if (matches.length !== 1) { unresolved++; continue; }
      task(targetBoard, matches[0]); edge(entity, taskId(targetBoard, matches[0]), 'depends-on', record.revision);
    }
    selected.attributes['prd.unresolved_dependencies'] = unresolved + Math.max(0, needs.length - 32);
    for (const child of result.items.filter((item: any) => path.dirname(keyOf(item)) === keyOf(record)).slice(0, limit)) {
      task(board, child); edge(entity, taskId(board, child), 'contains', record.revision);
    }
    return expanded(record.revision);
  }
  return { nodes, edges };
}
