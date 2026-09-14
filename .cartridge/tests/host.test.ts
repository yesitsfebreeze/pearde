import { expect, test } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { atomic, git } from '../../src/records';
test.skipIf(!process.env.CARTRIDGE_TEST_BIN)('real runtime supplies memory and routes PRD events', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'prd-native-host-'));
  try {
    git(root, ['init', '-q']); const board = path.join(root, '.cartridge/boards/root');
    atomic(path.join(board, 'settings.md'), `---\nname: fixture\nrepo: ${JSON.stringify(root)}\nrequire-repo: true\n---\n`);
    atomic(path.join(board, 'prds/example/prd.md'), '---\nstate: open\n---\n\n# Example\n');
    const profile = path.join(root, '.cartridge'), plugins = path.join(root, 'plugins'); fs.mkdirSync(plugins);
    atomic(path.join(profile, 'init.lua'), 'return {{id="memory",path="memory.lua"},{id="prd",path="prd"},{id="probe",path="probe.lua"}}');
    atomic(path.join(profile, 'config.lua'), `return {prd={root=${JSON.stringify(root)},timeout_seconds=30}}`);
    atomic(path.join(plugins, 'memory.lua'), `return {provide={"memory"},apply=function(ctx)
      local calls={} ctx:provide("memory",function(request)
        if request.op=="fixture_calls" then return calls end table.insert(calls,request)
        if request.op=="query" then return {items={{id="evidence",text="Planning evidence"}}} end
        if request.op=="ingest" then return {status="committed"} end error("unexpected memory operation")
      end) end}`);
    atomic(path.join(plugins, 'probe.lua'), `return {needs={"prd","memory"}, provide={"probe"}, apply=function(ctx)
      local events={} ctx:subscribe("prd","prd",function(envelope) table.insert(events,envelope) end)
      ctx:provide("probe",function(args)
        local function call(op,list,id) return ctx.prd({op="call",context={session="test",run="one",call=id,cwd=args.cwd},input={op=op,args=list}}) end
        local read=call("read",{"example"},"read") local added=call("add",{"Native runtime event probe"},"add")
        return {read=read,added=added,memory_calls=ctx.memory({op="fixture_calls"}),events=events}
      end) end}`);
    fs.symlinkSync(path.resolve(import.meta.dir, '../..'), path.join(plugins, 'prd'));
    const child = Bun.spawn([path.resolve(process.env.CARTRIDGE_TEST_BIN!), '--dir', plugins, 'run', 'probe', JSON.stringify({ cwd: root })], { cwd: root, stdout: 'pipe', stderr: 'pipe', timeout: 45000 });
    const [output, error, code] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited]);
    expect(error).not.toContain('panic'); expect(code, error).toBe(0); const data = JSON.parse(output);
    expect(data.read.error).toBe(false); expect(JSON.parse(data.read.content).memory.status).toBe('available'); expect(data.added.error).toBe(false);
    expect(data.memory_calls.some((c: any) => c.op === 'query')).toBe(true);
    expect(data.events.some((e: any) => e.kind === 'data' && e.channel === 'prd' && e.data.operation === 'add'), JSON.stringify(data.events)).toBe(true);
    expect(fs.existsSync(path.join(board, 'prds/native-runtime-event-probe/prd.md'))).toBe(true);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}, 60000);
