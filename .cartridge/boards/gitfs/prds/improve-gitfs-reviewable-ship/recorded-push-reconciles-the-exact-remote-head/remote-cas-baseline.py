import subprocess,tempfile,pathlib,os,json,hashlib
base=pathlib.Path(tempfile.mkdtemp(prefix='gitfs-push-probe-'))
def git(cwd,*args,env=None,okay=True):
 p=subprocess.run(['git','-C',str(cwd),*args],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if okay and p.returncode: raise RuntimeError(p.stderr.decode())
 return p
local=base/'local';remote=base/'remote.git';local.mkdir();git(local,'init','-q','-b','main');git(base,'init','--bare','-q',str(remote));git(local,'config','user.name','Fixture');git(local,'config','user.email','fixture@example.test')
(local/'file').write_text('base');git(local,'add','file');git(local,'commit','-qm','base');old=git(local,'rev-parse','HEAD').stdout.decode().strip();git(local,'push',str(remote),'HEAD:refs/heads/main');
(local/'file').write_text('next');git(local,'commit','-qam','next');new=git(local,'rev-parse','HEAD').stdout.decode().strip()
hooks=base/'hooks';hooks.mkdir();hook=hooks/'pre-push';hook.write_text('#!/bin/sh\nIFS=" " read -r lr lo rr ro || exit 1\n[ "$lo" = "$EXPECTED_NEW" ] && [ "$ro" = "$EXPECTED_OLD" ] && [ "$rr" = refs/heads/main ] || exit 1\nIFS=" " read -r extra && exit 1\nif [ -n "$RACE_COMMIT" ]; then git -C "$REMOTE_PATH" update-ref refs/heads/main "$RACE_COMMIT" "$EXPECTED_OLD" || exit 1; fi\nexit 0\n');hook.chmod(0o700)
env={**os.environ,'EXPECTED_NEW':new,'EXPECTED_OLD':old};args=['-c','core.hooksPath='+str(hooks),'push','--porcelain',str(remote),new+':refs/heads/main']
wrong=git(local,*args,env={**env,'EXPECTED_OLD':'0'*40},okay=False);afterwrong=git(remote,'rev-parse','refs/heads/main').stdout.decode().strip()
# Object already exists remotely to simulate another actor advancing after advertisement.
git(local,'push',str(remote),new+':refs/heads/seed');race=git(local,*args,env={**env,'RACE_COMMIT':new,'REMOTE_PATH':str(remote)},okay=False);afterrace=git(remote,'rev-parse','refs/heads/main').stdout.decode().strip()
git(remote,'update-ref','refs/heads/main',old,new);success=git(local,*args,env=env,okay=False);aftersuccess=git(remote,'rev-parse','refs/heads/main').stdout.decode().strip()
assert wrong.returncode!=0 and afterwrong==old
assert race.returncode!=0 and afterrace==new
assert success.returncode==0 and aftersuccess==new
out={'git_version':git(local,'--version').stdout.decode().strip(),'old':old,'new':new,'wrong_expected_refused':wrong.returncode,'wrong_expected_preserved':afterwrong==old,'advertisement_then_remote_advance_refused':race.returncode,'remote_cas_diagnostic':race.stderr.decode(),'ordinary_push_succeeded':success.returncode,'unrelated_seed_unchanged':git(remote,'rev-parse','refs/heads/seed').stdout.decode().strip()==new,'fixture':str(base)}
print(json.dumps(out,indent=2))
