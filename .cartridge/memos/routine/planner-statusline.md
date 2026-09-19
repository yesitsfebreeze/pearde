---
kind: routine
description: Render a bounded, read-only native planner status line for the current source owner
---

# Planner status line

Run this memo with `cartridge-task --file <memo> <recipe>`. Read Claude-style JSON from
stdin or `PRD_STATUS_JSON`; `MEMO_OWNER_ROOT` locates the central planner records.
The first line always shows the directory, available Git state and model.
The second selects the most specific mapped source owner; the composition and
planner roots select the root board. Counts describe records, including parents,
and **recorded done is not verified integration**. Complexity uses the native
planner's weighting; derived open counts are a subset of the live backlog.

The transcript tail is capped at 1 MiB, input at 64 KiB, and Git at one second.
Missing or malformed optional data is omitted. Existing vaults get an Obsidian
path link; `PRD_STATUS_LINK=off` prints its label without terminal escapes.
No legacy daemon, network, personal configuration, or generated files are used.

```task
status:
    #!/usr/bin/env bun
    import fs from 'node:fs';
    import path from 'node:path';
    const clean = (value, cap = 160) => String(value ?? '').replace(/\x1b\][\s\S]*?(?:\x07|\x1b\\)/g, '').replace(/\x1b\[[0-?]*[ -/]*[@-~]/g, '').replace(/[\x00-\x1f\x7f-\x9f\p{Cf}]/gu, ' ').trim().slice(0, cap);
    let input = process.env.PRD_STATUS_JSON ?? '', data = {};
    try {
      if (!input && !process.stdin.isTTY) {
        const chunks = []; let size = 0;
        for await (const chunk of Bun.stdin.stream()) { size += chunk.length; if (size > 65536) throw Error('input cap'); chunks.push(chunk); }
        input = Buffer.concat(chunks).toString('utf8');
      }
      if (Buffer.byteLength(input) <= 65536) { const parsed = JSON.parse(input || '{}'); if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) data = parsed; }
    } catch {}
    const owner = process.env.MEMO_OWNER_ROOT;
    const requested = data.current_dir ?? data.cwd ?? data.workspace?.current_dir;
    let cwd = typeof requested === 'string' && requested ? path.resolve(requested) : process.cwd();
    try { cwd = fs.realpathSync(cwd); } catch {}
    let model = data.model?.display_name ?? data.display_name ?? data.model?.id ?? '', persona = '';
    try {
      if (typeof data.transcript_path === 'string') {
        const stat = fs.statSync(data.transcript_path);
        if (stat.isFile()) {
          const start = Math.max(0, stat.size - 1048576), bytes = Buffer.alloc(Math.min(stat.size, 1048576));
          const fd = fs.openSync(data.transcript_path, 'r');
          try { fs.readSync(fd, bytes, 0, bytes.length, start); } finally { fs.closeSync(fd); }
          const lines = bytes.toString('utf8').split('\n'); if (start) lines.shift();
          for (const line of lines) try {
            const row = JSON.parse(line), message = row.message ?? row;
            if ((row.type === 'assistant' || message.role === 'assistant') && typeof message.model === 'string' && message.model !== '<synthetic>') model = message.model;
            const content = typeof message.content === 'string' ? message.content : Array.isArray(message.content) ? message.content.map(part => part.text ?? '').join(' ') : '';
            for (const match of content.matchAll(/▸[^\n]*?· as ([a-z][a-z0-9-]{1,15})(?![a-z0-9-])/g)) persona = match[1];
          } catch {}
        }
      }
    } catch {}
    const home = process.env.HOME;
    const short = home && (cwd === home || cwd.startsWith(home + path.sep)) ? '~' + cwd.slice(home.length) : cwd;
    const first = [clean(short, 240) || '.'];
    try {
      const result = Bun.spawnSync(['git', '--no-optional-locks', '-C', cwd, 'status', '--porcelain=v2', '--branch', '--untracked-files=normal'], { stdout: 'pipe', stderr: 'ignore', timeout: 1000, maxBuffer: 1048576 });
      if (!result.exitCode) {
        const lines = result.stdout.toString().trim().split('\n');
        const branch = lines.find(line => line.startsWith('# branch.head '))?.slice(14);
        if (branch) first.push(clean(branch));
        const dirty = lines.filter(line => line && !line.startsWith('#')).length; if (dirty) first.push('*' + dirty);
        const ab = /^# branch.ab \+(\d+) -(\d+)$/m.exec(lines.join('\n'));
        if (ab) { if (+ab[1]) first.push('↑' + ab[1]); if (+ab[2]) first.push('↓' + ab[2]); }
        else if (!lines.some(line => line.startsWith('# branch.upstream '))) first.push('no-upstream');
      }
    } catch {}
    if (clean(model, 80)) first.push('·', clean(model, 80));
    console.log(first.join(' '));
    try {
      const { document, scan, real, inside } = await import(path.join(owner, 'src/records.ts'));
      const { liveStates, weight } = await import(path.join(owner, 'src/planner.ts'));
      const boards = path.join(owner, '.cartridge/boards'), root = path.join(boards, 'root');
      const candidates = [];
      for (const entry of fs.readdirSync(boards, { withFileTypes: true })) {
        if (!entry.isDirectory()) continue;
        const board = path.join(boards, entry.name);
        try {
          const settings = document(path.join(board, 'settings.md')).fm, mapped = settings.repo ?? settings['source-repository'];
          if (typeof mapped !== 'string') continue;
          const repo = real(path.resolve(board, mapped));
          if (inside(repo, cwd)) candidates.push({ board, repo });
        } catch {}
      }
      candidates.sort((a, b) => b.repo.length - a.repo.length);
      const board = inside(real(owner), cwd) ? root : candidates.length && !(candidates[1]?.repo === candidates[0].repo) ? candidates[0].board : null;
      if (board) {
        const records = [...scan(board).values()], done = records.filter(record => record.state === 'done'), open = records.filter(record => liveStates.has(record.state));
        const totalWeight = records.reduce((sum, record) => sum + weight(record), 0), doneWeight = done.reduce((sum, record) => sum + weight(record), 0);
        const parts = ['prd ' + clean(path.basename(board)), 'recorded ' + done.length + '/' + records.length + ' done', 'weighted ' + (totalWeight ? Math.round(doneWeight / totalWeight * 100) : 0) + '%', 'open ' + open.length];
        const derived = open.filter(record => record.fm.origin === 'derived').length; if (derived) parts.push('derived open ' + derived);
        if (persona) parts.push(persona);
        const vault = [cwd, candidates[0]?.repo, owner, path.dirname(board), board].find(directory => directory && fs.existsSync(path.join(directory, '.obsidian')));
        if (vault) parts.push(process.env.PRD_STATUS_LINK === 'off' ? '▸vault' : '\x1b]8;;obsidian://open?path=' + encodeURIComponent(vault) + '\x1b\\▸vault\x1b]8;;\x1b\\');
        console.log(parts.join(' · '));
      }
    } catch {}
```

Legacy colors, daemon board links, Kern status, and OS-specific Obsidian registry
lookups are intentionally omitted. The native record line remains useful offline.
