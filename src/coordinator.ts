import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { atomic, codeRepo, document, hash, mutationKeys, openBoxes, resolve, scan, specs, withLocks } from './records';
import { clash, plan } from './planner';
import { argumentsOf, completionProblem, lane, transition } from './lifecycle';
import { runProcess } from './process';

export async function coordinate(board: string, args: string[], signal?: AbortSignal, emit?: (event: any) => void) {
  const { pos, opts } = argumentsOf(args);
  const workers = Number(opts.workers) || 3;
  if (pos.length > 1) throw Error('run accepts at most one PRD scope');
  const scope = pos[0], initial = plan(board, workers, scope);
  if (opts.dry) return { ...initial, completed: [], failed: [], status: 'preview' };
  if (typeof opts.adapter !== 'string' || !/^[A-Za-z0-9_-]{1,64}$/.test(opts.adapter)) throw Error('run requires an explicit configured adapter; use --dry to preview');
  const adapters = process.env.PRD_ADAPTER_DIR || path.resolve(import.meta.dir, '../.cartridge/adapters');
  const adapter = JSON.parse(fs.readFileSync(path.join(adapters, opts.adapter + '.json'), 'utf8'));
  if (!Array.isArray(adapter.command) || !adapter.command.length || !adapter.command.every((p: unknown) => typeof p === 'string')) throw Error('adapter command must be a nonempty string array');
  const executable = Bun.which(process.env.PRD_ADAPTER_BIN || adapter.command[0]);
  if (!executable) throw Error('configured adapter executable is unavailable');
  const seconds = opts.deadline ? Number(opts.deadline) : 1200;
  if (!Number.isFinite(seconds) || seconds < 0.05 || seconds > 86400) throw Error('invalid run deadline');
  const controller = new AbortController(), abort = () => controller.abort();
  signal?.addEventListener('abort', abort, { once: true });
  if (signal?.aborted) abort();
  const deadline = setTimeout(abort, seconds * 1000);
  const lockPaths = [board, ...[...scan(board).values()].map(p => p.board)].map(b => path.join(b, '.state/run-lock.sqlite'));
  const completed: string[] = [], failed: { ref: string; reason: string }[] = [], attempts = new Map<string, number>();
  const active = new Map<string, { owner: string; feet: string[]; work: Promise<void> }>();
  const checkpoint = (status?: string) => atomic(path.join(board, '.state/run.json'), JSON.stringify({ status: status ?? (controller.signal.aborted ? 'stopped' : active.size ? 'running' : 'idle'), scope: scope ?? null, live: [...active.keys()], completed, failed, attempts: Object.fromEntries(attempts), updated_at: new Date().toISOString() }, null, 2) + '\n');
  try {
    return await withLocks(lockPaths, async () => {
      let fills = 0;
      for (;;) {
        const frontier = plan(board, workers, scope);
        emit?.({ type: 'plan.updated', demand: frontier.demand, snapshot: frontier.snapshot });
        let launched = false;
        if (!controller.signal.aborted && (!opts.once || fills === 0)) {
          for (const row of frontier.rows) {
            if (active.size >= workers) break;
            const ownerLimit = Number(document(path.join(row.owner_path, 'settings.md')).fm.workers ?? workers);
            if (!Number.isInteger(ownerLimit) || ownerLimit < 1 || ownerLimit > 32) throw Error('invalid member worker limit');
            if ([...active.values()].filter(a => a.owner === row.owner_path).length >= ownerLimit) continue;
            if (!row.dispatchable || active.has(row.rel) || failed.some(f => f.ref === row.rel) || (attempts.get(row.rel) ?? 0) >= 5 || [...active.values()].some(a => clash(a.feet, row.feet))) continue;
            const worker = 'prd-run-' + randomUUID();
            let fingerprint = '', prompt = '', cwd = '';
            try {
              await withLocks(mutationKeys(board), async () => {
                if (row.role !== 'collector') await transition('claim', board, [row.rel, worker]);
                const prd = scan(board).get(row.rel)!;
                fingerprint = hash(prd.text + specs(prd).map(s => s.text).join(''));
                prompt = await transition('brief', board, [row.rel, '--role', row.role]);
                cwd = fs.existsSync(lane(prd).directory) ? lane(prd).directory : codeRepo(prd);
              });
            } catch (error) { failed.push({ ref: row.rel, reason: String(error) }); continue; }
            attempts.set(row.rel, (attempts.get(row.rel) ?? 0) + 1);
            emit?.({ type: 'worker.started', ref: row.rel, worker, role: row.role });
            const values: Record<string, string> = { board, rel: row.rel, role: row.role, prompt, worker };
            const command = adapter.command.map((part: string) => part.replace(/\{(board|rel|role|prompt|worker)\}/g, (_: string, key: string) => values[key]));
            command[0] = executable;
            const work = (async () => {
              try {
                const result = await runProcess(command, { cwd, signal: controller.signal, timeout: seconds * 1000, cap: 1048576 });
                atomic(path.join(board, '.state/run-' + hash(row.rel).slice(0, 16) + '.log'), result.output);
                let after = scan(board).get(row.rel);
                if (result.state === 'completed' && after?.state === 'claimed' && String(after.fm.claim).split(/\s/)[0] === worker && !openBoxes(after.text) && specs(after).length && specs(after).every(s => !openBoxes(s.text))) {
                  await withLocks(mutationKeys(board), async () => {
                    const current = scan(board).get(row.rel)!;
                    if (String(current.fm.claim).split(/\s/)[0] !== worker) throw Error('worker claim changed before collection');
                    await transition('collect', board, [row.rel], controller.signal);
                  });
                  after = scan(board).get(row.rel);
                }
                let problem = result.state !== 'completed' ? result.state + ': ' + result.output.slice(-2048) : !after ? 'PRD disappeared' : hash(after.text + specs(after).map(s => s.text).join('')) === fingerprint ? 'worker exited without persisted progress' : after.state === 'done' ? completionProblem(after) : after.fm.claim ? 'worker left its claim unresolved' : null;
                if (problem) failed.push({ ref: row.rel, reason: problem });
                else if (after!.state === 'done') completed.push(row.rel);
                emit?.({ type: 'worker.finished', ref: row.rel, worker, state: problem ? 'failed' : result.state, exit_code: result.exit_code });
                if (after?.state !== row.state) emit?.({ type: 'transition.applied', ref: row.rel, before: row.state, after: after?.state });
                if (after?.state === 'done') emit?.({ type: 'verification.completed', ref: row.rel, verified: !problem, commit: after.fm.commit ?? null });
              } catch (error) { failed.push({ ref: row.rel, reason: String(error) }); emit?.({ type: 'worker.finished', ref: row.rel, worker, state: 'failed', exit_code: null }); }
              finally { active.delete(row.rel); checkpoint(); }
            })();
            active.set(row.rel, { owner: row.owner_path, feet: row.feet, work }); launched = true; checkpoint();
          }
          if (launched) fills++;
        }
        if (!active.size) break;
        await Promise.race([...active.values()].map(a => a.work));
      }
      const finalGraph = scan(board), selected = scope ? resolve(finalGraph, scope).ref : null;
      for (const prd of finalGraph.values()) {
        if (prd.state !== 'done' || selected && prd.ref !== selected && !prd.ref.startsWith(selected + '/')) continue;
        const reason = completionProblem(prd, finalGraph);
        if (reason && !failed.some(f => f.ref === prd.ref)) failed.push({ ref: prd.ref, reason });
      }
      const remaining = plan(board, workers, scope).rows;
      const status = controller.signal.aborted ? 'stopped' : failed.length ? 'failed' : remaining.length ? 'blocked' : 'completed';
      checkpoint(status);
      return { status, completed, failed, remaining, owned: [...attempts.keys()] };
    }, 0);
  } finally { controller.abort(); await Promise.allSettled([...active.values()].map(a => a.work)); clearTimeout(deadline); signal?.removeEventListener('abort', abort); }
}
