import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import net from 'node:net';

export type ProcessResult = { output: string; exit_code: number | null; state: string; truncated: boolean; cleanup_error?: string; events?: { received: number; dropped: number; error?: string } };
// Each process is a session owned by this invocation. Never signal journal PIDs.
export async function runProcess(command: string[], options: { cwd: string; timeout?: number; cap?: number; signal?: AbortSignal; input?: string; grace?: number; onEvent?: (event: any) => void }): Promise<ProcessResult> {
  const cap = options.cap ?? 65536;
  let reason = '', cleanupError = '', size = 0, truncated = false, force: ReturnType<typeof setTimeout> | undefined;
  const chunks: Buffer[] = [];
  const eventDirectory = options.onEvent ? fs.mkdtempSync(path.join(os.tmpdir(), 'prd-events-')) : undefined;
  const eventPath = eventDirectory ? path.join(eventDirectory, 'events.sock') : undefined;
  const server = eventPath ? net.createServer() : undefined;
  if (server) await new Promise<void>((resolve, reject) => { server.once('error', reject); server.listen(eventPath, resolve); });
  const child = spawn(command[0], command.slice(1), { cwd: options.cwd, detached: true, stdio: ['pipe', 'pipe', 'pipe'], env: { ...process.env, PRD_NATIVE_EVENT_SOCKET: eventPath, PRD_NATIVE_EVENT_FD: undefined } });
  const events: { received: number; dropped: number; error?: string } = { received: 0, dropped: 0 };
  let eventSocket: net.Socket | undefined;
  let eventDrain: Promise<void> = Promise.resolve();
  if (options.onEvent) {
    let drained!: () => void;
    eventDrain = new Promise<void>(resolve => { drained = resolve; });
    server!.on('connection', stream => {
    if (eventSocket) { stream.destroy(); events.dropped++; return; }
    eventSocket = stream;
    stream.once('end', drained); stream.once('close', drained); stream.once('error', drained);
    let pending = '', discarding = false, bytes = 0;
    const drop = (error: string) => { events.dropped++; events.error = error.slice(0, 256); };
    stream.setEncoding('utf8');
    stream.on('data', (chunk: string) => {
      for (const part of chunk.split(/(?<=\n)/)) {
        if (!discarding) pending += part;
        if (Buffer.byteLength(pending) > 8192) { pending = ''; discarding = true; }
        if (!part.endsWith('\n')) continue;
        events.received++;
        if (discarding) { discarding = false; drop('event exceeds 8192-byte frame cap'); continue; }
        const line = pending; pending = '';
        if (events.received > 256 || bytes + Buffer.byteLength(line) > 65536) { drop('event count or byte budget exceeded'); continue; }
        bytes += Buffer.byteLength(line);
        try {
          const event = JSON.parse(line);
          if (!event || typeof event !== 'object' || Array.isArray(event)) throw Error('event must be an object');
          options.onEvent!(event);
        } catch (error) { drop(String(error)); }
      }
    });
    stream.on('end', () => { if (pending || discarding) { events.received++; drop('unterminated event frame'); } });
    stream.on('error', error => { events.error = String(error).slice(0, 256); });
    });
  }
  // Bun invalidates ChildProcess.pid after exit. Capture the positive session ID
  // once so a late output chunk can never turn -1 into a signal to PID 1.
  const ownedPid = child.pid;
  const liveGroup = () => {
    if (!ownedPid || ownedPid <= 1) return false;
    const ps = Bun.spawnSync(['ps', '-axo', 'pgid=,stat='], { stdout: 'pipe', stderr: 'pipe', timeout: 1000 });
    if (ps.exitCode !== 0) throw Error('cannot confirm owned process group termination');
    return ps.stdout.toString().trim().split('\n').map(line => line.trim().split(/\s+/)).some(([group, state]) => Number(group) === ownedPid && !state.startsWith('Z'));
  };
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
    reason = state;
    try { signal('SIGTERM'); } catch (error) { cleanupError = String(error); }
    force = setTimeout(() => { try { signal('SIGKILL'); } catch (error) { cleanupError = String(error); } }, options.grace ?? 1200);
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
    // Wait for the owned group, including a child whose leader already exited.
    // Sending a signal alone is not confirmation that its footprint is free.
    if (force) clearTimeout(force);
    try {
      if (liveGroup()) {
        signal('SIGTERM');
        const graceful = Date.now() + (options.grace ?? 1200);
        while (liveGroup() && Date.now() < graceful) await Bun.sleep(25);
        if (liveGroup()) signal('SIGKILL');
        const forced = Date.now() + 1000;
        while (liveGroup() && Date.now() < forced) await Bun.sleep(25);
        if (liveGroup()) throw Error('owned process group survived cleanup deadline');
      }
    } catch (error) { cleanupError = String(error); }
    // The process and its event socket have separate lifetimes. Drain the final
    // frames before returning, without inheriting a runtime-owned extra fd.
    if (eventSocket) {
      let drainTimer: ReturnType<typeof setTimeout> | undefined;
      await Promise.race([eventDrain, new Promise<void>(resolve => {
        drainTimer = setTimeout(() => { events.dropped++; events.error = 'event stream did not close after process cleanup'; eventSocket?.destroy(); resolve(); }, 1000);
      })]);
      if (drainTimer) clearTimeout(drainTimer);
    }
    return { output: Buffer.concat(chunks).toString('utf8'), exit_code: code, state: cleanupError ? 'cleanup_uncertain' : reason || (code === 0 ? 'completed' : 'failed'), truncated, ...(cleanupError ? { cleanup_error: cleanupError } : {}), ...(options.onEvent ? { events } : {}) };
  } finally { clearTimeout(timer); if (force) clearTimeout(force); options.signal?.removeEventListener('abort', abort); eventSocket?.destroy(); server?.close(); if (eventDirectory) fs.rmSync(eventDirectory, { recursive: true, force: true }); }
}
