"""Run investigation reproductions against the current memory source in a disposable crate."""
import json, pathlib, subprocess, tempfile, shutil
here = pathlib.Path(__file__).resolve().parent
root = next(parent for parent in here.parents if (parent / "memory.ctg/src/graph/Cargo.toml").exists())
with tempfile.TemporaryDirectory(prefix="memory-review-probes-") as directory:
    crate = pathlib.Path(directory)
    (crate / "src").mkdir()
    manifest = '[package]\nname="memory-review-probes"\nversion="0.0.0"\nedition="2021"\n[dependencies]\n'
    for name, relative in {"graph":"graph", "base":"base", "util":"util", "config":"config", "retrieval-piece":"retrieval/piece"}.items():
        manifest += name + "={path=" + json.dumps(str(root / "memory.ctg/src" / relative)) + "}\n"
    manifest += 'serde_json="1"\ntempfile="3"\n'
    (crate / "Cargo.toml").write_text(manifest)
    shutil.copyfile(here / "probe-Cargo.lock", crate / "Cargo.lock")
    source = (here / "probes.rs").read_text().replace("/Users/feb/dev/cartridge/memory.ctg", str(root / "memory.ctg"))
    (crate / "src/lib.rs").write_text(source)
    subprocess.run(["cargo", "test", "--locked", "--manifest-path", str(crate / "Cargo.toml"), "--", "--nocapture"], check=True)
