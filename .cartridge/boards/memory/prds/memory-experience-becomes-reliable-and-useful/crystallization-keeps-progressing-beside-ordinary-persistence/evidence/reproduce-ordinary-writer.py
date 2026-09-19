#!/usr/bin/env python3
"""Run the pre-fix probe in a disposable archive; never overwrite live artifacts."""
import io, os, pathlib, subprocess, tarfile, tempfile
root = next(parent for parent in pathlib.Path(__file__).resolve().parents if (parent / "memory.ctg" / "Cargo.toml").is_file())
repo = root / "memory.ctg"
assert repo.is_dir(), repo
snapshot = pathlib.Path(tempfile.mkdtemp(prefix="memory-writer-repro-"))
data = subprocess.check_output(["git", "-C", str(repo), "archive", "ff22be8"])
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    archive.extractall(snapshot)
subprocess.run(["git", "apply", str(pathlib.Path(__file__).with_name("ordinary-writer-reproduction.patch"))], cwd=snapshot, check=True)
barrier = snapshot / "probe-barrier"
barrier.mkdir()
env = dict(os.environ, CARGO_TARGET_DIR="/tmp/cartridge-memory-stack-writer-reproduction-target", MEMORY_WRITER_REPRO_BARRIER=str(barrier))
print("Snapshot:", snapshot, flush=True)
subprocess.run(["cargo", "test", "--locked", "-p", "rpc", "experience_probe_actual_ordinary_save_window_then_retry", "--lib", "--", "--nocapture"], cwd=snapshot, env=env, check=True)
