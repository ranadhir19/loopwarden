"""Lab 02 tests: identical agent code, interchangeable models, and the
optional HTTP adapter proven against a local stub server (no internet)."""
import json
import os
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from harnesskit import make_workspace_tools, run_agent  # noqa: E402
from harnesskit.http_model import HttpModel  # noqa: E402
from solution import make_model  # noqa: E402

TASK = "Read notes.txt and report what it says"


def run_with(model):
    root = tempfile.mkdtemp(prefix="lab02_")
    reg = make_workspace_tools(root)
    reg.call("write_file", {"path": "notes.txt",
                            "content": "the quick brown fox jumps"})
    return run_agent(model, reg, TASK)


class TestSwappableModels(unittest.TestCase):
    def test_playback_model_completes(self):
        result = run_with(make_model("playback"))
        self.assertEqual(result.status, "completed")
        self.assertIn("quick brown fox", result.answer)

    def test_echo_model_completes_with_same_agent_code(self):
        result = run_with(make_model("echo"))
        self.assertEqual(result.status, "completed")
        self.assertIn("quick brown fox", result.answer)

    def test_both_models_agree(self):
        a = run_with(make_model("playback"))
        b = run_with(make_model("echo"))
        self.assertEqual(a.answer, b.answer)


class _StubHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(length)
        payload = {"choices": [{"message": {"content": json.dumps(
            {"type": "final", "text": "stub model answer"})}}]}
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class TestHttpAdapterAgainstLocalStub(unittest.TestCase):
    def test_adapter_parses_action_json(self):
        server = HTTPServer(("127.0.0.1", 0), _StubHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_address[1]}/v1/chat/completions"
            model = HttpModel(endpoint=url, api_key="test", model_name="stub")
            action = model.respond([{"role": "user", "content": "hi"}], ["read_file"])
            self.assertEqual(action, {"type": "final", "text": "stub model answer"})
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main(verbosity=2)
