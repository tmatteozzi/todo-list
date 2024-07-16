from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
import jwt
import time

MODEL_SERVER_URL = "http://192.168.68.55:2004"
SECRET_KEY = "your_secret_key"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.serve_html()
        elif self.path == '/tasks':
            self.serve_tasks()
        else:
            self.send_response(404)
            self.end_headers()

    def serve_html(self):
        html_file_path = "index.html"
        try:
            with open(html_file_path, 'rb') as file:
                self._set_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def serve_tasks(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            self.send_response(401)
            self.end_headers()
            return

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            response = requests.get(f"{MODEL_SERVER_URL}/tasks")
            tasks = response.json()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        except jwt.ExpiredSignatureError:
            self.send_response(401)
            self.end_headers()
        except jwt.InvalidTokenError:
            self.send_response(401)
            self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            credentials = json.loads(post_data)

            if self.authenticate(credentials['username'], credentials['password']):
                token = jwt.encode({
                    'username': credentials['username'],
                    'exp': time.time() + 3600  # Token expira en 1 hora
                }, SECRET_KEY, algorithm="HS256")

                self._set_headers("application/json")
                self.wfile.write(json.dumps({'token': token}).encode('utf-8'))
            else:
                self.send_response(401)
                self.end_headers()
        elif self.path == '/add_task':
            self.handle_authorized_request(self.add_task)
        elif self.path == '/delete_task':
            self.handle_authorized_request(self.delete_task)
        elif self.path == '/update_task':
            self.handle_authorized_request(self.update_task)

    def handle_authorized_request(self, handler):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            self.send_response(401)
            self.end_headers()
            return

        token = auth_header.split(' ')[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            handler()
        except jwt.ExpiredSignatureError:
            self.send_response(401)
            self.end_headers()
        except jwt.InvalidTokenError:
            self.send_response(401)
            self.end_headers()

    def authenticate(self, username, password):
        response = requests.get(f"{MODEL_SERVER_URL}/authenticate", auth=(username, password))
        return response.status_code == 200

    def add_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        task_data = json.loads(post_data)

        response = requests.post(f"{MODEL_SERVER_URL}/add_task", json=task_data)
        if response.status_code == 200:
            self._set_headers("application/json")
            self.wfile.write(response.content)
        else:
            self.send_response(response.status_code)
            self.end_headers()

    def delete_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        task_data = json.loads(post_data)

        response = requests.post(f"{MODEL_SERVER_URL}/delete_task", json=task_data)
        if response.status_code == 200:
            self._set_headers("application/json")
            self.wfile.write(response.content)
        else:
            self.send_response(response.status_code)
            self.end_headers()

    def update_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        task_data = json.loads(post_data)

        response = requests.post(f"{MODEL_SERVER_URL}/update_task", json=task_data)
        if response.status_code == 200:
            self._set_headers("application/json")
            self.wfile.write(response.content)
        else:
            self.send_response(response.status_code)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(server_class=ThreadedHTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
