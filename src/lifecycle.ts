import fs from 'node:fs';
import path from 'node:path';
import { atomic, codeRepo, contained, document, adoptFields, edit, fieldsProblem, fieldsRefusal, git, recordFields, hash, list, openBoxes, real, relative, repoRoot, resolve, scan, specs, type Prd } from './records';
import { dependencies, feet, refusal } from './planner';
import { runProcess } from './process';

export type Options = Record<string, string | boolean>;
export function argumentsOf(args: string[]) {
  const pos: string[] = [], opts: Options = {};
  const switches = new Set(['dry', 'check', 'once', 'json']);
  for (let i = 0; i < args.length; i++) {
    const token = args[i];
    if (!token.startsWith('--')) { pos.push(token); continue; }
    const [key, ...rest] = token.slice(2).split('=');
    if (key in opts) throw Error('duplicate option --' + key);
    if (switches.has(key)) { if (rest.length) throw Error('switch takes no value: ' + key); opts[key] = true; }
    else { const value = rest.length ? rest.join('=') : args[++i]; if (value === undefined) throw Error('missing value for --' + key); opts[key] = value; }
  }
  return { pos, opts };
}
export function lane(prd: Prd) {
  const slug = prd.local.replace(/[^A-Za-z0-9._-]+/g, '-');
  // Include the owner in the branch identity: two boards can target one repository.
  return { directory: path.join(prd.board, '.lanes', slug), branch: 'lane/' + path.basename(prd.board) + '-' + slug };
}
function ensureSpecs(prd: Prd) {
  const published = specs(prd);
  if (!published.length && !prd.children.length) throw Error('specced requires at least one published spec');
  for (const spec of published) {
    if (!/^## Acceptance\b/m.test(spec.body) || !/\[[ xX~]\]/.test(spec.body)) throw Error(spec.file + ': missing acceptance checks');
    if (!list(spec.fm.footprint).length && !list(prd.fm.footprint).length) throw Error(spec.file + ': missing footprint');
    if (!verificationBlocks(spec.text).length) throw Error(spec.file + ': missing executable verification');
  }
}
export function verificationBlocks(text: string): string[] {
  // Only blocks under explicit Verify/Proof headings execute, never example snippets.
  return text.split(/(?=^##\s)/m).filter(section => /^##\s+(?:Verify|Verification|Proof)\b/i.test(section)).flatMap(section => [...section.matchAll(/^```(?:sh|bash|shell)\s*\n([\s\S]*?)^```\s*$/gm)].map(m => m[1]));
}
export async function verify(prd: Prd, cwd: string, signal?: AbortSignal) {
  const blocks = specs(prd).flatMap(spec => verificationBlocks(spec.text).map(command => ({ command, source: spec.file, digest: hash(spec.text) })));
  if (!blocks.length && !prd.children.length) throw Error('no executable verification');
  const evidence = [];
  for (const block of blocks) {
    if (signal?.aborted) throw Error('verification cancelled');
    const checked = await runProcess(['sh', '-eu', '-c', block.command], { cwd, signal, timeout: 120_000, cap: 65536 });
    if (checked.state !== 'completed') throw Error('verification ' + checked.state + ': ' + checked.output);
    evidence.push({ source: block.source, digest: block.digest, command: block.command, exit_code: 0, output: checked.output });
  }
  return evidence;
}
function childContracts(prd: Prd, graph: Map<string, Prd>) {
  const records = repoRoot(prd.board);
  return Object.fromEntries(prd.children.map(ref => {
    const child = graph.get(ref)!;
    return [path.relative(records, child.file), hash(child.text + specs(child).map(s => s.text).join('') + document(path.join(child.dir, 'collection.md')).text)];
  }));
}
export function completionProblem(prd: Prd, context?: Map<string, Prd>, ancestors = new Set<string>()): string | null {
  const graph = context ?? scan(prd.board);
  prd = [...graph.values()].find(p => p.dir === prd.dir) ?? prd;
  if (ancestors.has(prd.dir)) return 'collection proof cycle';
  const seen = new Set(ancestors).add(prd.dir);
  if (prd.state !== 'done') return 'PRD is not done';
  if (prd.fm.claim) return 'done PRD still has a claim';
  const published = specs(prd);
  if (openBoxes(prd.text) || published.some(s => openBoxes(s.text))) return 'done PRD still has open acceptance boxes';
  if (!prd.children.length && !published.length) return 'done leaf has no published contract';
  const commits = String(prd.fm.commit ?? '').split(/\s+/).filter(Boolean);
  if (commits.length !== 1 || !/^[a-f0-9]{7,40}$/i.test(commits[0])) return 'done PRD has no valid integration commit receipt';
  const commit = commits[0], code = codeRepo(prd), records = repoRoot(prd.board);
  if (!records) return 'collection record has no Git repository';
  if (!git(code, ['log', '-1', '--format=%H', commit], false)) return 'unknown integration commit';
  if (Bun.spawnSync(['git', '-C', code, 'merge-base', '--is-ancestor', commit, 'HEAD']).exitCode) return 'receipt is not integrated in code repository';
  const evidence = path.join(prd.dir, 'collection.md');
  if (!fs.existsSync(evidence)) return 'no recorded collection verification evidence';
  const receipt = document(evidence), digests = receipt.fm['spec-digests'];
  if (receipt.fm.commit !== commit) return 'collection evidence names another integration commit';
  if (!digests || typeof digests !== 'object' || Array.isArray(digests) || Object.keys(digests).length !== published.length) return 'collection specification contract changed or lacks revision digests';
  for (const spec of published) if (digests[path.basename(spec.file)] !== hash(spec.text)) return 'collection specification changed after verification';
  for (const file of [prd.file, evidence, ...published.map(s => s.file)]) {
    const committed = Bun.spawnSync(['git', '-C', records, 'show', 'HEAD:' + path.relative(records, file)]);
    if (committed.exitCode || !committed.stdout.equals(fs.readFileSync(file))) return path.basename(file) + ' is not committed at the record HEAD';
  }
  if (!/: exit 0\b|container: every child done/.test(receipt.body)) return 'collection evidence records no passing verification';
  for (const ref of prd.children) {
    const child = graph.get(ref);
    if (!child) return 'collection child disappeared: ' + ref;
    const problem = completionProblem(child, graph, seen);
    if (problem) return ref + ': ' + problem;
  }
  if (prd.children.length && JSON.stringify(receipt.fm['child-contracts']) !== JSON.stringify(childContracts(prd, graph))) return 'collection child contract changed after verification';
  const paths = feet(prd).map(p => path.relative(code, contained(code, path.relative(code, p))));
  if (paths.length) {
    if (git(code, ['diff', '--name-only', commit, '--', ...paths]) || git(code, ['ls-files', '--others', '--exclude-standard', '--', ...paths])) return 'verified source footprint changed after collection';
  }
  if (fs.existsSync(lane(prd).directory)) return 'done PRD still has an active lane';
  return null;
}
export function verifiedStatus(prd: Prd) {
  const reason = completionProblem(prd);
  return { ref: prd.ref, state: prd.state, revision: prd.revision, commit: prd.fm.commit ?? null, verified: reason === null, integrated: reason === null, reason, evidence: path.join(prd.dir, 'collection.md') };
}
function cleanIndex(repo: string) {
  if (git(repo, ['diff', '--cached', '--name-only'])) throw Error('repository has staged changes; preserve them before collection');
}
async function collect(prd: Prd, graph: Map<string, Prd>, opts: Options, signal?: AbortSignal) {
  if (opts.trust) throw Error('collection requires executable verification; --trust is unavailable');
  if (prd.state === 'done') { const problem = completionProblem(prd); if (problem) throw Error(problem); return 'Already verified and collected.\n'; }
  const deps = dependencies(prd, graph);
  if (deps.problems.length || deps.refs.some(ref => graph.get(ref)?.state !== 'done')) throw Error('collect: dependencies are not done');
  if (openBoxes(prd.text) || specs(prd).some(spec => openBoxes(spec.text))) throw Error('collect: open acceptance boxes remain');
  if (!prd.children.length && !['claimed', 'specced'].includes(prd.state)) throw Error('collect requires claimed or specced work');
  for (const ref of prd.children) { const problem = completionProblem(graph.get(ref)!, graph); if (problem) throw Error(ref + ': ' + problem); }
  const code = codeRepo(prd), records = repoRoot(prd.board), work = lane(prd);
  const contractDigests = Object.fromEntries(specs(prd).map(s => [path.basename(s.file), hash(s.text)]));
  const childDigests = childContracts(prd, graph);
  const contractsUnchanged = () => {
    if (hash(document(prd.file).text) !== prd.revision || JSON.stringify(Object.fromEntries(specs(prd).map(s => [path.basename(s.file), hash(s.text)]))) !== JSON.stringify(contractDigests)) throw Error('collection contract changed during verification');
    const current = scan(prd.board), parent = [...current.values()].find(p => p.dir === prd.dir)!;
    for (const ref of parent.children) { const problem = completionProblem(current.get(ref)!, current); if (problem) throw Error(ref + ': ' + problem); }
    if (JSON.stringify(childContracts(parent, current)) !== JSON.stringify(childDigests)) throw Error('collection child contract changed during verification');
  };
  if (!records) throw Error('collection records must live in a Git repository');
  if (opts.dry) return 'Would verify, integrate and commit collection records.\n';
  const tree = fs.existsSync(work.directory) ? work.directory : code;
  cleanIndex(code); if (tree !== code) cleanIndex(tree);
  const initialHead = git(code, ['rev-parse', 'HEAD']);
  const assertFootprint = (candidate: string) => {
    const allowed = feet(prd).map(f => path.relative(code, f));
    // Disable rename detection so both old and new paths must be authorized.
    const diff = Bun.spawnSync(['git', '-C', tree, 'diff', '--name-only', '--no-renames', '-z', initialHead, candidate, '--'], { stdout: 'pipe', stderr: 'pipe' });
    if (diff.exitCode) throw Error('could not validate committed source footprint');
    const files = diff.stdout.toString().split('\0').filter(Boolean);
    for (const file of files) if (!allowed.some(f => file === f || file.startsWith(f.replace(/\/$/, '') + '/'))) throw Error('committed path is outside the PRD footprint: ' + file);
  };
  assertFootprint(git(tree, ['rev-parse', 'HEAD']));
  let evidence = await verify(prd, tree, signal);
  contractsUnchanged();
  if (signal?.aborted) throw Error('collection cancelled before integration');
  // Verification may write output; only explicitly declared source paths may enter a commit.
  // Ask only about the footprint: a composed repository worked by several sessions is
  // never globally clean, and an unrelated dirty path is not this collection's business.
  // The committed revision is still checked in full by assertFootprint below.
  const scope = feet(prd).map(f => path.relative(code, f));
  const status = Bun.spawnSync(['git', '-C', tree, 'status', '--porcelain=v1', '-z', '--untracked-files=all', '--', ...scope]).stdout.toString();
  const changed: string[] = [];
  const entries = status.split('\0').filter(Boolean);
  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i], file = entry.slice(3);
    if (entry.slice(0, 2).includes('R') || entry.slice(0, 2).includes('C')) throw Error('collection requires explicit handling of renames');
    if (tree === code && real(path.resolve(tree, file)).startsWith(real(prd.board) + '/')) continue;
    const target = contained(tree, file), allowed = feet(prd).map(f => path.relative(code, f));
    if (!allowed.some(f => file === f || file.startsWith(f.replace(/\/$/, '') + '/'))) throw Error('changed path is outside the PRD footprint: ' + file);
    changed.push(file);
  }
  if (git(code, ['rev-parse', 'HEAD']) !== initialHead) throw Error('source HEAD changed during verification; inspect before retry');
  if (changed.length) {
    git(tree, ['add', '--', ...changed]);
    git(tree, ['commit', '--only', '-m', 'Implement ' + prd.ref, '--', ...changed]);
  }
  const candidate = git(tree, ['rev-parse', 'HEAD']);
  assertFootprint(candidate);
  if (tree !== code && git(code, ['rev-parse', 'HEAD']) !== initialHead) throw Error('source HEAD changed during verification; inspect before retry');
  if (tree !== code && candidate !== initialHead) {
    if (Bun.spawnSync(['git', '-C', code, 'merge-base', '--is-ancestor', initialHead, candidate]).exitCode) throw Error('lane diverged from source HEAD; reconcile before collection');
    git(code, ['merge', '--ff-only', candidate]);
    evidence = await verify(prd, code, signal);
    contractsUnchanged();
  }
  if (signal?.aborted) throw Error('collection interrupted after integration; inspect source HEAD');
  if (git(code, ['rev-parse', 'HEAD']) !== candidate) throw Error('source HEAD changed before collection receipt');
  contractsUnchanged();
  const verifiedPaths = feet(prd).map(p => path.relative(code, p));
  if (verifiedPaths.length && (git(code, ['diff', '--name-only', candidate, '--', ...verifiedPaths]) || git(code, ['ls-files', '--others', '--exclude-standard', '--', ...verifiedPaths]))) throw Error('source footprint changed during integrated verification');
  if (tree !== code) git(code, ['worktree', 'remove', work.directory]);
  const specDigests = Object.fromEntries(specs(prd).map(s => [path.basename(s.file), hash(s.text)]));
  const receipt = '---\ncommit: ' + candidate + '\nspec-digests: ' + JSON.stringify(specDigests) + '\nchild-contracts: ' + JSON.stringify(childDigests) + '\n---\n\n# Collection\n\n' + (evidence.length ? evidence.map(e => `${e.source}: exit 0\n\nCommand SHA-256: ${hash(e.command)}\n\n\`\`\`text\n${e.output}\n\`\`\`\n`).join('\n') : 'container: every child done\n');
  atomic(path.join(prd.dir, 'collection.md'), receipt);
  edit(prd.file, { state: 'done', claim: null, commit: candidate }, prd.revision);
  const files = [prd.file, path.join(prd.dir, 'collection.md'), ...specs(prd).map(s => s.file)].map(file => path.relative(records, file));
  git(records, ['add', '--', ...files]);
  git(records, ['commit', '--only', '-m', 'Collect ' + prd.ref, '--', ...files]);
  return 'Verified and collected ' + prd.ref + ' at ' + candidate + '\n';
}
export async function transition(operation: string, board: string, args: string[], signal?: AbortSignal) {
  const { pos, opts } = argumentsOf(args), graph = scan(board);
  if (operation === 'add') {
    if (!pos.length) throw Error('add requires a title');
    const title = pos.join(' '), slug = title.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    if (!slug || slug.length > 160) throw Error('title cannot form a bounded PRD id');
    const parentPrd = opts.parent ? resolve(graph, String(opts.parent)) : undefined;
    if (parentPrd && !['open', 'analyzing', 'refine'].includes(parentPrd.state)) throw Error('children require an open parent');
    const owner = parentPrd?.board ?? board, parent = parentPrd?.dir ?? path.join(owner, 'prds');
    const file = contained(owner, path.relative(owner, path.join(parent, slug, 'prd.md')));
    if (fs.existsSync(file)) throw Error('PRD already exists');
    const repo = parentPrd ? codeRepo(parentPrd) : document(path.join(owner, 'settings.md')).fm.repo;
    if (!opts.dry) atomic(file, `---\nstate: open\norigin: requested\npriority: ${Number(opts.priority) || 50}\n${repo ? 'repo: ' + JSON.stringify(repo) + '\n' : ''}---\n\n# ${title}\n\n## Outcome\n\nDefine one observable outcome before specification.\n\n## Acceptance\n\n- [ ] Record the concrete acceptance checks.\n`);
    if (!opts.dry) recordFields(file);
    return (opts.dry ? 'Would create ' : 'Created ') + file + '\n';
  }
  if (!pos.length) throw Error(operation + ' requires one PRD reference');
  const prd = resolve(graph, pos[0]);
  if (operation === 'adopt') {
    if (pos.length !== 1 || typeof opts.by !== 'string' || !/^[A-Za-z0-9_.:@-]{1,256}$/.test(opts.by) || typeof opts.reason !== 'string' || !opts.reason.trim() || opts.reason.length > 1024) throw Error('adopt requires a PRD, --by <identity> and --reason "<text>"');
    if (opts.dry) return 'Would adopt ' + prd.ref + '\n';
    const change = adoptFields(prd, opts.by, opts.reason);
    return 'Adopted ' + prd.ref + ': ' + JSON.stringify(change.old) + ' -> ' + JSON.stringify(change.new) + '\n';
  }
  if (operation !== 'brief') { const problem = fieldsProblem(prd.file); if (problem) throw Error(fieldsRefusal(prd, problem)); }
  if (operation === 'collect') return collect(prd, graph, opts, signal);
  if (operation === 'brief') {
    const role = String(opts.role ?? (prd.state === 'open' ? 'analyst' : 'implementer'));
    if (!['analyst', 'implementer', 'verifier', 'collector'].includes(role)) throw Error('unknown worker role');
    const code = codeRepo(prd), work = lane(prd);
    return `# ${role}: ${prd.ref}\n\nBoard: ${prd.board}\nPRD: ${prd.file}\nRevision: ${prd.revision}\nSource HEAD: ${git(code, ['rev-parse', 'HEAD'])}\nRepository: ${fs.existsSync(work.directory) ? work.directory : code}\nAllowed paths: ${feet(prd).join(', ') || 'define before implementation'}\nDeadline: 20 minutes\n\n${prd.body}\n\n${specs(prd).map(s => s.text).join('\n\n')}\n\nRecord observed checks and recovery. Use checked PRD transitions; exit zero alone does not establish completion.\n`;
  }
  let changes: Record<string, unknown> = {};
  if (operation === 'claim') {
    if (pos.length !== 2 || !/^[A-Za-z0-9_.:@-]{1,256}$/.test(pos[1])) throw Error('claim requires PRD and worker identity');
    const reason = refusal(prd, graph); if (reason) throw Error(reason);
    if (prd.state === 'specced') {
      ensureSpecs(prd);
      const work = lane(prd), code = codeRepo(prd);
      if (fs.existsSync(work.directory) || git(code, ['rev-parse', '--verify', 'refs/heads/' + work.branch], false)) throw Error('pre-existing lane must be inspected before claim');
      if (!opts.dry) { fs.mkdirSync(path.dirname(work.directory), { recursive: true }); git(code, ['worktree', 'add', '-b', work.branch, work.directory, 'HEAD']); }
    }
    changes = { state: prd.state === 'open' ? 'analyzing' : 'claimed', claim: pos[1] + ' ' + new Date().toISOString() };
  } else if (operation === 'release') {
    const to = pos[1], allowed: Record<string, string[]> = { analyzing: ['refine', 'question', 'open'], claimed: ['blocked', 'failed'], question: ['open'] };
    if (!to || !(allowed[prd.state] ?? ['open']).includes(to) || ['done', 'specced', 'open'].includes(prd.state)) throw Error('invalid release transition');
    if (to === 'question' && !/^## Questions\b/m.test(prd.body)) throw Error('question: no Questions section');
    if (to === 'blocked' && !list(prd.fm.needs).length) throw Error('blocked: no needs naming the prerequisite');
    if (to === 'failed' && !/^## Failure\b/m.test(prd.body)) throw Error('failed: no Failure section');
    changes = { state: to, claim: null };
  } else if (operation === 'specced') {
    if (!['open', 'analyzing', 'refine', 'specced'].includes(prd.state)) throw Error('cannot publish specs from ' + prd.state);
    ensureSpecs(prd); changes = { state: 'specced', claim: null };
    for (const key of ['workflow', 'route', 'lane']) if (opts[key]) changes[key] = opts[key];
    if (opts.blast) changes['blast-radius'] = opts.blast;
  } else if (operation === 'refine') {
    if (!['open', 'analyzing', 'refine'].includes(prd.state)) throw Error('cannot refine from ' + prd.state);
    if (!prd.children.length) throw Error('refine requires defined child PRDs; add each small outcome with --parent');
    changes = { state: 'open', claim: null };
  } else if (operation === 'defer') {
    if (prd.fm.claim) throw Error('release the active claim first'); changes = { state: 'deferred' };
  } else if (operation === 'retry' || operation === 'unblock') {
    if (prd.state !== (operation === 'retry' ? 'failed' : 'blocked')) throw Error('invalid ' + operation + ' state');
    const deps = dependencies(prd, graph);
    if (deps.problems.length || deps.refs.some(ref => graph.get(ref)?.state !== 'done')) throw Error('prerequisites remain unresolved');
    changes = { state: 'specced', claim: null };
  } else throw Error('unsupported lifecycle operation: ' + operation);
  if (!opts.dry && !opts.check) edit(prd.file, changes, prd.revision);
  return `${opts.dry || opts.check ? 'Would transition' : 'Transitioned'} ${prd.ref}: ${prd.state} → ${changes.state}\n`;
}
