import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { atomic, codeRepo, document, edit, git, hash, openBoxes, recordFields, repoRoot, scan, specs, type Prd } from './records';
import { dependencies, feet } from './planner';
import { completionProblem, lane, removeLane, seedSubmodules, verify, type Options } from './lifecycle';

const head = (repo: string) => git(repo, ['rev-parse', 'HEAD']);
const paths = (prd: Prd) => feet(prd).map(file => path.relative(codeRepo(prd), file));
const committedBytes = (repo: string, file: string) => {
  const result = Bun.spawnSync(['git', '-C', repo, 'show', 'HEAD:' + path.relative(repo, file)]);
  return !result.exitCode && result.stdout.equals(fs.readFileSync(file));
};
export function historyProblem(prd: Prd): string | null {
  let receipt = document(path.join(prd.dir, 'collection.md'));
  const seen = new Set<string>(), records = repoRoot(prd.board);
  while (receipt.fm['previous-receipt']) {
    const digest = receipt.fm['previous-receipt'];
    if (typeof digest !== 'string' || !/^[a-f0-9]{64}$/.test(digest) || seen.has(digest)) return 'invalid collection receipt history';
    seen.add(digest);
    const file = path.join(prd.dir, 'collection-history', digest + '.md');
    if (!fs.existsSync(file) || hash(fs.readFileSync(file)) !== digest || !committedBytes(records, file)) return 'collection receipt history is missing, changed or uncommitted';
    receipt = document(file);
  }
  return null;
}
export function workspaceDrift(prd: Prd): { path: string; sha256: string }[] {
  const code = codeRepo(prd), scope = paths(prd);
  if (!scope.length) return [];
  const changed = git(code, ['diff', '--name-only', '--no-renames', '-z', String(prd.fm.commit || 'HEAD'), '--', ...scope]);
  const staged = git(code, ['diff', '--cached', '--name-only', '--no-renames', '-z', '--', ...scope]);
  const untracked = git(code, ['ls-files', '--others', '--exclude-standard', '-z', '--', ...scope]);
  return [...new Set((changed + '\0' + staged + '\0' + untracked).split('\0').filter(Boolean))].sort().map(file => {
    const absolute = path.join(code, file), stat = fs.lstatSync(absolute, { throwIfNoEntry: false });
    const bytes = !stat ? 'deleted' : stat.isSymbolicLink() ? fs.readlinkSync(absolute) : stat.isFile() ? fs.readFileSync(absolute) : 'directory:' + git(code, ['diff', '--', file]);
    return { path: file, sha256: hash(bytes) };
  });
}
export function workspaceProof(prd: Prd, graph = scan(prd.board), seen = new Set<string>()): { workspace_verified: boolean; workspace_drift: any[] } {
  if (seen.has(prd.dir)) return { workspace_verified: false, workspace_drift: [{ ref: prd.ref, reason: 'cycle' }] };
  const drift: any[] = workspaceDrift(prd);
  for (const ref of prd.children) {
    const child = graph.get(ref);
    if (!child) drift.push({ ref, reason: 'missing child' });
    else drift.push(...workspaceProof(child, graph, new Set(seen).add(prd.dir)).workspace_drift.map(item => ({ ref, ...item })));
  }
  return { workspace_verified: drift.length === 0, workspace_drift: drift };
}
function cleanIndex(repo: string) {
  if (git(repo, ['diff', '--cached', '--name-only'])) throw Error('repository has staged changes; preserve them before collection');
}
function children(prd: Prd, graph: Map<string, Prd>) {
  const records = repoRoot(prd.board);
  return Object.fromEntries(prd.children.map(ref => {
    const child = graph.get(ref)!;
    return [path.relative(records, child.file), hash(child.text + specs(child).map(s => s.text).join('') + document(path.join(child.dir, 'collection.md')).text)];
  }));
}
async function snapshotProof(prd: Prd, code: string, candidate: string, signal?: AbortSignal) {
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'prd-commit-')), tree = path.join(scratch, 'source');
  try {
    git(code, ['worktree', 'add', '--detach', tree, candidate]);
    seedSubmodules(code, tree);
    const clean = () => { if (git(tree, ['status', '--porcelain', '--untracked-files=all'])) throw Error('committed verification snapshot changed'); };
    clean();
    const evidence = await verify(prd, tree, signal);
    clean();
    return { evidence, tree };
  } finally {
    // This checkout was created here, never a user's lane. Remove only our artifacts.
    if (fs.existsSync(path.join(tree, '.git'))) {
      for (const line of git(tree, ['ls-tree', '-r', 'HEAD']).split('\n')) {
        const match = /^160000 commit [a-f0-9]+\t(.+)$/.exec(line);
        if (match && fs.statSync(path.join(tree, match[1], '.git'), { throwIfNoEntry: false })?.isFile()) git(path.join(code, match[1]), ['worktree', 'remove', '--force', path.join(tree, match[1])]);
      }
      git(code, ['worktree', 'remove', '--force', tree]);
    }
    fs.rmSync(scratch, { recursive: true, force: true });
  }
}
export async function collectCommitted(prd: Prd, graph: Map<string, Prd>, opts: Options, signal?: AbortSignal) {
  const refresh = opts.reverify === true;
  if (opts.trust) throw Error('collection requires executable verification; --trust is unavailable');
  if (refresh && prd.state !== 'done') throw Error('reverify requires a done PRD');
  if (!refresh && prd.state === 'done') throw Error('use --reverify to refresh a done PRD');
  if (refresh) { const problem = completionProblem(prd, graph, new Set(), true); if (problem) throw Error(problem); }
  else if (!prd.children.length && !['claimed', 'specced'].includes(prd.state)) throw Error('collect requires claimed or specced work');
  if (openBoxes(prd.text) || specs(prd).some(spec => openBoxes(spec.text))) throw Error('collect: open acceptance boxes remain');
  const validateDependencies = (current: Map<string, Prd>) => {
    const deps = dependencies(prd, current);
    if (deps.problems.length) throw Error('collect: dependencies are unresolved');
    for (const ref of new Set([...deps.refs, ...prd.children])) {
      const dependency = current.get(ref), problem = dependency ? completionProblem(dependency, current) : 'missing';
      if (problem) throw Error('collect: dependency ' + ref + ': ' + problem);
    }
  };
  validateDependencies(graph);
  const code = codeRepo(prd), records = repoRoot(prd.board), work = lane(prd), initialHead = head(code);
  const digests = () => Object.fromEntries(specs(prd).map(s => [path.basename(s.file), hash(s.text)]));
  const contract = JSON.stringify(digests()), childContract = JSON.stringify(children(prd, graph));
  const unchanged = (candidate: string) => {
    if (signal?.aborted) throw Error('collection cancelled before receipt publication');
    if (head(code) !== candidate) throw Error('source HEAD changed during verification');
    if (hash(document(prd.file).text) !== prd.revision || JSON.stringify(digests()) !== contract) throw Error('collection contract changed during verification');
    const current = scan(prd.board);
    validateDependencies(current);
    if (JSON.stringify(children(prd, current)) !== childContract) throw Error('collection child contract changed during verification');
  };
  if (!records) throw Error('collection records must live in a Git repository');
  cleanIndex(code); if (records !== code) cleanIndex(records);
  if (opts.dry) return 'Would verify committed source and preserve prior collection evidence.\n';
  const tree = fs.existsSync(work.directory) ? work.directory : code;
  let candidate = initialHead;
  if (tree !== code) {
    cleanIndex(tree);
    const scope = paths(prd);
    const assertScope = () => {
      const changed = git(tree, ['diff', '--name-only', '--no-renames', '-z', initialHead, 'HEAD']).split('\0').filter(Boolean);
      for (const file of changed) if (!scope.some(p => file === p || file.startsWith(p.replace(/\/$/, '') + '/'))) throw Error('committed path is outside the PRD footprint: ' + file);
    };
    assertScope();
    await verify(prd, tree, signal);
    unchanged(initialHead);
    if (scope.length) {
      const status = Bun.spawnSync(['git', '-C', tree, 'status', '--porcelain', '-z', '--untracked-files=all', '--', ...scope]);
      if (status.exitCode) throw Error('could not inspect lane source changes');
      const dirty = status.stdout.toString();
      if (dirty) {
        const entries = dirty.split('\0').filter(Boolean);
        if (entries.some(entry => /[RC]/.test(entry.slice(0, 2)))) throw Error('collection requires explicit handling of renames');
        const changed = entries.map(entry => entry.slice(3));
        git(tree, ['add', '--', ...changed]); git(tree, ['commit', '--only', '-m', 'Implement ' + prd.ref, '--', ...changed]);
      }
    }
    assertScope(); candidate = head(tree);
    if (Bun.spawnSync(['git', '-C', code, 'merge-base', '--is-ancestor', initialHead, candidate]).exitCode) throw Error('lane diverged from source HEAD; reconcile before collection');
    unchanged(initialHead);
    if (candidate !== initialHead) git(code, ['merge', '--ff-only', candidate]);
  }
  const proof = await snapshotProof(prd, code, candidate, signal);
  unchanged(candidate);
  const collection = path.join(prd.dir, 'collection.md'), old = fs.existsSync(collection) ? fs.readFileSync(collection, 'utf8') : null;
  const previous = old === null ? null : hash(old), archive = previous ? path.join(prd.dir, 'collection-history', previous + '.md') : null;
  if (archive && fs.existsSync(archive) && fs.readFileSync(archive, 'utf8') !== old) throw Error('collection receipt history collision');
  const original = old ? document(collection).fm['original-commit'] ?? prd.fm.commit : candidate;
  const currentPrd = { ...prd, fm: { ...prd.fm, commit: candidate } }, workspace = workspaceProof(currentPrd);
  const header = { commit: candidate, 'verification-target': 'committed', 'original-commit': original, ...(previous ? { 'previous-receipt': previous } : {}), 'spec-digests': digests(), 'child-contracts': JSON.parse(childContract), 'workspace-verified': workspace.workspace_verified, 'workspace-drift': workspace.workspace_drift };
  const receipt = '---\n' + Object.entries(header).map(([key, value]) => key + ': ' + JSON.stringify(value)).join('\n') + '\n---\n\n# Collection\n\nVerified committed snapshot ' + candidate + ' in ' + proof.tree + '.\n\n' + (proof.evidence.length ? proof.evidence.map(e => `${e.source}: exit 0\n\nCommand SHA-256: ${hash(e.command)}\n\n\`\`\`text\n${e.output}\n\`\`\`\n`).join('\n') : 'container: every child done\n');
  // Lane cleanup can refuse user-created files. Do it before publishing any new proof.
  if (tree !== code) removeLane(code, tree);
  unchanged(candidate);
  const archiveExisted = archive ? fs.existsSync(archive) : false;
  const files = [prd.file, collection, ...specs(prd).map(s => s.file), ...(archive ? [archive] : [])].map(file => path.relative(records, file));
  try {
    if (archive) atomic(archive, old!);
    atomic(collection, receipt);
    edit(prd.file, { state: 'done', claim: null, commit: candidate }, prd.revision);
    git(records, ['add', '--', ...files]);
    git(records, ['commit', '--only', '-m', (refresh ? 'Reverify ' : 'Collect ') + prd.ref, '--', ...files]);
  } catch (error) {
    atomic(prd.file, prd.text); recordFields(prd.file);
    if (old === null) fs.rmSync(collection, { force: true }); else atomic(collection, old);
    if (archive && !archiveExisted) fs.rmSync(archive, { force: true });
    git(records, ['reset', '-q', 'HEAD', '--', ...files]);
    throw error;
  }
  return `Verified and ${refresh ? 'reverified' : 'collected'} ${prd.ref} at ${candidate}; verification_target=committed, workspace_verified=${workspace.workspace_verified}, workspace_drift=${JSON.stringify(workspace.workspace_drift)}\n`;
}
