#!/usr/bin/env python3
"""`pearde run`: the frontier's waves actually launched.

The other half of @resources/board/run.py. That file reads — discovery,
`real_feet`, `frontier`, `waves`, `slots`, `progress` — and this one runs what
it read: a rolling pool of pass workers, `slots()` wide, each row started the
moment a slot is free and nothing in flight clashes with its real-path
footprint. None of the read path's arithmetic is re-derived here; it is
imported.

    pearde run                  plan the cwd board, then dispatch it
    pearde run --dry            the plan, launching nothing
    pearde run --once           one fill, then report and stop
    pearde run all              the same over every watched board
    pearde run <group>          the same over one group of boards

This file is a library, not a command word. `run` resolves the scope and hands
the entries here; `pearde plan` is the read that moves nothing.
"""
import argparse
import os
import re
import subprocess
import sys
import time

# this file's own directory IS the board/ dir — the shipped code is imported
# from beside it, never from a path written down
BOARD = HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BOARD))
sys.path.insert(0, BOARD)
import run as runlib            # noqa: E402  the shipped read path
import plan as planlib          # noqa: E402
import serve as servelib        # noqa: E402
import transitions as trans     # noqa: E402  the same gate `claim` asks


# ── 1. a launch is not a worker ──────────────────────────────────────────────
# The load meter is a proxy. What actually bounds this machine is the model
# gateway: a 402 or a 429 comes back as a process that exits in under a second
# with an error in its log, and a dispatcher that counted the launch has
# already given away the slot and will report the row as worked.
#
# Measured on this repo 2026-09-02 with a stand-in binary that prints
# `API Error: 402 ...` and exits 1: the Popen call returns successfully, the
# pid is real, and `poll()` is None for the first ~5 ms. So "it started" is
# never the test. The two tests that hold are:
#
#   1. it is still running after GRACE seconds, and
#   2. its log holds no line matching DEAD_PAT.
#
# Both are needed. A worker that dies at second 30 passes (1) at second 2, and
# a worker that logs a retried-and-recovered 429 fails (2) while alive — so
# (2) is only ever consulted on a process that has EXITED, and (1) only inside
# the grace window.
GRACE = float(os.environ.get("PEARDE_LAUNCH_GRACE", "2.0"))
DEAD_PAT = re.compile(
    r"API Error|Credit balance|credit balance too low|"
    r"insufficient[_ ]quota|429 |402 |rate.?limit", re.I)
RETRIES = 1     # a dead worker is re-dispatched once; a second death is named


class Job:
    """One launched pass worker: the row it is working, the process, and the
    log the adapter is writing. `feet` is carried so a queued row can be
    clash-checked against what is IN FLIGHT, not against a wave computed
    before anything started."""

    def __init__(self, row, proc, log_path, attempt=1):
        self.row = row
        self.proc = proc
        self.log_path = log_path
        self.attempt = attempt
        self.t0 = time.time()
        self.verdict = None      # None while live; "ok"/"dead: …"/"exit N"

    @property
    def addr(self):
        return self.row["addr"]

    @property
    def feet(self):
        return self.row["feet"]

    def log_tail(self, n=4000):
        try:
            with open(self.log_path, encoding="utf-8", errors="replace") as fh:
                return fh.read()[-n:]
        except OSError:
            return ""

    def poll(self):
        """(finished, verdict). A live process is (False, None).

        The grace window is the whole point: `proc.poll() is None` one
        millisecond after Popen returns is true of a worker that is about to
        die on a 402, so the slot is not confirmed until GRACE has passed."""
        rc = self.proc.poll()
        if rc is None:
            return False, None
        tail = self.log_tail()
        hit = DEAD_PAT.search(tail)
        if hit:
            line = next((l.strip() for l in tail.splitlines()
                         if DEAD_PAT.search(l)), hit.group(0))
            return True, f"dead: {line[:160]}"
        if rc != 0:
            return True, f"dead: exited {rc} with no error line"
        if time.time() - self.t0 < GRACE:
            return True, (f"dead: exited 0 after "
                          f"{time.time() - self.t0:.2f}s — under the "
                          f"{GRACE:g}s launch grace, so it never worked")
        return True, "ok"


# ── 2. the refusal, re-asked at the moment of launch ─────────────────────────

