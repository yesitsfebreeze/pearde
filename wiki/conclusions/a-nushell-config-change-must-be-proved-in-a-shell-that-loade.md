---
title: a-nushell-config-change-must-be-proved-in-a-shell-that-loade
date: 2026-09-02
type: conclusion
tags: [chezmoi, conclusion, nushell, verification]
sources:
  - "[[260902-6c05]]"
  - "[[260902-181d]]"
derived_from: []
---

# A nushell config change must be proved in a shell that loaded the config

`nu -c '<code>'` loads neither `env.nu` nor `config.nu`. A correct, deployed
config change therefore reports as ABSENT under it, and the false negative is
convincing because unrelated variables still answer — they are inherited from
the parent process, not read from `env.nu`.

Measured twice on nushell 0.115.1, independently, on 2026-09-02 (pass one, and
again on the implementer's re-run):

    nu -c 'print $env.PEARDE_AS?'   -> UNSET      (deployed and correct)
    nu -c 'pearde sweep --dry'      -> External command failed
    nu -c 'print $env.EDITOR?'      -> nvim       (inherited — looks loaded)
    nu --env-config ~/.config/nushell/env.nu \
       --config ~/.config/nushell/config.nu -c 'print $env.PEARDE_AS?'
                                    -> engineer

So "a familiar variable answers" is a test that passes when nothing loaded at
all. Two forms actually prove it: naming both config paths explicitly, or a
detached `tmux new-session -d -s probe nu` — the shell nobody handed a path
to — driven with `send-keys` and read with `capture-pane`. The second is the
stronger check: the first proves the FILES work, never that the shell you
actually get loads them.
