"""
Refactor.ai Backend Service.
Built with Python stdlib http.server for 100% zero-dependency, ultra-reliable execution.
Exposes standard REST endpoints:
- GET /health
- GET /api/config-status
- POST /api/refactor
"""
import sys
import os
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Ensure local backend imports resolve cleanly
sys.path.insert(0, os.path.dirname(__file__))

from config import Settings
from models import RefactorRequest, HealthResponse, ConfigStatusResponse, RefactorGoal, Language
from provider import ProviderAdapter

settings = Settings.load_from_env()
adapter = ProviderAdapter(settings)


class RefactorHTTPHandler(BaseHTTPRequestHandler):
    server_version = "RefactorMind/1.1"
    
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, x-goog-api-key")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send_json_response(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        
        if path in ("/health", "/api/health"):
            active = "gemini" if adapter.has_gemini else ("nebius-nvidia" if adapter.has_nebius else ("groq" if adapter.has_groq else "demo"))
            resp = HealthResponse(
                status="ok",
                version=settings.APP_VERSION,
                gemini_configured=adapter.has_gemini,
                gemini_model=settings.GEMINI_MODEL,
                nebius_configured=adapter.has_nebius,
                nebius_model=settings.NEBIUS_MODEL,
                groq_configured=adapter.has_groq,
                groq_model=settings.GROQ_MODEL,
                active_provider=active,
                demo_mode=not (adapter.has_gemini or adapter.has_nebius or adapter.has_groq)
            )
            self._send_json_response(200, resp.model_dump())
            return

        if path == "/api/config-status":
            resp = ConfigStatusResponse(
                version=settings.APP_VERSION,
                active_selection=settings.AI_PROVIDER,
                providers={
                    "gemini": {
                        "configured": adapter.has_gemini,
                        "model": settings.GEMINI_MODEL,
                        "role": "Primary Development Inference"
                    },
                    "nebius_nvidia": {
                        "configured": adapter.has_nebius,
                        "model": settings.NEBIUS_MODEL,
                        "base_url": settings.NEBIUS_BASE_URL,
                        "role": "Mandatory Hackathon Integration"
                    },
                    "groq": {
                        "configured": adapter.has_groq,
                        "model": settings.GROQ_MODEL,
                        "role": "Secondary Fallback"
                    }
                }
            )
            self._send_json_response(200, resp.model_dump())
            return
            
        self._send_json_response(404, {"error": "Not Found", "path": self.path})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        
        if path in ("/api/refactor", "/refactor"):
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 500000:
                self._send_json_response(413, {"error": "Payload too large. Maximum size is 500KB."})
                return
                
            raw_body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(raw_body)
            except Exception as e:
                self._send_json_response(400, {"error": "Invalid JSON format", "detail": str(e)})
                return
                
            # Input validation
            code = data.get("code", "")
            if not isinstance(code, str) or len(code.strip()) < 5:
                self._send_json_response(422, {"error": "Validation Error", "detail": "Field 'code' must contain at least 5 characters."})
                return
                
            if len(code) > settings.MAX_CODE_LENGTH:
                self._send_json_response(422, {"error": "Validation Error", "detail": f"Field 'code' exceeds maximum limit of {settings.MAX_CODE_LENGTH} characters."})
                return

            goal_str = data.get("goal", "readability")
            try:
                goal = RefactorGoal(goal_str)
            except ValueError:
                self._send_json_response(422, {"error": "Validation Error", "detail": f"Invalid goal '{goal_str}'. Supported goals: {[g.value for g in RefactorGoal]}"})
                return

            lang_str = data.get("language", "auto")
            try:
                lang = Language(lang_str)
            except ValueError:
                lang = Language.AUTO

            req = RefactorRequest(
                code=code,
                goal=goal,
                language=lang,
                context=data.get("context")
            )

            try:
                res = adapter.refactor(req)
                self._send_json_response(200, res.model_dump())
            except Exception as e:
                self._send_json_response(500, {"error": "Refactoring processing error", "detail": str(e)})
            return
            
        self._send_json_response(404, {"error": "Not Found", "path": self.path})

    
def log_message(self, format, *args):
    # Log HTTP requests without exposing request bodies or credentials.
    try:
        message = format % args
    except (TypeError, ValueError):
        message = format

    sys.stderr.write(
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"
    )



def run(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), RefactorHTTPHandler)
    print(f"==================================================")
    print(f"Refactor.ai Backend Service Running on http://{host}:{port}")
    print(f"Endpoints:")
    print(f"  GET  http://localhost:{port}/health")
    print(f"  GET  http://localhost:{port}/api/config-status")
    print(f"  POST http://localhost:{port}/api/refactor")
    print(f"Gemini Key Configured: {adapter.has_gemini}")
    print(f"Nebius Key Configured: {adapter.has_nebius}")
    print(f"Groq Key Configured:   {adapter.has_groq}")
    print(f"==================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else settings.PORT
    run(host=settings.HOST, port=port)
