#!/usr/bin/env python3
"""Run a collect with `post_report` replaced by a raise.

The stub daemon proves the four shapes the `except` tuple misses today. This
proves the general case: whatever is put between the done write and the
commit, the record has to come back. Usage:

    python3 inject.py <collect.py> <exception-class> -- <collect argv…>

Exits with collect's own code, or 99 when the injected error escaped the
process as a traceback.
"""
import importlib.util
import sys


def load(path):
    spec = importlib.util.spec_from_file_location("collect_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["collect_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    collect_py, exc_name = sys.argv[1], sys.argv[2]
    argv = sys.argv[sys.argv.index("--") + 1:]
    mod = load(collect_py)
    exc = getattr(__builtins__, exc_name, None) \
        if not isinstance(__builtins__, dict) else __builtins__.get(exc_name)
    if exc is None:
        exc = RuntimeError

    def boom(*_a, **_k):
        raise exc("injected — post_report blew up")

    mod.post_report = boom
    try:
        return mod.cmd_collect(argv)
    except SystemExit as e:
        return int(e.code or 0)
    except BaseException:                      # the escape this probe measures
        import traceback
        traceback.print_exc()
        return 99


if __name__ == "__main__":
    sys.exit(main())
