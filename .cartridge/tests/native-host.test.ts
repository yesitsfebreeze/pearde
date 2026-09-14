import { expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execute } from '../../src/engine';
import { lane, completionProblem } from '../../src/lifecycle';
import { atomic, git, scan } from '../../src/records';

const enabled = !!process.env.CARTRIDGE_TEST_BIN && !!process.env.MEMORY_TEST_BIN;
const runtime = path.resolve(import.meta.dir, '../../../cartridge.ctg');
const cartridge = path.resolve(process.env.CARTRIDGE_TEST_BIN || path.join(runtime, 'target/debug/cartridge'));
const memory = path.resolve(process.env.MEMORY_TEST_BIN || path.join(runtime, 'target/debug/memory_cartridge'));
const mcp = path.resolve(process.env.MCP_TEST_BIN || path.join(path.dirname(cartridge), 'mcp'));
const prd = path.resolve(import.meta.dir, '../..');

function initialize(directory: string) {
  fs.mkdirSync(directory, { recursive: true });
  git(directory, ['init', '-q']); git(directory, ['config', 'user.name', 'Native host fixture']); git(directory, ['config', 'user.email', 'fixture@example.invalid']);
  atomic(path.join(directory, 'seed.txt'), 'seed\n'); git(directory, ['add', '.']); git(directory, ['commit', '-qm', 'fixture baseline']);
}
function fixture(distinctEmbeddings = true) {
  const root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-native-memory-'));
  const records = path.join(root, 'records'), source = path.join(root, 'source'), board = path.join(records, '.cartridge/boards/root');
  initialize(records); initialize(source);
  atomic(path.join(records, '.gitignore'), '**/.state/\n**/.lanes/\n');
  atomic(path.join(board, 'settings.md'), `---\nname: fixture\nrepo: ${JSON.stringify(source)}\nrequire-repo: true\n---\n`);
  atomic(path.join(board, 'prds/example/prd.md'), `---\nstate: specced\nrepo: ${JSON.stringify(source)}\nfootprint: [seed.txt]\n---\n\n# Example\n\nVerify an isolated source change.\n`);
  atomic(path.join(board, 'prds/example/specs/spec01.md'), '---\nfootprint: [seed.txt]\n---\n\n# Verified change\n\n## Acceptance\n\n- [x] Source contains changed\n\n## Verify and Proof\n\n```sh\ntest "$(cat seed.txt)" = changed\n```\n');
  git(records, ['add', '.']); git(records, ['commit', '-qm', 'bounded planning fixture']);
  let requests = 0;
  const endpoint = Bun.serve({ hostname: '127.0.0.1', port: 0, async fetch(request) {
    requests++; const body = await request.json() as any;
    // Distinct documents need distinct vectors: constant embeddings cause the
    // real store to deduplicate the proof against the seed instead of committing it.
    const inputs = Array.isArray(body.input) ? body.input : [body.input];
    return Response.json({ embeddings: inputs.map((text: unknown) => distinctEmbeddings && String(text).includes('Verified PRD collection') ? [0, 1, 0] : [1, 0, 0]) });
  } });
  const config = `memory={dir=${JSON.stringify(path.join(root, 'store'))},embed={url=${JSON.stringify(endpoint.url.origin)},model="fixture"},reason={url=""},tick={interval_secs=0},queue={enabled=false}}`;
  return { root, records, source, board, config, requests: () => requests, dispose() { endpoint.stop(true); fs.rmSync(root, { recursive: true, force: true }); } };
}
function binaryPlugin(plugins: string, name: string, binary: string) {
  atomic(path.join(plugins, name, 'cartridge.json'), JSON.stringify({ name, entry: 'init.lua' }));
  atomic(path.join(plugins, name, 'init.lua'), `return cartridge.process(${JSON.stringify(binary)})`);
}
async function run(args: string[], cwd: string, input = '') {
  const child = Bun.spawn(args, { cwd, env: { ...process.env, HOME: cwd, XDG_CONFIG_HOME: path.join(cwd, 'config'), XDG_DATA_HOME: path.join(cwd, 'data'), XDG_CACHE_HOME: path.join(cwd, 'cache') }, stdin: new Blob([input]), stdout: 'pipe', stderr: 'pipe', timeout: 60000 });
  try {
    const [output, error, code] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited]);
    expect(code, error + '\n' + output).toBe(0); expect(error).not.toContain('panic'); return output;
  } finally { if (child.exitCode === null) { child.kill(); await child.exited; } }
}

