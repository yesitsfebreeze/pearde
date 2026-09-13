import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const records = import.meta.dir;
const root = path.resolve(records, "../../../../../..");
const committed = process.argv[2] === "--committed";
const owner = path.resolve(process.argv[committed ? 3 : 2] ?? "");
const options = process.argv.slice(committed ? 4 : 3);
if (options.length && (options.length !== 2 || options[0] !== "--sessions-revision" || !/^[0-9a-f]{40}$/.test(options[1]))) throw Error("expected --sessions-revision followed by a full commit SHA");
const sessionsRevision = options[1];
if (!fs.existsSync(path.join(owner, "Cargo.toml"))) throw Error("harness source owner required");
const digest = (value: Buffer | string) => new Bun.CryptoHasher("sha256").update(value).digest("hex");
const shadow = fs.mkdtempSync(path.join(os.tmpdir(), "cartridge-roster-verification-"));
const resultFile = path.join(records, "integration", path.basename(shadow) + ".json");
fs.mkdirSync(path.dirname(resultFile), { recursive: true });
const receipt: any = {
  owner, committed, pinned_revisions: sessionsRevision ? { "sessions.ctg": sessionsRevision } : {}, shadow, started: new Date().toISOString(), revisions: {}, inputs: {}, results: [],
  scope: "Exact selected owner and adjacent source snapshots. Public gates execute inside the disposable composition; a successful lane proof does not integrate owner changes."
};
const save = () => fs.writeFileSync(resultFile, JSON.stringify(receipt, null, 2) + "\n");
const run = (args: string[], cwd: string, env = process.env, proof = false) => {
  const started = new Date().toISOString();
  const out = Bun.spawnSync(args, { cwd, env, stdout: "pipe", stderr: "pipe", timeout: 300_000 });
  if (proof) {
    receipt.results.push({ command: args, cwd, started, completed: new Date().toISOString(), stdout: out.stdout.toString(), stderr: out.stderr.toString(), exit: out.exitCode });
    save();
    console.log(`${args.join(" ")}: ${out.exitCode === 0 ? "passed" : "failed"}`);
  }
  if (out.exitCode !== 0) throw Error(`${args.join(" ")} failed (${out.exitCode})\n${out.stdout}\n${out.stderr}`);
  return out.stdout.toString();
};
try {
  const repositories = ["cartridge.ctg", "docs.ctg", "agent.ctg", "fs.ctg", "gitfs.ctg", "harness.ctg", "landscape.ctg", "mcp.ctg", "memo.ctg", "memory-tool.ctg", "proxy.ctg", "pty.ctg", "router.ctg", "sessions.ctg", "tools.ctg"];
  const files = new Map<string, { source: string; sha256: string; mode: number }>();
  for (const repository of repositories) {
    let source = repository === "harness.ctg" ? owner : path.join(root, repository);
    const pin = repository === "sessions.ctg" ? sessionsRevision : undefined;
    receipt.revisions[repository] = run(["git", "rev-parse", pin ? pin + "^{commit}" : "HEAD"], source).trim();
    let names: string[];
    if ((repository === "harness.ctg" && committed) || pin) {
      const archiveOwner = source;
      const archive = path.join(shadow, "committed-" + repository + ".tar");
      run(["git", "archive", "--format=tar", "--output=" + archive, receipt.revisions[repository]], source);
      source = path.join(shadow, "committed-" + repository); fs.mkdirSync(source);
      run(["tar", "-xf", archive, "-C", source], shadow);
      names = run(["git", "ls-tree", "-rz", "--name-only", receipt.revisions[repository]], archiveOwner).split("\0").filter(Boolean);
    } else {
      names = run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], source).split("\0").filter(Boolean);
    }
    if (repository === "cartridge.ctg") names.push(".cartridge/workspace/Cargo.toml", ".cartridge/workspace/Cargo.lock");
    for (const name of new Set(names)) {
      const absolute = path.join(source, name);
      if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) continue;
      files.set(repository + "/" + name, { source: absolute, sha256: digest(fs.readFileSync(absolute)), mode: fs.statSync(absolute).mode });
    }
  }
  receipt.inputs = Object.fromEntries([...files].sort(([a], [b]) => a.localeCompare(b)));
  const identityInputs = Object.fromEntries([...files].map(([key, v]) => [key, { sha256: v.sha256, mode: v.mode }]).sort(([a], [b]) => String(a).localeCompare(String(b))));
  receipt.identity = digest(JSON.stringify(identityInputs));
  for (const [relative, input] of files) {
    const target = path.join(shadow, relative);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.copyFileSync(input.source, target); fs.chmodSync(target, input.mode);
    if (digest(fs.readFileSync(target)) !== input.sha256 || digest(fs.readFileSync(input.source)) !== input.sha256) throw Error("source changed during copy: " + input.source);
  }
  const copiedHarness = path.join(shadow, "harness.ctg");
  if (!fs.existsSync(path.join(copiedHarness, "src/roster.rs"))) throw Error("selected committed owner does not contain roster implementation");
  // Recheck the whole input set after copying to detect edits to earlier files.
  for (const input of files.values()) if (digest(fs.readFileSync(input.source)) !== input.sha256) throw Error("source changed during snapshot: " + input.source);
  save();
  const runtime = path.join(shadow, "cartridge.ctg");
  const target = path.join(root, "cartridge.ctg/target/roster-proof");
  const env = { ...process.env, RUSTC_WRAPPER: "", RUSTC_WORKSPACE_WRAPPER: "", CARGO_TARGET_DIR: target, CARGO_PROFILE_DEV_DEBUG: "0", CARGO_PROFILE_TEST_DEBUG: "0", CARGO_INCREMENTAL: "0" };
  for (const command of [["just", "test", "harness"], ["just", "check", "harness"], ["just", "build", "harness"], ["just", "build", "sessions"]]) run(command, runtime, env, true);
  run(["bun", "test", path.join(copiedHarness, ".cartridge/tests/integration/roster.test.ts")], runtime, {
    ...env, HARNESS_BINARY: path.join(target, "debug/harness"), SESSIONS_BINARY: path.join(target, "debug/sessions")
  }, true);
  receipt.binary_inputs = Object.fromEntries(["harness", "sessions"].map(name => [name, digest(fs.readFileSync(path.join(target, "debug", name)))]));
  receipt.resulting_workspace_lock_sha256 = digest(fs.readFileSync(path.join(runtime, ".cartridge/workspace/Cargo.lock")));
  receipt.completed = new Date().toISOString(); receipt.status = "passed"; save();
  console.log("Roster composition proof: " + resultFile);
} catch (error) {
  receipt.completed = new Date().toISOString(); receipt.status = "failed"; receipt.error = String(error); save();
  throw error;
}
