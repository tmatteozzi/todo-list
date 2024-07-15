from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from socketserver import ThreadingMixIn

MODEL_SERVER_URL = "http://192.168.68.55:2004"

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
        response = requests.get(f"{MODEL_SERVER_URL}/tasks")
        tasks = response.json()
        self._set_headers("application/json")
        self.wfile.write(json.dumps(tasks).encode('utf-8'))

    def do_POST(self):
        if self.path == '/add_task':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)

            response = requests.post(f"{MODEL_SERVER_URL}/add_task", json=task_data)
            self._set_headers("application/json")
            self.wfile.write(response.content)

    def do_DELETE(self):
        if self.path == '/delete_task':
            content_length = int(self.headers['Content-Length'])
            delete_data = self.rfile.read(content_length)
            task_data = json.loads(delete_data)

            response = requests.delete(f"{MODEL_SERVER_URL}/delete_task", json=task_data)
            self._set_headers("application/json")
            self.wfile.write(response.content)

    def do_PUT(self):
        if self.path == '/update_task':
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            task_data = json.loads(put_data)

            response = requests.put(f"{MODEL_SERVER_URL}/update_task", json=task_data)
            self._set_headers("application/json")
            self.wfile.write(response.content)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run(server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