def refusal(row):
    """Why this row may not be dispatched right now, or None.

    `frontier` read every board once, and between that read and this launch a
    session on that board may have claimed the row itself. So the gate is
    re-asked here, against a FRESH scan of that one board, and the same gate
    `pearde claim` uses — `transitions.gate_claim`, which is
    `plan.dispatchable` plus the drill gate — so what this pool launches
    is exactly what `claim` would take.

    A refusal is returned as its own sentence and the row is skipped by name;
    it is never dropped silently."""
    try:
        prds = planlib.scan(row["path"])
    except Exception as e:
        return f"board unreadable — {type(e).__name__}: {e}"
    prd = prds.get(row["rel"])
    if prd is None:
        return "gone from the board since the frontier was read"
    if prd["state"] not in ("open", "specced"):
        return f"now `{prd['state']}` — it moved since the frontier was read"
    try:
        trans.gate_claim(row["path"], prds, prd)
    except trans.Refused as e:
        return str(e)
    except Exception as e:
        return f"gate error — {type(e).__name__}: {e}"
    return None


# ── 3. the launch ────────────────────────────────────────────────────────────

def adapter(name=None):
    """The launch target, from `serve.load_adapters` — the same JSON files the
    view's Start button uses. Not a second launcher: one adapter set, one
    prompt template, one resolution of the binary."""
    ads = servelib.load_adapters()
    if not ads:
        raise SystemExit("pearde run: no adapter under "
                         "resources/board/adapters/")
    if name:
        a = next((x for x in ads if x["id"] == name), None)
        if not a:
            raise SystemExit(f"pearde run: no adapter {name!r}")
        return a
    if len(ads) == 1:
        return ads[0]
    raise SystemExit("pearde run: several adapters — name one with "
                     f"--adapter ({', '.join(a['id'] for a in ads)})")


def launch(row, ad, attempt=1):
    """Start one pass worker on one board, scoped to one PRD.

    `cwd` is the board's repo (the board dir's parent), which is what the
    daemon's own `/run` does. The log is the same file `/run` writes,
    `<board>/.state/run-<rel>.log`, so a run started here and a run started
    from the view leave one trail rather than two."""
    prompt = ad["prompt"].format(rel=row["rel"])
    argv = [p.format(prompt=prompt, rel=row["rel"]) for p in ad["command"]]
    resolved = servelib.adapter_bin(argv[0])
    if not resolved:
        return None, (f"{argv[0]!r} not on PATH — set PEARDE_ADAPTER_BIN or "
                      f"fix the {ad['id']} adapter")
    argv[0] = resolved
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", row["rel"])
    log_path = os.path.join(planlib.state_dir(row["path"]), f"run-{safe}.log")
    try:
        log = open(log_path, "a", encoding="utf-8")
        log.write(f"\n─── pearde run {time.strftime('%F %T')} "
                  f"attempt {attempt} · {row['addr']}\n")
        log.flush()
        proc = subprocess.Popen(argv, cwd=os.path.dirname(row["path"]),
                                stdout=log, stderr=log,
                                start_new_session=True,
                                shell=(os.name == "nt"))
    except OSError as e:
        return None, f"could not start: {e}"
    return Job(row, proc, log_path, attempt), None


# ── 4. the rolling dispatch ──────────────────────────────────────────────────

def board_caps(entries):
    """Each board's own `workers:` — untouched by this command and honoured
    by it. Fork 3 of the parent: the machine-wide count is a dispatch-time
    override, and a board's own cap is never written to. `0` is unlimited."""
    caps = {}
    for key, path in entries:
        n = planlib.plan_workers(path, None)
        caps[key] = None if not n else n
    return caps


def live_progress(entries, nslots, live, done, refused, dead):
    """The merged progress line, re-read, with what this run is holding on the
    end of it. `run.progress` is the board's own line over the whole set
    (@references/parts/progress.md) and is not re-derived here — the dispatch
    counts are appended to it, so a person reads one line and sees both the
    machine and this run."""
    rows, _, _ = runlib.frontier(entries, nslots)
    wv, _ = runlib.waves(rows, nslots)
    return (runlib.progress(entries, rows, wv, nslots)
            + f" · in flight {len(live)} · in {len(done)}"
            + f" · skipped {len(refused)} · dead {len(dead)}")


