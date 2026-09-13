---
complexity: small
footprint: [".cartridge/tests/unit/src/tests/reload.rs","src/loader.rs",".cartridge/tests/unit/src/tests/mod.rs",".cartridge/tests/unit/src/tests/composition.rs"]
---

# spec01 — Wait for the nested generation before asserting its surface

Hold the initial nested provider behind an explicitly missing dependency. The
parent and sibling can announce startup while this generation remains waiting.
The existing 60 ms settle helper must still leave the read unavailable. Publish
the dependency, await this exact fiber's settled boundary with a five-second
failure deadline, require Active with no error, and only then assert its value.
This uses the existing lifecycle contract and needs no production API change.

## Acceptance

- [x] A dependency barrier forces the old startup observation to fail even after the old delay, then the same fixture reads version 1 after generation readiness.
- [x] Successful replacements return a different active generation; failed candidate 3 keeps generation 2 active and readable; candidate 4 can recover.
- [x] The existing development gate includes the fixture and twenty unchanged-binary runs pass.

## Verify and Proof

```sh
# The central lane lives inside another .cartridge directory. memo-run currently
# derives the wrong owner there; run Cargo directly in the lane, then the public
# gate in the source checkout during the collector's integrated verification.
if [ -f .git ]; then
    cargo test --all-targets tests::reload
else
    just test runtime tests::reload
fi
cargo test --lib tests::reload --message-format=json > target/reload-test-artifacts.json
python3 - <<'PYTEST'
import json, subprocess
from pathlib import Path
executables = [row['executable'] for line in Path('target/reload-test-artifacts.json').read_text().splitlines() if line.startswith('{') and (row := json.loads(line)).get('reason') == 'compiler-artifact' and row.get('executable') and row.get('profile', {}).get('test')]
assert len(executables) == 1, executables
for _ in range(20):
    subprocess.run([executables[0], 'tests::reload::'], check=True, stdout=subprocess.DEVNULL)
print('20 unchanged-binary reload regression runs passed')
PYTEST
```
