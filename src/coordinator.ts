import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { atomic, codeRepo, hash, members, mutationKeys, scan, specs, withLocks } from './records';
import { clash, plan } from './planner';
import { argumentsOf, completionProblem, lane, transition } from './lifecycle';
import { runProcess } from './process';

export async function coordinate(board: string, args: string[], signal?: AbortSignal) {
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
  const lockPaths = [board, ...members(board).map(([, b]) => b)].map(b => path.join(b, '.state/run-lock.sqlite'));
  const completed: string[] = [], failed: { ref: string; reason: string }[] = [], attempts = new Map<string, number>();
  const active = new Map<string, { feet: string[]; work: Promise<void> }>();
  const checkpoint = () => atomic(path.join(board, '.state/run.json'), JSON.stringify({ status: controller.signal.aborted ? 'stopped' : active.size ? 'running' : 'idle', scope: scope ?? null, live: [...active.keys()], completed, failed, attempts: Object.fromEntries(attempts), updated_at: new Date().toISOString() }, null, 2) + '\n');
  try {
    return await withLocks(lockPaths, async () => {
      let fills = 0;
      for (;;) {
        const frontier = plan(board, workers, scope);
        let launched = false;
        if (!controller.signal.aborted && (!opts.once || fills === 0)) {
          for (const row of frontier.rows) {
            if (active.size >= workers) break;
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
            const values: Record<string, string> = { board, rel: row.rel, role: row.role, prompt, worker };
            const command = adapter.command.map((part: string) => part.replace(/\{(board|rel|role|prompt|worker)\}/g, (_: string, key: string) => values[key]));
            command[0] = executable;
            const work = (async () => {
              try {
                const result = await runProcess(command, { cwd, signal: controller.signal, timeout: seconds * 1000, cap: 1048576 });
                atomic(path.join(board, '.state/run-' + hash(row.rel).slice(0, 16) + '.log'), result.output);
                const after = scan(board).get(row.rel);
                let problem = result.state !== 'completed' ? result.state + ': ' + result.output.slice(-2048) : !after ? 'PRD disappeared' : hash(after.text + specs(after).map(s => s.text).join('')) === fingerprint ? 'worker exited without persisted progress' : after.state === 'done' ? completionProblem(after) : after.fm.claim ? 'worker left its claim unresolved' : null;
                if (problem) failed.push({ ref: row.rel, reason: problem });
                else if (after!.state === 'done') completed.push(row.rel);
              } catch (error) { failed.push({ ref: row.rel, reason: String(error) }); }
              finally { active.delete(row.rel); checkpoint(); }
            })();
            active.set(row.rel, { feet: row.feet, work }); launched = true; checkpoint();
          }
          if (launched) fills++;
        }
        if (!active.size) break;
        await Promise.race([...active.values()].map(a => a.work));
      }
      checkpoint();
      const remaining = plan(board, workers, scope).rows;
      return { status: controller.signal.aborted ? 'stopped' : failed.length ? 'failed' : remaining.length ? 'blocked' : 'completed', completed, failed, remaining };
    }, 0);
  } finally { controller.abort(); await Promise.allSettled([...active.values()].map(a => a.work)); clearTimeout(deadline); signal?.removeEventListener('abort', abort); }
}
