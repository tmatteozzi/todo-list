from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from socketserver import ThreadingMixIn

MODEL_SERVER_URL = "http://192.168.68.55:2004"
session = {"logged_in": False, "username": "", "password": ""}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.serve_html()
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

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            credentials = json.loads(post_data)

            response = requests.post(f"{MODEL_SERVER_URL}/login", json=credentials)
            if response.status_code == 200:
                session["logged_in"] = True
                session["username"] = credentials["username"]
                session["password"] = credentials["password"]
                self._set_headers("application/json")
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            else:
                print(f"Login failed: {response.status_code} {response.text}")
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")

        elif self.path == '/tasks':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            response = requests.post(f"{MODEL_SERVER_URL}/tasks", json={"username": session["username"], "password": session["password"]})
            if response.status_code == 200:
                tasks = response.json()
                self._set_headers("application/json")
                self.wfile.write(json.dumps(tasks).encode('utf-8'))
            else:
                print(f"Failed to retrieve tasks: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

        elif self.path == '/add_task':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)
            task_data.update({"username": session["username"], "password": session["password"]})

            response = requests.post(f"{MODEL_SERVER_URL}/add_task", json=task_data)
            if response.status_code == 200:
                self._set_headers("application/json")
                self.wfile.write(response.content)
            else:
                print(f"Failed to add task: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

        elif self.path == '/delete_task':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            content_length = int(self.headers['Content-Length'])
            delete_data = self.rfile.read(content_length)
            task_data = json.loads(delete_data)
            task_data.update({"username": session["username"], "password": session["password"]})

            response = requests.post(f"{MODEL_SERVER_URL}/delete_task", json=task_data)
            if response.status_code == 200:
                self._set_headers("application/json")
                self.wfile.write(response.content)
            else:
                print(f"Failed to delete task: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

        elif self.path == '/update_task':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            task_data = json.loads(put_data)
            task_data.update({"username": session["username"], "password": session["password"]})

            response = requests.post(f"{MODEL_SERVER_URL}/update_task", json=task_data)
            if response.status_code == 200:
                self._set_headers("application/json")
                self.wfile.write(response.content)
            else:
                print(f"Failed to update task: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run(server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from socketserver import ThreadingMixIn

MODEL_SERVER_URL = "http://192.168.68.55:2004"
session = {"logged_in": False, "username": "", "password": ""}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.serve_html()
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

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            credentials = json.loads(post_data)

            response = requests.post(f"{MODEL_SERVER_URL}/login", json=credentials)
            if response.status_code == 200:
                session["logged_in"] = True
                session["username"] = credentials["username"]
                session["password"] = credentials["password"]
                self._set_headers("application/json")
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            else:
                print(f"Login failed: {response.status_code} {response.text}")
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")

        elif self.path == '/tasks':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            response = requests.post(f"{MODEL_SERVER_URL}/tasks", json={"username": session["username"], "password": session["password"]})
            if response.status_code == 200:
                tasks = response.json()
                self._set_headers("application/json")
                self.wfile.write(json.dumps(tasks).encode('utf-8'))
            else:
                print(f"Failed to retrieve tasks: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

        elif self.path == '/add_task':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)
            task_data.update({"username": session["username"], "password": session["password"]})

            response = requests.post(f"{MODEL_SERVER_URL}/add_task", json=task_data)
            if response.status_code == 200:
                self._set_headers("application/json")
                self.wfile.write(response.content)
            else:
                print(f"Failed to add task: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

        elif self.path == '/delete_task':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            content_length = int(self.headers['Content-Length'])
            delete_data = self.rfile.read(content_length)
            task_data = json.loads(delete_data)
            task_data.update({"username": session["username"], "password": session["password"]})

            response = requests.post(f"{MODEL_SERVER_URL}/delete_task", json=task_data)
            if response.status_code == 200:
                self._set_headers("application/json")
                self.wfile.write(response.content)
            else:
                print(f"Failed to delete task: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

        elif self.path == '/update_task':
            if not session["logged_in"]:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                return

            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            task_data = json.loads(put_data)
            task_data.update({"username": session["username"], "password": session["password"]})

            response = requests.post(f"{MODEL_SERVER_URL}/update_task", json=task_data)
            if response.status_code == 200:
                self._set_headers("application/json")
                self.wfile.write(response.content)
            else:
                print(f"Failed to update task: {response.status_code} {response.text}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run(server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
