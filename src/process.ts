import { spawn } from 'node:child_process';

export type ProcessResult = { output: string; exit_code: number | null; state: string; truncated: boolean };
// Each process is a session owned by this invocation. Never signal journal PIDs.
export async function runProcess(command: string[], options: { cwd: string; timeout?: number; cap?: number; signal?: AbortSignal; input?: string; grace?: number }): Promise<ProcessResult> {
  const cap = options.cap ?? 65536;
  let reason = '', size = 0, truncated = false, force: ReturnType<typeof setTimeout> | undefined;
  const chunks: Buffer[] = [];
  const child = spawn(command[0], command.slice(1), { cwd: options.cwd, detached: true, stdio: ['pipe', 'pipe', 'pipe'] });
  // Bun invalidates ChildProcess.pid after exit. Capture the positive session ID
  // once so a late output chunk can never turn -1 into a signal to PID 1.
  const ownedPid = child.pid;
  const signal = (name: NodeJS.Signals) => {
    if (!ownedPid || ownedPid <= 1) return;
    try { process.kill(-ownedPid, name); }
    catch (error: any) {
      if (error.code === 'ESRCH') return;
      // Darwin reports EPERM for a process group containing only zombies.
      // Confirm that exact condition; never hide a permission failure on live work.
      if (error.code === 'EPERM') {
        const ps = Bun.spawnSync(['ps', '-axo', 'pgid=,stat='], { stdout: 'pipe', stderr: 'pipe' });
        const members = ps.stdout.toString().trim().split('\n').map(line => line.trim().split(/\s+/)).filter(([group]) => Number(group) === ownedPid);
        if (ps.exitCode === 0 && members.every(([, state]) => state.startsWith('Z'))) return;
      }
      throw error;
    }
  };
  function stop(state: string) {
    if (reason) return;
    reason = state; signal('SIGTERM');
    force = setTimeout(() => signal('SIGKILL'), options.grace ?? 1200);
  }
  const timer = setTimeout(() => stop('timed_out'), options.timeout ?? 120_000);
  const abort = () => stop('cancelled');
  options.signal?.addEventListener('abort', abort, { once: true });
  if (options.signal?.aborted) abort();
  for (const stream of [child.stdout, child.stderr]) stream!.on('data', (chunk: Buffer) => {
    const keep = Math.max(0, cap - size);
    chunks.push(chunk.subarray(0, keep)); size += Math.min(keep, chunk.length);
    if (chunk.length > keep) { truncated = true; stop('output_limit'); }
  });
  child.stdin!.on('error', () => {});
  child.stdin!.end(options.input);
  try {
    const code = await new Promise<number | null>((resolve, reject) => { child.on('error', reject); child.on('close', resolve); });
    // A worker may exit while its child keeps running. Close the owned group too.
    signal('SIGKILL');
    return { output: Buffer.concat(chunks).toString('utf8'), exit_code: code, state: reason || (code === 0 ? 'completed' : 'failed'), truncated };
  } finally { clearTimeout(timer); if (force) clearTimeout(force); options.signal?.removeEventListener('abort', abort); }
}
