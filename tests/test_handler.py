"""
In-process Mock Client to test RefactorHTTPHandler end-to-end without socket networking.
Tests the exact HTTP request handling, serialization, status codes, and headers.
"""
import sys
import os
import unittest
import json
from io import BytesIO

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, BACKEND_DIR)

from main import RefactorHTTPHandler, settings


class DummyServer:
    pass


class MockHTTPHandler(RefactorHTTPHandler):
    def __init__(self, method: str, path: str, body: dict = None):
        self.rfile = BytesIO(json.dumps(body).encode("utf-8") if body else b"")
        self.wfile = BytesIO()
        self.command = method
        self.path = path
        self.requestline = f"{method} {path} HTTP/1.1"
        self.request_version = "HTTP/1.1"
        self.headers = {
            "Content-Length": str(len(self.rfile.getvalue())),
            "Content-Type": "application/json"
        }
        self.server = DummyServer()
        self.close_connection = True
        
        # Dispatch
        if method == "GET":
            self.do_GET()
        elif method == "POST":
            self.do_POST()
        elif method == "OPTIONS":
            self.do_OPTIONS()

    def get_response_body(self):
        val = self.wfile.getvalue().decode("utf-8")
        parts = val.split("\r\n\r\n", 1)
        if len(parts) > 1:
            return json.loads(parts[1])
        return {}


class TestHandlerDirect(unittest.TestCase):
    def test_health_route(self):
        handler = MockHTTPHandler("GET", "/health")
        data = handler.get_response_body()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("gemini_model"), settings.GEMINI_MODEL)
        self.assertEqual(data.get("nebius_model"), settings.NEBIUS_MODEL)
        self.assertIn("active_provider", data)

    def test_config_status_route(self):
        handler = MockHTTPHandler("GET", "/api/config-status")
        data = handler.get_response_body()
        self.assertIn("providers", data)
        self.assertIn("gemini", data["providers"])
        self.assertIn("nebius_nvidia", data["providers"])
        self.assertEqual(data["providers"]["gemini"]["model"], settings.GEMINI_MODEL)

    def test_refactor_post_validation(self):
        handler = MockHTTPHandler("POST", "/api/refactor", {"code": "bad"})
        data = handler.get_response_body()
        self.assertIn("Validation Error", data.get("error", ""))

    def test_refactor_post_success(self):
        sample = {
            "code": "def process(x, y): return x + y",
            "goal": "readability",
            "language": "python"
        }
        handler = MockHTTPHandler("POST", "/api/refactor", sample)
        data = handler.get_response_body()
        self.assertEqual(data.get("goal"), "readability")
        self.assertIn("refactored_code", data)
        self.assertIsInstance(data.get("explanations"), list)
        self.assertGreater(len(data.get("explanations")), 0)


if __name__ == "__main__":
    unittest.main()
