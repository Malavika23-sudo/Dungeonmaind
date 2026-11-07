"""Local stand-in for the n8n hello webhook.

Same request and response as n8n/hello-workflow.json, except the
source field is local-stand-in. It is not n8n.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

WEBHOOK_PATH = "/webhook/hello"
SOURCE = "local-stand-in"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path.split("?", 1)[0] != WEBHOOK_PATH:
            self._send(404, {"source": SOURCE, "error": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            self._send(400, {"source": SOURCE, "error": "body must be JSON"})
            return
        text = payload.get("text", "")
        self._send(200, {"source": SOURCE, "text": text})

    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def start(host: str = "127.0.0.1", port: int = 8787) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)