for (const distinct of [true, false]) test.skipIf(!enabled)(distinct
  ? 'actual runtime and memory recall context and commit verified collection evidence'
  : 'actual memory deduplication is never mistaken for committed collection ingestion', async () => {
  const f = fixture(distinct), expected = distinct ? 'committed' : 'pending';
  try {
    const claimed = await execute('claim', f.board, ['example', 'fixture-worker']); expect(claimed.error).toBe('');
    atomic(path.join(lane(scan(f.board).get('example')!).directory, 'seed.txt'), 'changed\n');
    // One user profile: the host reads the `.cartridge` beside its working
    // directory, which is `f.root` for the run below.
    const profile = path.join(f.root, '.cartridge'), plugins = path.join(f.root, 'plugins'); fs.mkdirSync(plugins);
    atomic(path.join(profile, 'init.lua'), 'return {{id="memory",path="memory"},{id="prd",path="prd"},{id="probe",path="probe"}}');
    atomic(path.join(profile, 'config.lua'), `return {${f.config},prd={root=${JSON.stringify(f.records)},timeout_seconds=30}}`);
    binaryPlugin(plugins, 'memory', memory); fs.symlinkSync(prd, path.join(plugins, 'prd'));
    const launch = path.join(f.root, 'native-host-probe');
    atomic(launch, `#!/bin/sh\nexec ${JSON.stringify(process.execPath)} ${JSON.stringify(path.join(import.meta.dir, 'fixtures/native-host-probe.ts'))} "$@"\n`); fs.chmodSync(launch, 0o755);
    binaryPlugin(plugins, 'probe', launch);
    const data = JSON.parse(await run([cartridge, '--dir', plugins, 'run', 'native-host-probe', JSON.stringify({ cwd: f.records })], f.root));
    expect(data.seed.status).toBe('committed'); expect(data.read.error).toBe(false);
    const read = JSON.parse(data.read.content); expect(read.memory.status).toBe('available'); expect(JSON.stringify(read.memory.results)).toContain('Cedar');
    expect(data.collected.error, String(data.collected.content)).toBe(false);
    const collected = JSON.parse(data.collected.content);
    expect(collected.verification[0].verified).toBe(true); expect(collected.memory.status, JSON.stringify(collected.memory)).toBe(expected);
    const outbox = path.join(f.records, '.cartridge/.state/prd-service/memory-outbox');
    const receipts = fs.readdirSync(outbox).map(name => JSON.parse(fs.readFileSync(path.join(outbox, name), 'utf8')));
    expect(receipts).toHaveLength(1); expect(receipts[0].status).toBe(expected); expect(receipts[0].attempts).toBe(1);
    if (distinct) expect(JSON.stringify(data.recalled)).toContain('Verified PRD collection');
    else expect(receipts[0].error).toContain('did not acknowledge committed status');
    expect(data.events.some((event: any) => event.kind === 'data' && event.ch === 'prd' && event.data.operation === 'collect'), JSON.stringify(data.events)).toBe(true);
    expect(completionProblem(scan(f.board).get('example')!)).toBeNull(); expect(fs.readFileSync(path.join(f.source, 'seed.txt'), 'utf8')).toBe('changed\n');
    expect(f.requests()).toBeGreaterThan(0);
  } finally { f.dispose(); }
}, 90000);

test.skipIf(!enabled || !fs.existsSync(mcp))('shipped MCP profile discovers PRD and routes real read, plan and mutation', async () => {
  const f = fixture();
  try {
    const profile = path.join(f.root, '.cartridge'), plugins = path.join(f.root, 'plugins'); fs.mkdirSync(plugins);
    // There is one shipped profile now; the MCP server is an entry point into
    // it, not a composition of its own.
    const init = fs.readFileSync(path.join(runtime, '.cartridge/init.lua'), 'utf8');
    expect(init).toMatch(/id\s*=\s*"prd"/);
    atomic(path.join(profile, 'init.lua'), init);
    // Shallowest first: a cartridge nested inside another (`live/mcp`) arrives
    // through its parent's link and must not be linked over it.
    const names = [...new Set([...init.matchAll(/path\s*=\s*"([^"\n]+)"/g)].map(match => match[1]))]
      .sort((left, right) => left.split('/').length - right.split('/').length);
    for (const name of names) {
      if (fs.existsSync(path.join(plugins, name))) continue;
      if (name === 'memory' || name === 'mcp') binaryPlugin(plugins, name, name === 'memory' ? memory : mcp);
      else {
        fs.mkdirSync(path.dirname(path.join(plugins, name)), { recursive: true });
        fs.symlinkSync(name === 'prd' ? prd : fs.realpathSync(path.join(runtime, 'builtin', name)), path.join(plugins, name));
      }
    }
    atomic(path.join(profile, 'config.lua'), `local config=dofile(${JSON.stringify(path.join(runtime, '.cartridge/config.lua'))})\nlocal isolated={${f.config}}\nconfig.memory=isolated.memory\nconfig.prd={root=${JSON.stringify(f.records)},timeout_seconds=30}\nconfig.mcp.cwd=${JSON.stringify(f.records)}\nconfig.sessions={dir=${JSON.stringify(path.join(f.root, 'sessions'))}}\nreturn config\n`);
    const messages = [
      { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'prd-native-host-fixture', version: '1' } } },
      { jsonrpc: '2.0', method: 'notifications/initialized' },
      { jsonrpc: '2.0', id: 2, method: 'tools/list', params: {} },
      ...[['read', ['example']], ['plan', []], ['add', ['MCP native integration fixture']]].map(([op, args], index) => ({ jsonrpc: '2.0', id: index + 3, method: 'tools/call', params: { name: 'prd', arguments: { op, args } } })),
    ];
    const output = await run([cartridge, '--dir', plugins, 'mcp'], f.root, messages.map(message => JSON.stringify(message) + '\n').join(''));
    const replies = output.trim().split('\n').map(line => JSON.parse(line));
    expect(replies.find(reply => reply.id === 2).result.tools.some((tool: any) => tool.name === 'prd')).toBe(true);
    for (const id of [3, 4, 5]) { const reply = replies.find(reply => reply.id === id); expect(reply.error, JSON.stringify(reply)).toBeUndefined(); expect(reply.result.isError, JSON.stringify(reply)).not.toBe(true); }
    const result = (id: number) => JSON.parse(replies.find(reply => reply.id === id).result.content[0].text);
    expect(result(3).state).toBe('completed'); expect(result(3).data.text).toContain('Verify an isolated source change');
    expect(result(4).state).toBe('completed'); expect(result(4).data.rows.some((row: any) => row.rel === 'example')).toBe(true);
    expect(result(5).state).toBe('completed'); expect(result(5).changed).toHaveLength(1);
    expect(fs.existsSync(path.join(f.board, 'prds/mcp-native-integration-fixture/prd.md'))).toBe(true);
  } finally { f.dispose(); }
}, 90000);