def dispatch(entries, rows, nslots, ad, dry=False, once=False,
             log=print, poll_every=0.5, deadline=None, tick=None):
    """Run the frontier down to nothing, `nslots` at a time.

    The waves `plan` prints are the PLAN; this is the plan run live. A
    queued row starts when three things are true at once:

      * a slot is free (machine-wide `nslots`, and the row's own board's
        `workers:` under it),
      * nothing IN FLIGHT clashes with its real-path footprint, and
      * the claim gate does not refuse it now.

    Clash-checking the in-flight set rather than a precomputed wave is the
    same guarantee — no two writers on one real path — reached without a
    barrier: wave 2's first row starts the moment wave 1's clashing row is
    in, instead of waiting for wave 1's slowest.

    Returns (done, refused, dead) — every row accounted for by name."""
    pool = [r for r in rows
            if not r["held"] and not r["collect"]
            and r["state"] in ("open", "specced")]
    caps = board_caps(entries)
    live, done, refused, dead = [], [], [], []
    started, moved = 0, False
    while pool or live:
        # ── reap ────────────────────────────────────────────────────────────
        still = []
        for j in live:
            fin, why = j.poll()
            if not fin:
                still.append(j)
                continue
            if why == "ok":
                log(f"in   {j.addr} · {time.time() - j.t0:.0f}s")
                done.append((j.addr, why))
                moved = True
            elif j.attempt <= RETRIES:
                log(f"DEAD {j.addr} · {why} · re-dispatching once")
                pool.insert(0, dict(j.row, _attempt=j.attempt + 1))
            else:
                log(f"DEAD {j.addr} · {why} · not re-dispatched again")
                dead.append((j.addr, why))
                moved = True
        live = still
        if moved and tick:
            # a transition is where the progress line is printed on this
            # board, and a dispatch across the machine is no exception
            tick(live_progress(entries, nslots, live, done, refused, dead))
            moved = False

        # ── fill ────────────────────────────────────────────────────────────
        rest = []
        for r in pool:
            if len(live) >= nslots:
                rest.append(r)
                continue
            cap = caps.get(r["board"])
            if cap and sum(1 for j in live if j.row["board"] == r["board"]) >= cap:
                rest.append(r)
                continue
            blocker = next((j.addr for j in live
                            if runlib.clash(r["feet"], j.feet)), None)
            if blocker:
                rest.append(r)
                continue
            why = refusal(r)
            if why:
                log(f"skip {r['addr']} · {why}")
                refused.append((r["addr"], why))
                continue
            if dry:
                log(f"would {r['addr']} · {ad['prompt'].format(rel=r['rel'])}"
                    f" in {os.path.dirname(r['path'])}")
                done.append((r["addr"], "dry"))
                continue
            job, err = launch(r, ad, r.get("_attempt", 1))
            if job is None:
                log(f"FAIL {r['addr']} · {err}")
                dead.append((r["addr"], err))
                continue
            log(f"out  {r['addr']} · pid {job.proc.pid}")
            live.append(job)
            started += 1
        pool = rest

        if once:
            break
        if deadline and time.time() > deadline:
            log(f"stop · deadline reached with {len(live)} in flight")
            break
        if live:
            time.sleep(poll_every)
        elif pool:
            # nothing in flight and nothing startable: every remaining row is
            # blocked by a clash with a job that just ended, so loop once more
            continue
    return done, refused, dead


# ── 5. the command ───────────────────────────────────────────────────────────

def main(argv, entries=None, only=None):
    """`entries` are the boards `run` resolved the scope to; `only` is a PRD
    rel when the scope was a PRD, and the frontier is then cut to that
    subtree. Neither is a flag: the scope word is the command's argument, and
    the resolving is @resources/board/run.py's."""
    ap = argparse.ArgumentParser(prog="pearde run")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--adapter")
    ap.add_argument("--workers", type=int, default=0,
                    help="dispatch-time override; 0 = the load-derived count")
    ap.add_argument("--deadline", type=float, default=0.0)
    a = ap.parse_args(argv)

    skipped = []
    if entries is None:
        entries, skipped = runlib.boards()
        if isinstance(skipped, str):
            print(f"pearde run: {skipped}", file=sys.stderr)
            return 1
    nslots, reading = runlib.slots()
    if a.workers:
        nslots = a.workers
        reading = f"{nslots} slots (override) · " + reading
    rows, notes, demand = runlib.frontier(entries, nslots)
    if only:
        # a PRD scope is the loop over that subtree: the PRD itself and every
        # PRD under it, and nothing else on the board is a launch candidate
        pre = only.rstrip("/") + "/"
        rows = [r for r in rows if r["rel"] == only or r["rel"].startswith(pre)]
        notes = notes + [f"scope `{only}`: {len(rows)} PRD(s) in that subtree"]
    wv, defer = runlib.waves(rows, nslots)

    # contract step 4: the order is printed BEFORE anything moves
    print(runlib.text(rows, wv, skipped, notes, reading,
                    [k for k, _ in entries], demand, defer))
    print()
    print(runlib.progress(entries, rows, wv, nslots))
    print()

    ad = adapter(a.adapter)
    done, refused, dead = dispatch(entries, rows, nslots, ad,
                                   dry=a.dry, once=a.once, tick=print,
                                   deadline=(time.time() + a.deadline
                                             if a.deadline else None))
    print()
    print(runlib.progress(entries, runlib.frontier(entries, nslots)[0], wv, nslots))
    print(f"dispatched {len(done)} · refused {len(refused)} · dead {len(dead)}")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
