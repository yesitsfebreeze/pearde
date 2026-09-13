import { afterEach, beforeEach, expect, test, spyOn } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { atomic, hash, members, scan, sourceDeclarations } from '../../src/records';
import { Service } from '../../src/service';

let root: string, boards: string;
function settings(name: string, members: unknown = {}) {
  const directory = path.join(boards, name);
  atomic(path.join(directory, 'settings.md'), `---\nname: fixture\nmembers: ${JSON.stringify(members)}\n---\n`);
  atomic(path.join(directory, 'prds/same/prd.md'), '# Same\n');
  return directory;
}
function snapshot(directory = root): string {
  return hash(JSON.stringify(fs.readdirSync(directory, { recursive: true, withFileTypes: true }).map(e => {
    const file = path.join(e.parentPath, e.name), stat = fs.lstatSync(file);
    return [path.relative(directory, file), stat.mode, e.isFile() ? hash(fs.readFileSync(file)) : e.isSymbolicLink() ? fs.readlinkSync(file) : 'directory'];
  }).sort((a, b) => String(a[0]).localeCompare(String(b[0])))));
}
beforeEach(() => {
  root = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'prd-declarations-'));
  boards = path.join(root, '.cartridge/boards');
  settings('root', { base: 'base' }); settings('root/base', [{ plugin: 'plugin' }]); settings('root/base/plugin');
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

test('real grammar retains hierarchical scanner identities and exports exact immutable declaration bytes', async () => {
  const before = snapshot(), refs = [...scan(path.join(boards, 'root')).keys()];
  expect(refs).toEqual(['same', '@base/same', '@base/plugin/same']);
  for (const board of ['root', 'root/base', 'root/base/plugin']) {
    const result = await sourceDeclarations(boards, board);
    expect(result.status).toBe('available');
    if (result.status !== 'available') throw Error('missing declarations');
    expect(result.children.map(e => [e.name, e.root])).toEqual(members(path.join(boards, board)));
    expect(result.revision).toBe(hash(fs.readFileSync(path.join(boards, board, 'settings.md'))));
  }
  const file = path.join(boards, 'root/settings.md');
  const old = await sourceDeclarations(boards, 'root');
  expect(snapshot()).toBe(before);
  atomic(file, '\uFEFF---\r\nmembers: {base: base}\r\n---\r\n# Root\r\n');
  const next = await sourceDeclarations(boards, 'root');
  expect(next.status).toBe('available');
  if (next.status !== 'available' || old.status !== 'available') throw Error('missing revision');
  expect(next.revision).toBe(hash(fs.readFileSync(file))); expect(next.revision).not.toBe(old.revision);
  expect([...scan(path.join(boards, 'root')).keys()]).toEqual(refs);
});

test('missing descendants, backlinks and repeated mounts remain declarations without weakening strict scan', async () => {
  settings('root', [{ z: 'base' }, { a: 'base' }, { missing: 'gone' }]);
  const answer = await sourceDeclarations(boards, 'root');
  expect(answer.status).toBe('available');
  if (answer.status !== 'available') throw Error('missing edges');
  expect(answer.children.map(e => e.name)).toEqual(['a', 'missing', 'z']);
  expect(() => scan(path.join(boards, 'root'))).toThrow('no planning board');
  settings('root', { base: 'base' }); settings('root/base', { backlink: '..' });
  expect((await sourceDeclarations(boards, 'root/base')).status).toBe('available');
  expect(() => scan(path.join(boards, 'root'))).toThrow('cycle');
  fs.rmSync(path.join(boards, 'root/base'), { recursive: true });
  expect((await sourceDeclarations(boards, 'root')).status).toBe('available');
  expect((await sourceDeclarations(boards, 'root/base')).status).toBe('unavailable');
});

test('selectors, exact configured authority and settings inode rules reject escapes and nonregular files', async () => {
  for (const board of ['', '.', '..', '/tmp', 'root/', 'root//base', 'root/../root', 'root\\base', 'root\0', 'x'.repeat(513), Array(33).fill('a').join('/')])
    expect((await sourceDeclarations(boards, board)).status).toBe('malformed');
  fs.mkdirSync(path.join(root, 'outside')); fs.symlinkSync(path.join(root, 'outside'), path.join(boards, 'escape'));
  expect((await sourceDeclarations(boards, 'escape')).status).toBe('malformed');
  for (const location of ['../../outside', '../escape/missing']) {
    settings('root', { escape: location }); expect((await sourceDeclarations(boards, 'root')).status).toBe('malformed');
  }
  settings('root', { child: 'base' });
  const file = path.join(boards, 'root/settings.md'); fs.unlinkSync(file); fs.symlinkSync(path.join(boards, 'root/base/settings.md'), file);
  expect((await sourceDeclarations(boards, 'root')).status).toBe('malformed');
  fs.unlinkSync(file); fs.mkdirSync(file); expect((await sourceDeclarations(boards, 'root')).status).toBe('malformed');
});

