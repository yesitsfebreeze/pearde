import fs from 'node:fs';
import path from 'node:path';
import { adoptionWarnings, atomic, canonicalBoard, contained, document, dropOrphanFields, fieldsProblem, fieldsRefusal, hash, members, mutationKeys, resolve, scan, snapshot, withLocks } from './records';
import { gantt, plan } from './planner';
import { argumentsOf, transition, verifiedStatus } from './lifecycle';
import { coordinate } from './coordinator';

const mutations = new Set(['add', 'claim', 'release', 'specced', 'refine', 'collect', 'defer', 'retry', 'unblock', 'adopt']);
export async function execute(operation: string, board: string, args: string[] = [], signal?: AbortSignal, emit?: (event: any) => void) {
  board = canonicalBoard(board);
  const envelope: any = { operation, board, exit_code: 0, output: '', error: '', changed: [], verification: [] };
  const { opts, pos } = argumentsOf(args);
  const limit = opts.limit ? Number(opts.limit) : 20, offset = opts.offset ? Number(opts.offset) : 0;
  if (!Number.isInteger(limit) || limit < 1 || limit > 200 || !Number.isInteger(offset) || offset < 0) throw Error('invalid pagination');
  const work = async () => {
    const before = snapshot(scan(board));
    try {
      if (signal?.aborted) throw Error('invocation cancelled');
      if (operation === 'plan' || operation === 'scan') {
        const data: any = operation === 'plan' ? plan(board, Number(opts.workers) || 0, pos[0]) : { rows: Object.values(before), snapshot: hash(JSON.stringify(before)) };
        const total = data.rows.length;
        data.rows = data.rows.slice(offset, offset + limit);
        if (data.waves) { const addresses = new Set(data.rows.map((r: any) => r.addr)); data.waves = data.waves.map((wave: string[]) => wave.filter(a => addresses.has(a))).filter((w: string[]) => w.length); }
        envelope.data = { ...data, total, limit, offset, next_offset: offset + limit < total ? offset + limit : null };
      } else if (operation === 'read' || operation === 'verified-status') {
        if (pos.length !== 1) throw Error('read requires one reference');
        if (operation === 'read' && pos[0].endsWith('.md') && !pos[0].endsWith('/prd.md')) {
          const file = contained(board, pos[0]); envelope.data = { path: file, text: document(file).text };
        } else {
          const prd = resolve(scan(board), pos[0]);
          envelope.data = operation === 'read' ? { ...before[prd.ref], text: prd.text } : verifiedStatus(prd);
          if (operation === 'verified-status') envelope.verification = [envelope.data];
        }
      } else if (operation === 'gantt') {
        envelope.output = gantt(board);
        atomic(path.join(board, 'gantt.md'), envelope.output);
      } else if (operation === 'next') {
        const current = plan(board); envelope.data = current.rows.find(row => row.dispatchable) ?? { status: 'blocked-or-complete', notes: current.notes };
      } else if (operation === 'status') {
        const counts: Record<string, number> = {}; for (const p of scan(board).values()) counts[p.state] = (counts[p.state] ?? 0) + 1; envelope.data = counts;
      } else if (operation === 'members') envelope.data = Object.fromEntries(members(board));
      else if (operation === 'run') { envelope.data = await coordinate(board, args, signal, emit); if (['failed', 'stopped'].includes(envelope.data.status)) envelope.exit_code = 2; }
      else if (mutations.has(operation) || operation === 'brief') envelope.output = await transition(operation, board, args, signal);
      else if (operation === 'check') {
        const current = plan(board); const problems = [...current.notes, ...current.rows.filter(r => r.held?.includes('outside this graph')).map(r => r.rel + ': ' + r.held)];
        // Every board in the graph, not just the ones that still hold a record: a board whose last record
        // was rehomed elsewhere must still be swept, or its orphaned values are never dropped or surfaced.
        // scan() above already rejected member cycles, so this walk terminates.
        const graph = scan(board), reach = (owner: string): string[] => [owner, ...members(owner).flatMap(([, target]) => reach(target))];
        const owners = [...new Set(reach(board))];
        const warnings: string[] = [];
        // check writes and deletes under <owner>/.state/fields; a store it cannot maintain is a planning
        // problem naming the owner board that failed, not a raw errno out of a read.
        let owner = board;
        try {
          for (owner of owners) warnings.push(...dropOrphanFields(owner));
          // One pause per check, not one per record: a board-wide tamper must not serialize into minutes.
          const suspect = [...graph.values()].filter(prd => { owner = prd.board; return fieldsProblem(prd.file, true); });
          if (suspect.length) Bun.sleepSync(50);
          for (const prd of suspect) { owner = prd.board; const problem = fieldsProblem(prd.file, true); if (problem) problems.push(fieldsRefusal(prd, problem)); }
          for (owner of owners) warnings.push(...adoptionWarnings(owner, graph));
        } catch (error: any) {
          problems.push(owner + ': the engine field store is unavailable (' + (error.code ?? error.message) + '); check records, drops and reads state, claim and commit under ' + path.join(owner, '.state/fields') + ' and needs write access there');
        }
        envelope.data = { records: graph.size, problems, warnings }; if (problems.length) envelope.exit_code = 2;
      } else if (['workflow', 'grammar', 'memo', 'questions'].includes(operation)) {
        if (pos[0] !== 'check' && pos[0] !== 'list') throw Error(operation + ' supports check or list; edit authored records through the memo system');
        const setting = document(path.join(board, 'settings.md')).fm[operation === 'workflow' ? 'workflows' : operation === 'memo' ? 'memos' : operation];
        if (!setting && operation !== 'questions') throw Error('no ' + operation + ' library configured');
        const files = operation === 'questions' ? [...scan(board).values()].filter(p => p.state === 'question').map(p => p.file) : (() => { const target = path.resolve(board, String(setting)); return fs.statSync(target).isDirectory() ? fs.readdirSync(target).filter(n => n.endsWith('.md')).map(n => path.join(target, n)) : [target]; })();
        files.forEach(file => document(file)); envelope.data = { files, count: files.length };
      } else throw Error('unknown operation ' + operation);
    } catch (error) { envelope.exit_code = 2; envelope.error = error instanceof Error ? error.message : String(error); }
    const afterGraph = scan(board), after = snapshot(afterGraph);
    envelope.changed = [...new Set([...Object.keys(before), ...Object.keys(after)])].sort().filter(ref => JSON.stringify(before[ref]) !== JSON.stringify(after[ref])).map(ref => ({ ref, before: before[ref] ?? null, after: after[ref] ?? null }));
    if (operation === 'run') envelope.changed = envelope.changed.filter((change: any) => (envelope.data?.owned ?? []).some((ref: string) => change.ref === ref || change.ref.startsWith(ref + '/')));
    if (['collect', 'run'].includes(operation) && !opts.dry) envelope.verification = envelope.changed.filter((c: any) => c.after?.state === 'done').map((c: any) => verifiedStatus(afterGraph.get(c.ref)!));
    if (emit) {
      if (operation === 'plan') emit({ type: 'plan.updated', operation, demand: envelope.data?.demand ?? 0, snapshot: envelope.data?.snapshot });
      if (operation !== 'run') for (const change of envelope.changed) emit({ type: 'transition.applied', operation, ref: change.ref, before: change.before?.state, after: change.after?.state });
      if (operation !== 'run') for (const proof of envelope.verification) emit({ type: 'verification.completed', operation, ref: proof.ref, verified: proof.verified, commit: proof.commit });
    }
    return envelope;
  };
  return mutations.has(operation) ? withLocks(mutationKeys(board), work) : work();
}
