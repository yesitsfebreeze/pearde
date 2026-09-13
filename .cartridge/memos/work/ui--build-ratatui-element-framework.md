---
kind: work
description: Build a reusable Ratatui library of terminal UI elements before defining a default surface
status: done
needs:
  - "[[tui-is-a-ratatui-element-framework]]"
---

## Outcome

Deliver a reusable Ratatui terminal UI framework containing messages, multiline
inputs, loaders, and popups that consumers can compose into their own surfaces.
This is the user's next priority. Follow [[tui-is-a-ratatui-element-framework]].
The default application surface is separate future work.

## Check

- [x] Consumers can import and compose the framework as a Rust library using Ratatui.
- [x] Message display, multiline input, loaders, and popups expose reusable
  rendering and interaction state without requiring agent or session services.
- [x] Consumers control layout, styles, bindings, and application actions.
- [x] Session, agent, and approval orchestration is separated from the framework;
  the library owns no fixed conversation flow or application layout.
- [x] Small component examples demonstrate composition without defining a default surface.
- [x] Buffer tests cover rendering at small sizes; interaction tests cover Unicode
  multiline editing, popup focus/dismissal, and caller-driven loader updates.
- [x] Relevant tests and repository checks pass, with results recorded here.

## Approach

Start at builtin/tui: main.rs owns conversation orchestration, editor.rs owns
custom terminal editing/rendering, and cartridge.rs owns service and terminal
lifecycle. Establish the library/application boundary before extracting elements.
Use Ratatui for rendering and keep element events independent of service calls.
Preserve existing behavior in a separate consumer as needed during migration.
Do not choose the future default surface in this work.

## Result

Implemented on 2026-09-10. `builtin/tui` is a Ratatui library exposing Message,
Input/InputState/InputAction, Loader/LoaderState, and Popup/PopupState/PopupAction.
Consumers own areas, styles, bindings, event routing, application actions, and
terminal lifecycle. Input editing respects grapheme clusters and display columns;
loaders advance only on caller-supplied time; popup state cycles local focus and
returns the previous focus on dismissal.

The former cartridge moved to `builtin/tui-surface`, which consumes the library's
input state and Ratatui widgets/backend. Its binary and service stay named `tui`.
The default profile and bundle manifest resolve that consumer, preserving
`just run`. No future default surface was defined.

Verification:
- `cargo test -p tui -p tui-surface`: 10 component tests and 17 consumer tests passed.
- `cargo run -p tui --example elements`: rendered the headless component gallery.
- Dependency inspection: the library has no cartridge, Tokio, agent, session, router,
  or harness dependency.
- `cargo build --workspace`: passed.
- `target/debug/cartridge list`: resolved `tui` from `tui-surface` with its existing injections.
- `NEXTEST_TEST_THREADS=2 just all`: formatting and Clippy passed; 210 workspace
  tests, one documentation example, and six Python tests passed.
- `git diff --check`: passed.

The initial gate encountered disk exhaustion while linking. Removed regenerable
local debug-symbol archives and older debug-symbol bundles; the subsequent full
gate passed. Changes remain uncommitted in the working tree.
