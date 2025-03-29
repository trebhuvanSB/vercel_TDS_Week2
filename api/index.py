import json
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('./api/q-vercel-python.json', 'r') as file:
                data = json.load(file)

            query = self.path.split('?')[1] if '?' in self.path else ''
            params = parse_qs(query)

            # Extract names in the order they appear in the query
            names = params.get('name', [])

            # Convert data into a dictionary for quick lookup
            data_dict = {item['name']: item.get('marks', 0) for item in data}

            # Retrieve marks in the same order as names in the query
            marks_list = [data_dict.get(name, 0) for name in names]

            response = {"marks": marks_list}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
