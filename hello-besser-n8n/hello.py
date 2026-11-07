"""Run the BESSER hello world and send the greeting to the backend.

Default backend: the local stand-in in stand_in.py.
Real n8n: set N8N_WEBHOOK_URL to the published webhook. See README.md.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

from model import GREETING_TEXT, generate
from stand_in import WEBHOOK_PATH, start

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode())


def load_greeting():
    sys.path.insert(0, str(ROOT))
    for name in ("output.classes", "output"):
        sys.modules.pop(name, None)
    importlib.invalidate_caches()
    classes = importlib.import_module("output.classes")
    return classes.Greeting


def main() -> int:
    model = generate(OUTPUT)
    Greeting = load_greeting()
    greeting = Greeting(text=GREETING_TEXT)

    webhook = os.environ.get("N8N_WEBHOOK_URL", "").strip()
    server = None
    if not webhook:
        port = int(os.environ.get("STAND_IN_PORT", "8787"))
        server = start(port=port)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        webhook = f"http://127.0.0.1:{port}{WEBHOOK_PATH}"

    print(f"BESSER model: {model.name}")
    print(f"generated: {OUTPUT / 'classes.py'}")
    print(f"Greeting.text: {greeting.text}")
    print(f"POST {webhook}")

    try:
        reply = post_json(webhook, {"text": greeting.text})
    except urllib.error.URLError as error:
        print(f"backend did not answer: {error.reason}")
        print("If this URL is n8n, start n8n, import n8n/hello-workflow.json, and publish it.")
        return 1
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()

    print(f"reply: {json.dumps(reply)}")
    if reply.get("text") != greeting.text:
        print("reply text does not match the BESSER greeting")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
