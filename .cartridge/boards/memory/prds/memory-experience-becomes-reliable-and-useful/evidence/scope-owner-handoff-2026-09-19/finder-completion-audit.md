# Finder completion audit

The original objective is a finder.nvim-style composable fuzzy search over ASP and project disk files. The previous turn made progress by committing the verified migration baseline. This turn verified remaining interactions and committed their fixes.

| Requirement | Current evidence |
| --- | --- |
| Typed composable sources and filters | filter_chain.py declares ASP, All, Files, Dirs, Grep, Fuzzy, Type and Expand contracts. test_finder covers compatible chains, quoted separators and rejecting incompatible inputs. |
| Fuzzy finding | RapidFuzz subsequence preselection and deterministic ranking in filter_chain.py. Tests cover path abbreviations and line content. A fresh 100000-path probe returned 856 hits in 9.74 ms median across five runs; this measures filtering/ranking only. |
| Tab completion and chaining/backtracking | FinderInput drives compatible completion, all/selected/marked scope forwarding and Shift-Tab. Tests cover completion, chained Grep, backtracking and waiting for the latest filter before capturing a scope. |
| Both ASP and disk | The isolated final binary and host passed ASP jev > Grep needle and Files search.txt > Grep needle, using actual ASP RPC and ripgrep. Mixed source tests and complete input identity cache tests pass. |
| Fast bounded presentation | test_navigation exercises 10000 rows with a maximum 300 mounted rows, page and wheel transitions, stable selection and updates. Disk search cancellation kills and reaps its subprocess. Results are capped and partial/error states are surfaced. |
| One shared list and item-specific detail | Generic Context/DetailTree and declared owner detail events work for all ASP types. Three plugin renderer integration cases passed through the isolated base binary. Their separate owner source collection remains outside the requested Scope commit. |
| Usage waterfall independent of list ranking | Model/timeline fixtures verify retained use, ordering and coordinated selection. Seventeen ASP tests passed for roots, schemas, retained activity and monitor reads. Memory processing status semantics remain the separate memory PRD task. |
| Center input and 50/50 preview/results | Layout tests assert preview above input, results below, equal pane heights and resize behavior. F4 selects detail/waterfall. |
| Terminal palette and foreground highlights | scope.tcss uses ansi_default and ANSI foreground accents, with reverse style on focused selections. Existing navigation tests verify relevant rendered styles; no custom background palette is introduced. |
| Natural memo jev and agent-directed filtering | Natural type/query tests and prior native agent evidence establish the agent conversation. A new test verifies agent-returned composed chains use the finder backend. F5 stays on that backend. |
| Ctrl-E, external editor and normal update path | EditSession tests verify registered session/run/call IDs, tool.read and tool.write, owner revision guards and generic agent change proposals. A real PTY probe passed Ctrl-E, F6 with a chosen editor, Ctrl-S tool dispatch and Ctrl-Q. A prior actual file save probe verified materialization and session touched paths. Draft-switch/conflict tests pass. |
| Base migration and old UI removal | Base b4345b6 and root a5b2719 committed the embedded UI, required ASP support and seven legacy deletions. Follow-up base dd75e7f and root de26542 contain the verified interaction fixes. No memory source/docs were selected. |
| Launch and isolated verification | Final binary /tmp/scope-finder-final-target/debug/cartridge passed embedded --once and real PTY launch/filter/exit. Source launch is documented in ui/README.md. The live binary was preserved. |
| Research | ui/README.md links finder.nvim, Awesome TUI, VisiData and Textual DataTable, with the implementation choice described. |

The final Python suite passed all 34 tests in /tmp/scope-finder-final-tests-2.log. The isolated build passed in /tmp/scope-finder-final-build.log. Final UI package bytes exactly match the isolated built source checkout. Scope hard audit and 21-cartridge isolation passed. Tests prove the requested functionality within documented bounds: ASP provider responses up to 256 results, disk content matches up to 10000, complete inline edit documents up to 64 KiB, previews up to 128 KiB, and session-local drafts. The implementation does not claim exhaustive provider inventories, durable editor drafts, physical-terminal frame benchmarks or memory processing status inference.

No required finder implementation work remains. Separate memory/runtime claims and unrelated working-tree changes were preserved. The handoff at /tmp/memory-stack-scope-readiness/owner-reply.md records the initial failed isolation probe and the corrected passing proof.
