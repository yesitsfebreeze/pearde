#!/usr/bin/env python3
"""A daemon that is not the daemon — one socket on PEARDE_PORT answering in
the four shapes `post_report`'s `except` tuple does not name.

`post_report` guards `urllib.error.URLError, OSError, ValueError`. A live
listener that is not this board's daemon answers outside that set:

  garbage   non-HTTP bytes on the wire      -> http.client.BadStatusLine
  truncate  Content-Length longer than body -> http.client.IncompleteRead
  list      a JSON body that is not a dict  -> AttributeError on .get
  entry     a `boards` row with no `path`   -> KeyError

Each is a real thing a port holds: another service on 8443, a daemon killed
mid-write, an older or newer /status shape. Usage:

    python3 stub_daemon.py <mode> [port]      # prints the port, then serves

Serves forever; the caller kills it.
"""
import json
import socket
import sys
import threading

MODES = ("garbage", "truncate", "list", "entry", "ok")


def body_for(mode, path, board_path):
    if mode == "list":
        return json.dumps([]).encode()
    if mode == "entry":
        return json.dumps({"boards": [{"name": "b"}]}).encode()
    return json.dumps({"boards": [{"name": "b", "path": board_path}]}).encode()


def serve(sock, mode, board_path):
    while True:
        try:
            conn, _ = sock.accept()
        except OSError:
            return
        threading.Thread(target=handle, args=(conn, mode, board_path),
                         daemon=True).start()


def handle(conn, mode, board_path):
    try:
        conn.settimeout(5)
        try:
            req = conn.recv(65536).decode("utf-8", "replace")
        except OSError:
            req = ""
        path = (req.split(" ") + ["", ""])[1]
        if mode == "garbage":
            # what a TLS listener, or anything not speaking HTTP, puts on the
            # wire when a plaintext GET arrives
            conn.sendall(b"\x15\x03\x01\x00\x02\x02\x28not http at all\r\n")
            return
        payload = body_for(mode, path, board_path)
        if mode == "truncate" and path.startswith("/report"):
            # headers promise a body, the process dies before writing it
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 4096\r\n\r\n"
                         b"{")
            return
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                     + f"Content-Length: {len(payload)}\r\n\r\n".encode()
                     + payload)
    finally:
        try:
            conn.close()
        except OSError:
            pass


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        print(f"usage: stub_daemon.py {'|'.join(MODES)} [board-path]",
              file=sys.stderr)
        return 2
    mode = sys.argv[1]
    board_path = sys.argv[2] if len(sys.argv) > 2 else "/nowhere"
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 0))
    sock.listen(16)
    print(sock.getsockname()[1], flush=True)
    serve(sock, mode, board_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
