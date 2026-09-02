"""Run candidate verify blocks exactly as collect.run() does: the block on
stdin of `bash -e -o pipefail`, cwd = a fixture tree."""
import subprocess, sys, os, tempfile, shutil

def run(script, cwd):
    r = subprocess.run(["bash", "-e", "-o", "pipefail"], cwd=cwd,
                       input=script, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def fixture(broken):
    d = tempfile.mkdtemp(prefix="vb-")
    # the "probe" the verify block pipes: prints a tally, exits 0 either way
    open(os.path.join(d, "probe0.sh"), "w").write(
        "echo '  ok    A'\n"
        + ("echo '  FAIL  B'\n" if broken else "echo '  ok    B'\n")
        + ("echo '2 checks · 1 pass · 1 fail'\n" if broken
           else "echo '2 checks · 2 pass · 0 fail'\n"))
    # a probe that exits non-zero when the tree is broken
    open(os.path.join(d, "probe1.sh"), "w").write(
        "echo '  ok    A'\n"
        + ("echo '  FAIL  B'\nexit 1\n" if broken else "echo '  ok    B'\n"))
    return d

CASES = {
 "A pipe to tail, probe exits 0 on broken":
   "bash probe0.sh 2>&1 | tail -1\n",
 "B pipe to grep, probe exits 0 on broken":
   "bash probe0.sh 2>&1 | tail -1 | grep -E '0 fail$'\n",
 "C pipe to tail, probe exits 1 on broken":
   "bash probe1.sh 2>&1 | tail -1\n",
 "D pipe to grep -c, probe exits 1 on broken":
   "bash probe1.sh 2>&1 | grep -c '^  ok'\n",
 "E pipe into a var assignment":
   "OUT=$(bash probe1.sh 2>&1 | tail -1)\necho \"$OUT\"\n",
 "F pipe into `export`":
   "export OUT=$(bash probe1.sh 2>&1 | tail -1)\necho \"$OUT\"\n",
 "G bare grep, no file (reads the script off stdin)":
   "bash probe1.sh > out.txt 2>&1\ngrep -q 'FAIL'\necho reached-the-end\n",
 "H probe reads stdin (eats the rest of the block)":
   "cat > /dev/null\nbash probe1.sh 2>&1 | tail -1\necho reached-the-end\n",
 "I pipe, then a later assertion after a stdin-eater":
   "bash probe0.sh 2>&1 | grep -q 'ok    A'\n"
   "cat\n"
   "bash probe0.sh 2>&1 | grep -q '0 fail'\n"
   "echo reached-the-end\n",
 "J pipe to head (SIGPIPE on the writer)":
   "bash probe0.sh 2>&1 | head -1\n",
 "K pipeline behind ||, counter never asserted":
   "N=0\nbash probe0.sh 2>&1 | tail -1 | grep -qE '0 fail$' || N=$((N+1))\n"
   "echo \"$N problem(s)\"\n",
}

for name, script in sorted(CASES.items()):
    for broken in (False, True):
        d = fixture(broken)
        code, out = run(script, d)
        shutil.rmtree(d)
        state = "broken" if broken else "clean "
        print(f"{name:52s} {state}  exit {code:3d}  "
              f"{out.strip().replace(chr(10), ' / ')[:60]}")
    print()
