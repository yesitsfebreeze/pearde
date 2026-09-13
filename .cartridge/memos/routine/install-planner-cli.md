---
kind: routine
description: Install the native planner CLI and migrate its existing local statusline consumer
---

# Install the planner CLI

This explicit recipe installs `prd` and the legacy `pearde` command name as thin
launchers for the same native engine. It migrates the existing PeaRDe Claude
statusline to the maintained statusline memo. Other settings and local repositories
are preserved. Superseded wrappers are saved in the user's local state directory.

```just
install:
    #!/usr/bin/env bun
    import fs from 'node:fs';
    import path from 'node:path';
    import os from 'node:os';
    const owner=process.env.MEMO_OWNER_ROOT, home=os.homedir();
    const runner=path.join(owner,'../cartridge.ctg/.cartridge/tools/memo-run');
    const memo=path.join(owner,'.cartridge/memos/routine/planner-statusline.md');
    if(!fs.existsSync(memo))throw Error('Install requires the maintained planner-statusline memo');
    const quote=s=>"'"+s.replaceAll("'","'\\''")+"'";
    const bin=path.join(home,'.local/bin'), backup=path.join(home,'.local/state/cartridge/planner-migration',String(Date.now()));
    const writes=[];
    for(const name of ['prd','pearde']){
      const file=path.join(bin,name), old=fs.existsSync(file)?fs.readFileSync(file,'utf8'):null;
      if(old&&!old.includes(owner)&&!old.includes('/dev/infra/pearde'))throw Error('Unrelated launcher already owns '+file);
      writes.push({file,old,next:'#!/bin/sh\nexec '+quote(path.join(owner,'prd'))+' "$@"\n',mode:0o755});
    }
    const settings=path.join(home,'.claude/settings.json');
    if(fs.existsSync(settings)){
      const old=fs.readFileSync(settings,'utf8'), value=JSON.parse(old), command=value.statusLine?.command;
      if(typeof command==='string'&&(command.includes('/dev/infra/pearde/')||command.includes(owner+'/.cartridge/engine/'))){
        const next=old.replace(JSON.stringify(command),JSON.stringify(quote(runner)+' '+quote(memo)+' status'));
        if(next===old)throw Error('Could not locate exact statusline command');
        writes.push({file:settings,old,next,mode:fs.statSync(settings).mode&0o777});
      }
    }
    fs.mkdirSync(backup,{recursive:true,mode:0o700});
    for(const [i,entry] of writes.entries()){
      fs.mkdirSync(path.dirname(entry.file),{recursive:true});
      if(entry.old!==null)fs.writeFileSync(path.join(backup,String(i)+'-'+path.basename(entry.file)),entry.old,{mode:0o600});
      const temporary=entry.file+'.cartridge-migration.tmp';fs.writeFileSync(temporary,entry.next,{flag:'wx',mode:entry.mode});fs.renameSync(temporary,entry.file);
    }
    const legacy=path.join(home,'dev/infra/pearde'), retired=path.join(owner,'.cartridge/engine');
    if(fs.existsSync(path.dirname(legacy))){
      try{if(fs.lstatSync(legacy).isSymbolicLink()&&path.resolve(path.dirname(legacy),fs.readlinkSync(legacy))===retired){fs.writeFileSync(path.join(backup,'retired-symlink-target'),fs.readlinkSync(legacy));fs.unlinkSync(legacy);}}catch(error){if(error.code!=='ENOENT')throw error;}
    }
    console.log('Installed native prd/pearde launchers; preserved superseded configuration in '+backup);
```

The legacy command name supports the native CLI documented by `prd help`; it does
not restore the retired dispatcher. Run `prd check --json`, `pearde help`, and
render the statusline with a disposable input before using the migrated tools.
