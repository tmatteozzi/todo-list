from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import unquote
import requests

class OwnCloudClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def upload_tasks(self, tasks):
        url = f"{self.base_url}/remote.php/dav/files/{self.username}/tasks.json"
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers, data=json.dumps(tasks), auth=(self.username, self.password))
        return response.status_code == 201 or response.status_code == 204

    def download_tasks(self):
        url = f"{self.base_url}/remote.php/dav/files/{self.username}/tasks.json"
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return json.loads(response.content)
        return []

    def authenticate(self, username, password):
        url = f"{self.base_url}/status.php"
        response = requests.get(url, auth=(username, password))
        return response.status_code == 200

owncloud_client = OwnCloudClient("http://localhost/owncloud", "Matias", "PasswordOwncloud")

class ModelHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/tasks':
            tasks = owncloud_client.download_tasks()
            self._set_headers()
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        elif self.path == '/authenticate':
            self.authenticate_user()
        else:
            self.send_response(404)
            self.end_headers()

    def authenticate_user(self):
        username = self.headers.get('username')
        password = self.headers.get('password')
        if owncloud_client.authenticate(username, password):
            self._set_headers()
            self.wfile.write(json.dumps({'status': 'authenticated'}).encode('utf-8'))
        else:
            self.send_response(401)
            self.end_headers()

    def do_POST(self):
        if self.path == '/add_task':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)

            task = {
                'task': task_data['task'],
                'description': task_data['description'],
                'completed': task_data.get('completed', False)
            }

            tasks = owncloud_client.download_tasks()
            tasks.append(task)
            owncloud_client.upload_tasks(tasks)

            self._set_headers()
            self.wfile.write(json.dumps(task).encode('utf-8'))

    def do_DELETE(self):
        if self.path == '/delete_task':
            content_length = int(self.headers['Content-Length'])
            delete_data = self.rfile.read(content_length)
            task_data = json.loads(delete_data)

            tasks = owncloud_client.download_tasks()
            task_found = False
            for task in tasks:
                if task['task'] == task_data['task']:
                    tasks.remove(task)
                    task_found = True
                    break

            if task_found:
                owncloud_client.upload_tasks(tasks)
                self._set_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    def do_PUT(self):
        if self.path == '/update_task':
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_task = json.loads(put_data)

            tasks = owncloud_client.download_tasks()
            task_found = False
            for task in tasks:
                if task['task'] == updated_task['task']:
                    task['completed'] = updated_task.get('completed

