from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

class OwnCloudClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload_tasks(self, tasks, username, password):
        url = f"{self.base_url}/remote.php/dav/files/{username}/tasks.json"
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers, data=json.dumps(tasks), auth=(username, password))
        return response.status_code == 201 or response.status_code == 204

    def download_tasks(self, username, password):
        url = f"{self.base_url}/remote.php/dav/files/{username}/tasks.json"
        response = requests.get(url, auth=(username, password))
        if response.status_code == 200:
            return json.loads(response.content)
        return []

    def authenticate(self, username, password):
        url = f"{self.base_url}/remote.php/dav/files/{username}/"
        response = requests.request('PROPFIND', url, auth=(username, password))
        print(f"Authentication response: {response.status_code} {response.text}")
        return response.status_code == 207

owncloud_client = OwnCloudClient("http://localhost/owncloud")

class ModelHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
        self.wfile.write(b"405 Method Not Allowed")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        username = data.get('username')
        password = data.get('password')

        if self.path == '/login':
            if owncloud_client.authenticate(username, password):
                self._set_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                print(f"Authentication failed for user {username}")
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
        elif self.path == '/tasks':
            tasks = owncloud_client.download_tasks(username, password)
            self._set_headers()
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        elif self.path == '/add_task':
            task_data = data
            task = {
                'task': task_data['task'],
                'description': task_data['description'],
                'completed': task_data.get('completed', False)
            }

            tasks = owncloud_client.download_tasks(username, password)
            tasks.append(task)
            owncloud_client.upload_tasks(tasks, username, password)

            self._set_headers()
            self.wfile.write(json.dumps(task).encode('utf-8'))
        elif self.path == '/delete_task':
            task_data = data

            tasks = owncloud_client.download_tasks(username, password)
            task_found = False
            for task in tasks:
                if task['task'] == task_data['task']:
                    tasks.remove(task)
                    task_found = True
                    break

            if task_found:
                owncloud_client.upload_tasks(tasks, username, password)
                self._set_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        elif self.path == '/update_task':
            updated_task = data

            tasks = owncloud_client.download_tasks(username, password)
            task_found = False
            for task in tasks:
                if task['task'] == updated_task['task']:
                    task['completed'] = updated_task.get('completed', task['completed'])
                    task_found = True
                    break
                elif task['task'] == updated_task.get('old_task'):
                    task['task'] = updated_task['task']
                    task['description'] = updated_task['description']
                    task_found = True
                    break

            if task_found:
                owncloud_client.upload_tasks(tasks, username, password)
                self._set_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

def run(server_class=HTTPServer, handler_class=ModelHTTPRequestHandler, port=2004):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting model server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