test('malformed grammar and bounded declarations fail explicitly, with no child scan', async () => {
  for (const raw of [[{ a: 'base' }, { a: 'base' }], { invalid: 42 }, { '/bad': 'base' }]) {
    settings('root', raw); expect((await sourceDeclarations(boards, 'root')).status).toBe('malformed');
    expect(() => members(path.join(boards, 'root'))).toThrow('invalid or duplicate');
  }
  settings('root', Object.fromEntries(Array.from({ length: 65 }, (_, i) => ['a' + i, 'missing' + i])));
  expect((await sourceDeclarations(boards, 'root')).status).toBe('capacity');
  for (const raw of [{ ['a'.repeat(65)]: 'base' }, { a: 'a'.repeat(4097) }]) {
    settings('root', raw); expect((await sourceDeclarations(boards, 'root')).status).toBe('capacity');
  }
  const file = path.join(boards, 'root/settings.md');
  atomic(file, 'x'.repeat(65537)); expect((await sourceDeclarations(boards, 'root')).status).toBe('capacity');
  atomic(file, '---\nmembers: [broken\n---\n'); expect((await sourceDeclarations(boards, 'root')).status).toBe('malformed');
  fs.writeFileSync(file, Buffer.from([0xff])); expect((await sourceDeclarations(boards, 'root')).status).toBe('malformed');
});

test('deadline covers filesystem work and static failures do not expose paths', async () => {
  for (const deadline of [0, 2001, 1.5, NaN]) expect((await sourceDeclarations(boards, 'root', deadline)).status).toBe('malformed');
  const realpath = fs.promises.realpath.bind(fs.promises);
  let finish!: () => void;
  const paused = new Promise<void>(resolve => { finish = resolve; });
  const delayed = spyOn(fs.promises, 'realpath').mockImplementation((async (file: fs.PathLike) => {
    await paused; return realpath(file);
  }) as typeof fs.promises.realpath);
  try {
    const answer = await sourceDeclarations(boards, 'root', 5);
    expect(answer).toEqual({ schema: 'cartridge-source-declarations/v1', status: 'timeout' });
  } finally { finish(); await Bun.sleep(10); delayed.mockRestore(); }
});

test('YAML alias member lists stop at the edge cap before expanding repeated maps', async () => {
  const entries = Object.fromEntries(Array.from({ length: 100 }, (_, i) => ['edge' + i, 'missing' + i]));
  const file = path.join(boards, 'root/settings.md');
  atomic(file, '---\ntemplate: &edges ' + JSON.stringify(entries) + '\nmembers:\n' + '  - *edges\n'.repeat(1000) + '---\n');
  expect(fs.statSync(file).size).toBeLessThan(65536);
  const keys = Object.keys; let expanded = 0;
  const observed = spyOn(Object, 'keys').mockImplementation(value => {
    if ((value as any).edge99 === 'missing99') expanded++;
    return keys(value);
  });
  try {
    expect((await sourceDeclarations(boards, 'root')).status).toBe('capacity');
    expect(expanded).toBe(1);
  } finally { observed.mockRestore(); }
});

test('service native method bypasses tool execution, callbacks, journals and spills', async () => {
  let callbacks = 0;
  const service = new Service({ root, max_output_bytes: 1024 }, { request: async () => { callbacks++; throw Error('forbidden'); }, publish: () => { callbacks++; } });
  try {
    const before = snapshot();
    expect((await service.declarations({ op: 'source_declarations', board: 'root' })).status).toBe('available');
    for (const extra of [{ root }, { config: {} }, { cwd: root }, { args: [] }, { deadline_ms: null }])
      expect((await service.declarations({ op: 'source_declarations', board: 'root', ...extra })).status).toBe('malformed');
    expect((await service.dispatch({ op: 'describe' })).input_schema.properties.op.enum).not.toContain('source_declarations');
    expect((await service.dispatch({ op: 'source_declarations', board: 'root' })).error).toBe(true);
    expect(callbacks).toBe(0); expect(snapshot()).toBe(before); expect(service.started.size).toBe(0); expect(service.tasks.size).toBe(0);
  } finally { await service.close(); }
});

test('a FIFO swapped in after metadata inspection cannot strand the settings open', async () => {
  const open = fs.promises.open.bind(fs.promises);
  const file = path.join(boards, 'root/settings.md');
  let actualWork: Promise<unknown> | undefined;
  const replacement = spyOn(fs.promises, 'open').mockImplementation(async (name, flags, mode) => {
    if (name === file) {
      fs.unlinkSync(file);
      expect(Bun.spawnSync(['mkfifo', file]).exitCode).toBe(0);
    }
    return open(name, flags, mode);
  });
  try {
    expect((await sourceDeclarations(boards, 'root', 500, work => { actualWork = work; })).status).toBe('unavailable');
    await Promise.race([actualWork, Bun.sleep(500).then(() => { throw Error('settings open remained pending'); })]);
  } finally { replacement.mockRestore(); }
});

