---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "2h"
actual: "30m"
---

# The LSP query every session is told to ask before opening a file returns `unavailable: timeout`, while sixteen rust-analyzer processes from three editor sessions are alive and one has held 98% of a core since 01:56.

**Done 2026-09-08** — the measurement landed as
[[the-lsp-timeout-is-not-the-index]] and [[an-empty-lsp-answer-is-not-a-no]].
Two of the three candidate conditions are excluded by the error message itself
and the third, a merely indexing server, by a clean single-analyzer control that
answered `index_status` in under 0.1 s on 46 polls across 15 minutes; only a
starved or wedged attached server survives, unreproduced. **Nothing was killed:** at 16:23:14, before this
run touched anything, `pgrep -f rust-analyzer | wc -l` printed 0, `just terminal
status` showed `panes: {}`, and no `nvim.sock` or `nvim` process existed — the
sixteen analyzers and the editor that owned them were already gone, so no
process could be placed as orphaned. The kill authorized by
[[approve-lsp-timeout-investigation]] stays unspent.

## Do

Approved 2026-09-08 as "Approve + allow killing orphans" [[approve-lsp-timeout-investigation]]. The measurement below is authorized, and so is killing the rust-analyzer processes it identifies as orphaned — each one placed by evidence first, and nothing killed that cannot be placed.

Observed defect, measured 2026-09-08 at 11:05 in `/Users/feb/dev/memory` on macOS 25.2.0, code revision `36d6def6`, inside the shared tmux session. [[SYSTEM]] tells every session to use [[terminal]] "for every session's own reads: ask the warm LSP before opening a file whole". The pane integration itself works: `just terminal status` answered with the socket and both pane ids, and `just terminal nvim '{"op":"capabilities"}'` returned the installed command list. But `{"op":"query","method":"index_status","path":"/Users/feb/dev/memory/src/commands/src/commands_mcp.rs"}` answered `{"error": "...neovim-control.lua:233: unavailable: ...neovim-control.lua:26: timeout"}`. `Lsp.index_status` (`memos/system/neovim-control.md:159`) exists to say whether asking is worth trying yet, and it is the call that timed out.

Beside it, and not established as its cause: `pgrep -f rust-analyzer | wc -l` printed 16, spanning three editor generations — instances started 01:56, 02:20 and 09:31 — and pid 56689 from 01:56 was holding 98.1% CPU and 146 MB at the time of the query. This repeats a pattern already known on this machine, orphaned language servers outliving the editor that started them.

Proposed scope: measure only. Re-run the `index_status` query and one `document_symbols` query against the same absolute path, read which server the current Neovim actually has attached (`vim.lsp.get_clients` through the `lua` op), and establish whether the timeout comes from the attached server still indexing, from the attached server being one of the wedged older instances, or from the pane owner being held. Land the finding as one memo. Then kill the analyzer processes that measurement places as orphaned — belonging to no living editor — and no others: identification is the whole risk, and a process that cannot be placed is left alone and named in the finding.

Benefit: two instructions every session carries — ask the LSP first, and fall back only with a reason — currently resolve to the fallback every time, so every session reads whole files it was told not to, and a core has been burning for nine hours. Tradeoff: a kill is destructive, and a process misidentified as orphaned is a live editor losing its language server. Preserve what works: `just terminal status`, `capabilities`, and the claim/release protocol all answer correctly and must keep answering; [[terminal]]'s rule that a timeout is not proof of no references stays exactly as written — this item does not propose weakening the fallback, only finding out why it is always taken.

## Acceptance
Already run, 2026-09-08: `just terminal status` returned the socket and panes `%2`/`%3` with an empty owner; `capabilities` returned the command list; `index_status` with no path returned `absolute path required`, and with an absolute path returned `unavailable: ... timeout`; `pgrep -f rust-analyzer | wc -l` printed 16, with pid 56689 at 98.1% CPU since 01:56.

Unrun: the identity of the server Neovim has attached for that buffer, and a statement of which of the three candidate conditions the timeout follows from. Then, after the kills: `index_status` on an absolute path answers rather than timing out, `pgrep -f rust-analyzer | wc -l` is reported before and after, and every process killed is listed with the evidence that placed it as orphaned.

Run `just memos-check` once after the finding memo lands and require success. The gate does not see the editor; the query observation above is required.
