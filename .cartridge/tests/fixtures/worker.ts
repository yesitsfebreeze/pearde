// Deterministic external adapter fixture: no model or network access.
import path from 'node:path';
import { execute } from '../../../src/engine';
import { atomic, scan } from '../../../src/records';
const [board, ref] = process.argv.slice(2);
const prd = scan(board).get(ref)!;
const name = prd.local.replaceAll('/', '-') + '.txt';
let answer;
if (prd.children.length) answer = await execute('collect', board, [ref]);
else if (prd.state === 'analyzing') {
  atomic(path.join(prd.dir, 'specs/spec01.md'), `---\ncomplexity: 1\nfootprint: [${name}]\n---\n\n# Spec\n\n## Acceptance\n\n- [x] Output matches\n\n## Verify\n\n\`\`\`sh\ntest "$(cat ${name})" = changed\n\`\`\`\n`);
  answer = await execute('specced', board, [ref]);
} else {
  atomic(path.join(process.cwd(), name), 'changed\n');
  answer = await execute('collect', board, [ref]);
}
if (answer.exit_code) console.error(answer.error);
process.exitCode = answer.exit_code;
