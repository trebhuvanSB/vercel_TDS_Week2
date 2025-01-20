import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('q-vercel-python.json', 'r') as file:
                data = json.load(file)

            query = self.path.split('?')[1] if '?' in self.path else ''
            params = {key: value for key, value in [param.split('=') for param in query.split('&') if '=' in param]}

            names = params.get('name', '').split(',') if 'name' in params else []

            results = [item for item in data if item['name'] in names]
            response = {"results": results}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
