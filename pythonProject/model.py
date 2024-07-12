# model.py
import requests
import json

class OwnCloudClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password


    def upload_task(self, task_data):
        url = f"{self.base_url}/remote.php/dav/files/{self.username}/tasks.json"
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers, data=json.dumps(task_data), auth=(self.username, self.password))
        return response.status_code == 201 or response.status_code == 204

    def download_tasks(self):
        url = f"{self.base_url}/remote.php/dav/files/{self.username}/tasks.json"
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return json.loads(response.content)
        return []

# Replace with your ownCloud credentials and URL
owncloud_client = OwnCloudClient("http://localhost/owncloud", "Matias", "PasswordOwncloud")
