from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from model import owncloud_client

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
        tasks = owncloud_client.download_tasks()
        self._set_headers("application/json")
        self.wfile.write(json.dumps(tasks).encode('utf-8'))

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
            owncloud_client.upload_task(tasks)

            self._set_headers("application/json")
            self.wfile.write(json.dumps(task).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/delete_task'):
            task_id = self.path.split('/')[-1]
            tasks = owncloud_client.download_tasks()
            task_found = False
            for task in tasks:
                if task['task'] == task_id:
                    tasks.remove(task)
                    task_found = True
                    break
            
            if task_found:
                owncloud_client.upload_task(tasks)
                self._set_headers("application/json")
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    def do_PUT(self):
        if self.path.startswith('/update_task'):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_task = json.loads(put_data)

            task_id = self.path.split('/')[-1]
            tasks = owncloud_client.download_tasks()
            task_found = False
            for task in tasks:
                if task['task'] == task_id:
                    task['completed'] = updated_task.get('completed', task['completed'])
                    task_found = True
                    break
            
            if task_found:
                owncloud_client.upload_task(tasks)
                self._set_headers("application/json")
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
