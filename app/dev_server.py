"""Zero-dependency local demo server.

The production entrypoint is FastAPI. This server keeps the judging demo
runnable before cloud dependencies or credentials are installed.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .engine import build_approval_queue, sample_opportunities
from .models import ApplicantProfile


ROOT = Path(__file__).resolve().parent.parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802 - stdlib handler API
        if self.path == "/":
            self.path = "/static/index.html"
        if self.path == "/health":
            return self._json({"status": "ok", "mode": "approval-first"})
        return super().do_GET()

    def do_POST(self):  # noqa: N802 - stdlib handler API
        if self.path != "/api/queue":
            self.send_error(404)
            return

        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        profile = ApplicantProfile(
            country=payload.get("country", "Denmark"),
            is_adult=bool(payload.get("is_adult", True)),
            works_solo=bool(payload.get("works_solo", True)),
            attributes={
                "internet_access": bool(payload.get("internet_access", True)),
                "verified_student": bool(payload.get("verified_student", False)),
            },
            evidence={},
        )
        self._json(
            {
                "items": [
                    asdict(item)
                    for item in build_approval_queue(profile, sample_opportunities())
                ]
            }
        )

    def _json(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("PrizePilot Agent running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()