test('timed out native reads retain their capacity slots until actual IO settles', async () => {
  const service = new Service({ root }), realpath = fs.promises.realpath.bind(fs.promises);
  let finish!: () => void;
  const paused = new Promise<void>(resolve => { finish = resolve; });
  const delayed = spyOn(fs.promises, 'realpath').mockImplementation((async (file: fs.PathLike) => {
    await paused; return realpath(file);
  }) as typeof fs.promises.realpath);
  try {
    const replies = await Promise.all(Array.from({ length: 8 }, () => service.declarations({ op: 'source_declarations', deadline_ms: 5 })));
    expect(replies.every(reply => reply.status === 'timeout')).toBe(true);
    expect(service.declarationReads.size).toBe(8);
    expect((await service.declarations({ op: 'source_declarations' })).status).toBe('capacity');
    finish(); await Promise.all(service.declarationReads);
    expect(service.declarationReads.size).toBe(0);
  } finally { finish(); delayed.mockRestore(); await service.close(); }
});

test.skipIf(!process.env.CARTRIDGE_TEST_BIN)('actual Host invokes native declarations without Memory or event effects and tool exposure', async () => {
  const profile = path.join(root, 'profile'), plugins = path.join(root, 'plugins'); fs.mkdirSync(plugins);
  atomic(path.join(profile, 'init.lua'), 'return {{id="memory",path="memory.lua"},{id="prd",path="prd"},{id="probe",path="probe.lua"}}');
  atomic(path.join(profile, 'config.lua'), `return {prd={root=${JSON.stringify(root)},max_output_bytes=1024}}`);
  atomic(path.join(plugins, 'memory.lua'), `return {provide={"memory"},apply=function(ctx) ctx:provide("memory",function(request) error("declaration operation called Memory") end) end}`);
  fs.symlinkSync(path.resolve(import.meta.dir, '../..'), path.join(plugins, 'prd'));
  const probe = path.join(root, 'probe.ts');
  atomic(probe, `import {createInterface} from 'node:readline';
import {HostBridge} from ${JSON.stringify(path.resolve(import.meta.dir, '../../src/service.ts'))};
if(process.argv[2]==='hello'){console.log(JSON.stringify({inject:['prd','tool.prd'],provide:['probe']}));process.exit(0);}
const send=m=>console.log(JSON.stringify(m)),bridge=new HostBridge(send),events=[];
for await(const line of createInterface({input:process.stdin})){
 const m=JSON.parse(line);if(bridge.accept(m))continue;if(m.dispose)break;
 if(m.apply){send({provide:'probe'});send({subscribe:'prd'});send({ready:true});}
 else if(m.call==='probe')void(async()=>{try{
  const rows=[];for(const board of ['root','root/base','root/base/plugin'])rows.push(await bridge.request('prd',{op:'source_declarations',board}));
  const rejected=await bridge.request('tool.prd',{op:'source_declarations',board:'root'});
  const described=await bridge.request('tool.prd',{op:'describe'});
  send({reply:m.id,data:{rows,rejected,described,events}});
 }catch(e){send({reply:m.id,error:String(e)});}})();
 else events.push(m);
}bridge.close();`);
  const launch = path.join(root, 'probe'); atomic(launch, `#!/bin/sh\nexec '${process.execPath.replaceAll("'", "'\\''")}' '${probe.replaceAll("'", "'\\''")}' "$@"\n`); fs.chmodSync(launch, 0o755);
  atomic(path.join(plugins, 'probe.lua'), `return cartridge.process(${JSON.stringify(launch)})`);
  const before = snapshot(boards);
  const child = Bun.spawn([path.resolve(process.env.CARTRIDGE_TEST_BIN!), '--dir', plugins, '--profile', profile, 'run', 'probe', '{}'], { cwd: root, stdout: 'pipe', stderr: 'pipe', timeout: 15000 });
  try {
    const [output, error, code] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited]);
    expect(code, error + '\n' + output).toBe(0);
    const data = JSON.parse(output); expect(data.rows.map((r: any) => r.status)).toEqual(['available', 'available', 'available']);
    expect(data.rows[0].children[0].root).toBe(path.join(boards, 'root/base'));
    expect(data.rejected.error).toBe(true); expect(data.described.input_schema.properties.op.enum).not.toContain('source_declarations');
    expect(data.events.filter((e: any) => e.event?.kind !== 'subscribe')).toEqual([]);
    expect(snapshot(boards)).toBe(before); expect(fs.existsSync(path.join(root, '.cartridge/.state'))).toBe(false);
  } finally { if (child.exitCode === null) { child.kill(); await child.exited; } }
}, 20000);
