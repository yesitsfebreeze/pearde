import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';
import { execute } from './engine';
import { canonicalBoard } from './records';

export const ROOT = path.resolve(import.meta.dir, '..');
export async function main(argv = process.argv.slice(2)) {
  if (!argv.length || ['help', '--help', '-h'].includes(argv[0])) {
    console.log('prd — planning, specifications, Gantt and checked execution\n\nscan | plan | gantt | read <id> | brief <id> | next\nadd | refine | specced | claim | release | collect | defer | retry | unblock\ncollect <id> --committed  (verify committed artifact; report dirty workspace separately)\ncollect <done-id> --reverify  (rerun unchanged contract; preserve previous receipt)\nadopt <id> --by <identity> --reason <text>  (accept state/claim/commit changed outside the engine; recorded)\nrun --dry | run --adapter <configured-agent> [--workers 3]\ncheck | status | members | boards\n\nUse --board <registered-name-or-path> (default root), --json for the API envelope.'); return 0;
  }
  const [operation, ...rest] = argv, args: string[] = [];
  let selected: string | undefined, json = false;
  for (let i = 0; i < rest.length; i++) {
    if (rest[i] === '--json') { json = true; continue; }
    if (rest[i] === '--board' || rest[i].startsWith('--board=')) {
      if (selected !== undefined) throw Error('specify --board only once');
      selected = rest[i].includes('=') ? rest[i].slice(8) : rest[++i];
      if (!selected) throw Error('--board requires a value');
    } else args.push(rest[i]);
  }
  const boards = path.join(ROOT, '.cartridge/boards');
  if (operation === 'boards') { console.log(JSON.stringify(Object.fromEntries(fs.readdirSync(boards).filter(name => fs.existsSync(path.join(boards, name, 'settings.md'))).map(name => [name, path.join(boards, name)])), null, 2)); return 0; }
  const board = canonicalBoard(selected ? fs.existsSync(path.join(boards, selected, 'settings.md')) ? path.join(boards, selected) : selected : path.join(boards, 'root'));
  const controller = new AbortController();
  const stop = () => controller.abort(); process.on('SIGTERM', stop); process.on('SIGINT', stop);
  try {
    let eventErrors = 0;
    let eventError = '';
    let socket: net.Socket | undefined;
    const failed = (error: unknown) => { eventErrors++; eventError = String(error).slice(0, 256); };
    if (process.env.PRD_NATIVE_EVENT_SOCKET) {
      socket = net.createConnection(process.env.PRD_NATIVE_EVENT_SOCKET);
      socket.on('error', failed);
      try { await new Promise<void>((resolve, reject) => { socket!.once('connect', resolve); socket!.once('error', reject); }); } catch {}
    }
    const emit = socket ? (event: any) => {
      const packet = JSON.stringify(event) + '\n';
      if (socket!.destroyed || socket!.writableLength + Buffer.byteLength(packet) > 65536) { failed('native event channel unavailable or backpressured'); return; }
      socket!.write(packet);
    } : undefined;
    const result = await execute(operation, board, args, controller.signal, emit);
    if (socket && !socket.destroyed) await new Promise<void>(resolve => {
      const timer = setTimeout(() => { failed('native event flush timed out'); socket!.destroy(); resolve(); }, 1000);
      const done = () => { clearTimeout(timer); resolve(); };
      socket!.once('error', done); socket!.end(done);
    });
    if (eventErrors) { result.event_errors = eventErrors; result.event_error = eventError; }
    if (json) console.log(JSON.stringify(result));
    else { if (result.data) console.log(operation === 'read' ? result.data.text : JSON.stringify(result.data, null, 2)); if (result.output) process.stdout.write(result.output); if (result.error) console.error(result.error); }
    return result.exit_code;
  } finally { process.off('SIGTERM', stop); process.off('SIGINT', stop); }
}
if (import.meta.main) { try { process.exitCode = await main(); } catch (error) { console.error('prd: ' + (error instanceof Error ? error.message : error)); process.exitCode = 2; } }
