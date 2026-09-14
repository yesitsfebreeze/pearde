import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import { atomic, contained, hash, inside, real, relative, sourceDeclarations, declarationFailure } from './records';
import { ROOT } from './cli';
import { sourceRecords, sourceRecordFailure } from './source-records';
import { runProcess } from './process';
import { Wire } from './wire';

const OPS = ['scan', 'plan', 'gantt', 'read', 'brief', 'next', 'add', 'refine', 'specced', 'claim', 'release', 'collect', 'run', 'status', 'stop'];
const flags: Record<string, Record<string, string>> = {
  scan: { limit: 'page', offset: 'offset' }, plan: { workers: 'count', limit: 'page', offset: 'offset' }, gantt: {}, read: {}, next: {},
  brief: { as: 'text', role: 'text', worker: 'text' }, add: { as: 'text', priority: 'integer', parent: 'path', dry: 'switch' },
  refine: { as: 'text', dry: 'switch' }, specced: { as: 'text', blast: 'text', workflow: 'text', route: 'text', lane: 'text', dry: 'switch', check: 'switch' },
  claim: { as: 'text', dry: 'switch' }, release: { as: 'text', dry: 'switch' }, collect: { as: 'text', report: 'file', dry: 'switch' },
  run: { workers: 'count', deadline: 'deadline', dry: 'switch', once: 'switch' },
};
const counts: Record<string, number[]> = { scan: [0, 0], plan: [0, 0], gantt: [0, 0], next: [0, 0], read: [1, 1], brief: [1, 1], add: [1, 16], refine: [1, 1], specced: [1, 1], claim: [2, 2], release: [2, 2], collect: [1, 1], run: [0, 1] };
const object = (v: any) => v !== null && typeof v === 'object' && !Array.isArray(v);
const bytes = (v: any) => Buffer.byteLength(JSON.stringify(v));
const id = () => randomUUID().replaceAll('-', '');
export const result = (value: any, error = false) => ({ content: JSON.stringify(value), error });
export function describe() {
  return { name: 'prd', description: 'Plan centralized PRD boards, prepare briefs, and perform checked transitions. Host agents follow the run-board memo. External run requires a trusted configured adapter. status/stop address only this session’s jobs. Memory provides context; PRD records remain authoritative.', input_schema: { type: 'object', additionalProperties: false, required: ['op'], properties: { op: { type: 'string', enum: OPS }, board: { type: 'string', maxLength: 256 }, args: { type: 'array', maxItems: 64, items: { type: 'string', maxLength: 8192 } } } } };
}
export function contextKey(context: any) {
  if (!object(context) || Object.keys(context).sort().join() !== 'call,cwd,run,session') throw Error('call requires trusted session, run, call and cwd context');
  for (const key of ['session', 'run', 'call']) if (typeof context[key] !== 'string' || !context[key].trim() || context[key].length > 256 || context[key].includes('\0')) throw Error('invalid invocation context');
  if (typeof context.cwd !== 'string' || !path.isAbsolute(context.cwd) || context.cwd.length > 4096 || context.cwd.includes('\0')) throw Error('context.cwd must be an absolute workspace directory');
  return JSON.stringify([context.session, context.run, context.call]);
}
export class Service {
  root: string; boards: string; state: string; defaultBoard: string; timeout: number; jobTimeout: number; outputCap: number; adapter?: string;
  instance = id(); closed = false;
  declarationReads = new Set<Promise<unknown>>();
  cancelled = new Map<string, AbortController>(); started = new Set<string>(); jobs = new Map<string, any>(); tasks = new Set<Promise<any>>(); deliveries = new Map<string, Promise<any>>();
  constructor(config: any = {}, public host?: Pick<Wire, 'call' | 'publish'>) {
    const allowed = ['root', 'default_board', 'timeout_seconds', 'max_output_bytes', 'adapter', 'job_timeout_seconds'];
    if (!object(config) || Object.keys(config).some(k => !allowed.includes(k))) throw Error('unknown PRD configuration');
    this.root = real(path.resolve(config.root ?? ROOT)); this.boards = real(path.join(this.root, '.cartridge/boards')); this.state = path.join(this.root, '.cartridge/.state/prd-service');
    this.defaultBoard = config.default_board ?? 'root'; this.timeout = config.timeout_seconds ?? 120; this.jobTimeout = config.job_timeout_seconds ?? 1200; this.outputCap = config.max_output_bytes ?? 65536;
    // How large each cap may be is declared in `cartridge.json` and the host has
    // refused anything outside it already; a second copy of the bounds here is
    // only a way for the two to drift apart. What stays is what no declaration
    // can promise a caller who arrives without a host: a usable number.
    for (const value of [this.timeout, this.jobTimeout, this.outputCap]) if (typeof value !== 'number' || !Number.isFinite(value) || value <= 0) throw Error('invalid PRD execution caps');
    this.outputCap = Math.floor(this.outputCap); this.adapter = config.adapter ?? undefined;
    if (this.adapter !== undefined && (typeof this.adapter !== 'string' || !/^[A-Za-z0-9_-]{1,64}$/.test(this.adapter))) throw Error('invalid configured adapter');
    this.board(this.defaultBoard);
  }
  board(name: string) {
    if (typeof name !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9_.-]{0,255}$/.test(name)) throw Error('board must name a centralized board');
    const board = contained(this.boards, name);
    if (!fs.existsSync(path.join(board, 'settings.md'))) throw Error('board is missing');
    return board;
  }
  prepare(request: any) {
    if (!object(request) || Object.keys(request).some(k => !['op', 'board', 'args'].includes(k))) throw Error('input accepts only op, board and args; context is host-owned');
    const op = request.op, args = request.args ?? [];
    if (!OPS.includes(op)) throw Error('unknown PRD operation');
    if (!Array.isArray(args) || args.length > 64 || args.some(a => typeof a !== 'string' || a.length > 8192 || a.includes('\0')) || args.reduce((n, a) => n + a.length, 0) > 32768) throw Error('invalid or oversized PRD arguments');
    const board = this.board(request.board ?? this.defaultBoard);
    if (op === 'status' || op === 'stop') { if (args.length !== 1 || !/^[a-f0-9]{32}$/.test(args[0])) throw Error('status/stop require one job ID'); return { op, board, args }; }
    const output: string[] = [], pos: string[] = [], seen = new Set<string>();
    for (let i = 0; i < args.length; i++) {
      const token = args[i];
      if (!token.startsWith('-')) { pos.push(token); output.push(token); continue; }
      const [flag, ...rest] = token.split('='), name = flag.slice(2), kind = token.startsWith('--') ? flags[op][name] : null;
      if (!kind || seen.has(name)) throw Error(op + ': unsupported or duplicate argument ' + flag); seen.add(name);
      if (kind === 'switch') { if (rest.length) throw Error('switch takes no value'); output.push(flag); continue; }
      let value = rest.length ? rest.join('=') : args[++i];
      if (!value || value.startsWith('-') && kind !== 'integer') throw Error(flag + ' requires a value');
      if (['integer', 'count', 'deadline', 'page', 'offset'].includes(kind)) {
        if (!/^-?\d+$/.test(value) || !Number.isSafeInteger(Number(value))) throw Error('expected integer');
        const number = Number(value), range: Record<string, number[]> = { count: [1, 32], page: [1, 50], offset: [0, 100000], deadline: [1, this.jobTimeout] };
        if (range[kind] && (number < range[kind][0] || number > range[kind][1])) throw Error(flag + ' is outside its limit');
      }
      if (kind === 'path' || kind === 'file') { relative(value); const file = contained(board, value); if (kind === 'file' && !fs.existsSync(file)) throw Error('report must exist under selected board'); }
      output.push(flag, value);
    }
    const [low, high] = counts[op]; if (pos.length < low || pos.length > high) throw Error(op + ' has wrong positional argument count');
    if (pos.length && op !== 'add') { relative(pos[0]); contained(board, pos[0]); contained(board, 'prds/' + pos[0]); if (op === 'run' && ['all', 'global'].includes(pos[0])) throw Error('run must stay on selected board'); }
    if (op === 'run') { if (!this.adapter) throw Error('external run needs trusted config.adapter; use next/brief for host-driven work'); output.push('--adapter', this.adapter); }
    return { op, board, args: output };
  }
  async execute(op: string, board: string, args: string[], controller: AbortController, timeout: number, context?: any) {
    if (controller.signal.aborted || this.closed) return { op, state: 'cancelled', output: '', exit_code: null } as any;
    const delivery = { published: 0, unavailable: 0 };
    const processResult = await runProcess([process.execPath, path.join(ROOT, 'src/cli.ts'), op, '--board', board, '--json', ...args], { cwd: this.root, timeout: timeout * 1000, cap: ['plan', 'scan', 'run'].includes(op) ? 1048576 : this.outputCap, signal: controller.signal, grace: 12_000, onEvent: event => {
      if (!['plan.updated', 'worker.started', 'worker.finished', 'transition.applied', 'verification.completed'].includes(event.type)) throw Error('unknown native domain event');
      if (!context || !this.host) { delivery.unavailable++; return; }
      try { this.host.publish('prd', { ...event, schema_version: 1, operation: op, board: path.basename(board), session: context.session, run: context.run, call: context.call }); delivery.published++; }
      catch { delivery.unavailable++; }
    } });
    let outcome: any = { op, board: path.basename(board), ...processResult, effects: processResult.state === 'completed' ? 'see engine output' : 'inspect board before retrying' };
    if (['completed', 'failed'].includes(processResult.state)) {
      try {
        const native = JSON.parse(processResult.output);
        if (!object(native) || !Number.isInteger(native.exit_code)) throw Error('missing engine envelope');
        outcome.output = native.output ?? ''; outcome.state = native.exit_code ? 'failed' : 'completed';
        for (const field of ['data', 'changed', 'verification', 'error']) if (field in native) outcome[field] = native[field];
        if (native.event_errors) { delivery.unavailable += Number(native.event_errors); processResult.events = { ...processResult.events!, error: String(native.event_error ?? 'native event delivery failed') }; }
      } catch (error) { outcome.state = 'failed'; outcome.error = 'invalid native engine response: ' + String(error); }
    }
    outcome.events = { ...processResult.events, ...delivery };
    return outcome;
  }
  result(value: any, error = false) {
    const answer = result(value, error);
    if (bytes(answer) <= this.outputCap) return answer;
    const identifier = id(), file = path.join(this.state, 'responses', identifier + '.json');
    // Budget the final serialized ToolResult, including JSON string escaping.
    // Keep proof and diagnostics even when the caller needs a smaller response.
    atomic(file, JSON.stringify(answer));
    return result({ state: 'output_limit', truncated: true, response_id: identifier, original_state: typeof value.state === 'string' ? value.state.slice(0, 64) : null, details: 'full ToolResult retained in service responses journal; inspect before retrying' }, true);
  }
  saveJob(job: any) { atomic(path.join(this.state, job.job_id + '.json'), JSON.stringify(job)); }
  publicJob(job: any) {
    if (bytes(job) <= this.outputCap) return { ...job };
    return { job_id: job.job_id, state: job.state, op: job.op, board: job.board, exit_code: job.exit_code, started_at: job.started_at, finished_at: job.finished_at, events: job.events, verification_count: job.verification?.length ?? 0, changed_count: job.changed?.length ?? 0, truncated: true, details: 'full result retained in durable job journal' };
  }
  job(op: string, identifier: string, context: any) {
    let job = this.jobs.get(identifier);
    if (!job) { const file = path.join(this.state, identifier + '.json'); if (!fs.existsSync(file) || fs.statSync(file).size > 2 * 1048576) throw Error('unknown or invalid job'); job = JSON.parse(fs.readFileSync(file, 'utf8')); }
    if (job.session !== context.session) throw Error('job belongs to another session');
    if (op === 'stop') { if (!this.jobs.has(identifier)) throw Error('job is not owned by this service instance; no stale PID was signalled'); this.cancelled.get(job.invocation)?.abort(); return { job_id: identifier, state: 'stop_requested' }; }
    if (job.instance !== this.instance && job.state === 'running') job = { ...job, state: 'interrupted', effects: 'previous service ended; inspect board before retrying' };
    return this.publicJob(job);
  }
  publish(op: string, board: string, args: string[], context: any, outcome: any) {
    const refs = (outcome.changed ?? []).map((c: any) => c.ref).filter((r: any) => typeof r === 'string');
    const event = { schema_version: 1, type: 'command.' + outcome.state, operation: op, board: path.basename(board), ref: refs.length === 1 ? refs[0] : args[0]?.startsWith('-') ? null : args[0] ?? null, refs, session: context.session, run: context.run, call: context.call, exit_code: outcome.exit_code ?? null };
    try { if (!this.host) throw Error('host unavailable'); this.host.publish('prd', event); return { ...event, delivery: 'submitted' }; }
    catch (error) { return { ...event, delivery: 'unavailable', delivery_error: String(error) }; }
  }
  /** A memory call bounded to three seconds; memory is context and never holds up planning. */
  memory(args: any) {
    if (!this.host) return Promise.reject(Error('memory provider unavailable'));
    let timer: ReturnType<typeof setTimeout> | undefined;
    const expired = new Promise<never>((_, reject) => { timer = setTimeout(() => reject(Error('memory request timed out; outcome may be unknown')), 3000); });
    return Promise.race([this.host.call('memory', args), expired]).finally(() => clearTimeout(timer));
  }
  async recall(board: string, args: string[]) {
    const authority = 'context only; PRD record is authoritative';
    try { const results = await this.memory({ op: 'query', text: 'PRD planning board ' + path.basename(board) + ' ' + (args[0] ?? ''), k: 5 }); if (bytes(results) > this.outputCap) throw Error('memory response exceeds output cap'); return { status: 'available', authority, provider: 'memory', results }; }
    catch (error) { return { status: 'unavailable', authority, error: String(error) }; }
  }
  deliverMemory(file: string): Promise<any> {
    if (this.deliveries.has(file)) return this.deliveries.get(file)!;
    const work = (async () => {
      const entry = JSON.parse(fs.readFileSync(file, 'utf8'));
      if (entry.status !== 'committed' && entry.attempts < 3) {
        entry.attempts++; entry.status = 'pending'; atomic(file, JSON.stringify(entry));
        try { const ack = await this.memory({ op: 'ingest', text: entry.text, raw: true, sync: true }); if (ack?.status !== 'committed') throw Error('memory did not acknowledge committed status'); entry.status = 'committed'; delete entry.error; }
        catch (error) { entry.error = String(error).slice(0, 512); }
        atomic(file, JSON.stringify(entry));
      }
      const { text, session, ...receipt } = entry; return receipt;
    })().finally(() => this.deliveries.delete(file));
    this.deliveries.set(file, work); return work;
  }
  async rememberVerified(board: string, context: any, outcome: any) {
    const proof = (Array.isArray(outcome.verification) ? outcome.verification : [outcome.verification]).filter((p: any) => object(p) && p.verified === true);
    if (!proof.length) return { status: 'not_recorded', reason: 'no verified engine evidence' };
    const files: string[] = [];
    for (const item of proof) {
      const evidence = JSON.stringify(item, Object.keys(item).sort());
      if (Buffer.byteLength(evidence) > 8192) return { status: 'not_recorded', reason: 'verification evidence exceeds cap' };
      const text = 'Verified PRD collection on board ' + path.basename(board) + ': ' + evidence, identifier = hash(text), file = path.join(this.state, 'memory-outbox', identifier + '.json');
      if (!fs.existsSync(file)) atomic(file, JSON.stringify({ id: identifier, status: 'pending', attempts: 0, session: context.session, text })); files.push(file);
    }
    const receipts = []; for (const file of files.slice(0, 8)) receipts.push(await this.deliverMemory(file));
    return files.length === 1 ? receipts[0] : { status: receipts.length === files.length && receipts.every(r => r.status === 'committed') ? 'committed' : 'pending', queued: files.length, attempted: receipts.length, receipts };
  }
  async replayMemory() {
    const directory = path.join(this.state, 'memory-outbox'); if (!fs.existsSync(directory)) return;
    let attempts = 0;
    for (const name of fs.readdirSync(directory).filter(n => n.endsWith('.json')).sort()) {
      if (this.closed || attempts >= 16) break;
      try { const file = path.join(directory, name), entry = JSON.parse(fs.readFileSync(file, 'utf8')); if (entry.status !== 'committed' && entry.attempts < 3) { attempts++; await this.deliverMemory(file); } } catch {}
    }
  }
  async dispatch(request: any): Promise<any> {
    try {
      if (!object(request)) throw Error('expected a tool envelope');
      if (request.op === 'describe' && Object.keys(request).length === 1) return describe();
      if (!['call', 'cancel'].includes(request.op) || Object.keys(request).sort().join() !== (request.op === 'call' ? 'context,input,op' : 'context,op')) throw Error('expected describe, call or cancel envelope');
      const context = request.context, key = contextKey(context);
      if (!this.cancelled.has(key)) { if (this.cancelled.size >= 4096) throw Error('invocation capacity reached'); this.cancelled.set(key, new AbortController()); }
      const controller = this.cancelled.get(key)!;
      if (request.op === 'cancel') { controller.abort(); return this.result({ state: 'cancel_requested' }); }
      if (controller.signal.aborted || this.closed) return this.result({ state: 'cancelled' }, true);
      if (this.started.has(key)) throw Error('invocation already used; inspect status before retrying'); this.started.add(key);
      const { op, board, args } = this.prepare(request.input);
      if (op === 'status' || op === 'stop') return this.result(this.job(op, args[0], context));
      if (op === 'run') {
        if ([...this.jobs.values()].filter(j => j.state === 'running').length >= 4 || this.jobs.size >= 128) throw Error('PRD job capacity reached');
        const job = { job_id: id(), session: context.session, instance: this.instance, invocation: key, board: path.basename(board), state: 'running', started_at: Date.now() / 1000 };
        this.jobs.set(job.job_id, job); this.saveJob(job); this.publish(op, board, args, context, job);
        const work = (async () => { let outcome: any; try { outcome = await this.execute(op, board, args, controller, this.jobTimeout, context); outcome.memory = await this.rememberVerified(board, context, outcome); } catch (error) { outcome = { state: 'failed', error: String(error) }; } Object.assign(job, outcome, { finished_at: Date.now() / 1000 }); this.saveJob(job); this.publish(op, board, args, context, outcome); })();
        this.tasks.add(work); void work.finally(() => this.tasks.delete(work)); return this.result({ ...job });
      }
      const work = this.execute(op, board, args, controller, this.timeout, context); this.tasks.add(work);
      let outcome; try { outcome = await work; } finally { this.tasks.delete(work); }
      if (['plan', 'brief', 'read'].includes(op) && outcome.state === 'completed') outcome.memory = await this.recall(board, args);
      if (['add', 'refine', 'specced', 'claim', 'release', 'collect'].includes(op)) outcome.event = this.publish(op, board, args, context, outcome);
      if (op === 'collect' && outcome.state === 'completed') outcome.memory = await this.rememberVerified(board, context, outcome);
      return this.result(outcome, outcome.state !== 'completed');
    } catch (error) { return this.result({ error: error instanceof Error ? error.message : String(error) }, true); }
  }
  async declarations(request: any) {
    if (this.closed) return declarationFailure('unavailable');
    if (!object(request) || request.op !== 'source_declarations' || Object.keys(request).some(k => !['op', 'board', 'deadline_ms'].includes(k))) return declarationFailure('malformed');
    if (this.declarationReads.size >= 8) return declarationFailure('capacity');
    return sourceDeclarations(this.boards, request.board === undefined ? this.defaultBoard : request.board, request.deadline_ms === undefined ? 500 : request.deadline_ms, work => {
      this.declarationReads.add(work);
      void work.finally(() => this.declarationReads.delete(work));
    });
  }
  async records(request: any) {
    if (this.closed) return sourceRecordFailure('unavailable');
    if (!object(request) || request.op !== 'source_records' || Object.keys(request).some(k => !['op', 'board', 'action', 'expected_source_revision', 'path', 'expected_revision', 'deadline_ms'].includes(k))) return sourceRecordFailure('malformed');
    if (this.declarationReads.size >= 8) return sourceRecordFailure('capacity');
    const { op, board, deadline_ms, ...selection } = request;
    return sourceRecords(this.boards, board === undefined ? this.defaultBoard : board, selection as any, deadline_ms === undefined ? 500 : deadline_ms, work => {
      this.declarationReads.add(work); void work.finally(() => this.declarationReads.delete(work));
    });
  }
  async close() { this.closed = true; for (const controller of this.cancelled.values()) controller.abort(); await Promise.allSettled([...this.tasks, ...this.deliveries.values()]); }
}
export function main() {
  const wire = new Wire(), tasks = new Set<Promise<any>>();
  let service: Service | undefined;
  wire.on('apply', async config => {
    if (service) throw Error('cartridge is already applied');
    service = new Service(config ?? {}, wire); void service.replayMemory();
  });
  for (const key of ['prd', 'tool.prd', 'source.board']) wire.on(key, async args => {
    if (!service) throw Error('cartridge is not applied');
    // `source.board` is the memo-declared key for the owner of board search roots; it serves only the two source ops.
    const declarations = key === 'source.board' && args?.op !== 'source_records';
    const records = key === 'source.board' && args?.op === 'source_records';
    if (tasks.size >= 8 && !['cancel', 'describe'].includes(args?.op)) return declarations ? declarationFailure('capacity') : records ? sourceRecordFailure('capacity') : result({ error: 'service is busy' }, true);
    const work = declarations ? service.declarations(args) : records ? service.records(args) : service.dispatch(args);
    tasks.add(work); try { return await work; } finally { tasks.delete(work); }
  });
  wire.on('graph.announce', async () => { const tool = describe(); return { nodes: [{ kind: 'tool', key: 'tool.prd', name: tool.name, description: tool.description }], edges: [] }; });
  wire.onClose(() => { void service?.close(); });
}
if (import.meta.main) main();
