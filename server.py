import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.trip_planner import build_trip_plan, compare_scenarios

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / 'static'


class TravelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/trip-plan':
            params = parse_qs(parsed.query)
            interests = params.get('interests', ['culture,food'])
            interest_list = [item.strip() for item in interests[0].split(',') if item.strip()]
            payload = build_trip_plan(
                destination=params.get('destination', ['Rome'])[0],
                days=int(params.get('days', ['3'])[0]),
                budget=float(params.get('budget', ['1800'])[0]),
                travellers=int(params.get('travellers', ['2'])[0]),
                interests=interest_list,
                pace=params.get('pace', ['balanced'])[0],
                weather=params.get('weather', ['sunny'])[0],
                scenario=params.get('scenario', ['comfort'])[0],
            )
            self._send_json(payload)
            return

        if path == '/api/scenarios':
            params = parse_qs(parsed.query)
            interests = params.get('interests', ['culture,food'])
            interest_list = [item.strip() for item in interests[0].split(',') if item.strip()]
            payload = compare_scenarios(
                destination=params.get('destination', ['Rome'])[0],
                budget=float(params.get('budget', ['1800'])[0]),
                days=int(params.get('days', ['3'])[0]),
                travellers=int(params.get('travellers', ['2'])[0]),
                interests=interest_list,
                pace=params.get('pace', ['balanced'])[0],
                weather=params.get('weather', ['sunny'])[0],
            )
            self._send_json(payload)
            return

        file_path = self._resolve_static_path(path)
        if file_path is not None:
            self._send_file(file_path)
            return

        self.send_response(404)
        self.end_headers()

    def _resolve_static_path(self, request_path: str):
        if request_path in ('', '/'):
            return STATIC_DIR / 'index.html'
        candidate = STATIC_DIR / request_path.lstrip('/')
        if candidate.exists() and candidate.is_file():
            return candidate
        return None

    def _send_file(self, file_path: Path):
        content = file_path.read_bytes()
        mime_type = 'text/html' if file_path.suffix.lower() in {'.html'} else 'text/css' if file_path.suffix.lower() in {'.css'} else 'application/javascript' if file_path.suffix.lower() in {'.js'} else 'application/octet-stream'
        self.send_response(200)
        self.send_header('Content-Type', mime_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 3000), TravelHandler)
    print('TripMind AI is running at http://127.0.0.1:3000')
    server.serve_forever()
