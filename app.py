import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


notes = []


class NotesHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "message": "Notes API is running",
                "endpoints": ["/healthz", "/notes"]
            })

        elif self.path == "/healthz":
            self.send_json(200, {"status": "ok"})

        elif self.path == "/notes":
            self.send_json(200, {"notes": notes})

        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/notes":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))

            if not isinstance(data, dict) or not isinstance(data.get("text"), str):
                self.send_json(400, {"error": "A text field is required"})
                return

            note = {"id": len(notes) + 1, "text": data["text"]}
            notes.append(note)
            self.send_json(201, note)

        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid JSON"})

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), NotesHandler)
    print(f"Notes API listening on port {port}", flush=True)
    server.serve_forever()

# minor change
