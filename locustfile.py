from locust import HttpUser, task
from requests.auth import HTTPBasicAuth
from pathlib import Path
import random

Path("output.txt").write_text("_________________________________________________\n")

class NextcloudUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = None
        self.users_list = random.sample(range(40), 40)
        self.user = None
        self.password = "test_password1234!"

    def on_start(self):
        user_id = self.users_list.pop()
        self.user = f"user{user_id}"
        self.auth = HTTPBasicAuth(self.user, self.password)
        self.verify_authentication()

    def verify_authentication(self):
        response = self.client.head("/remote.php/dav", auth=self.auth)
        if response.status_code != 200:
            error_msg = f"Authentication failed for user {self.user}: {response.text}.\n"
            Path("output.txt").write_text(error_msg, mode='a')
            raise Exception(error_msg)

    @task
    def propfind(self):
        try:
            response = self.client.request("PROPFIND", "/remote.php/dav", auth=self.auth)
            response.raise_for_status()
        except Exception as e:
            Path("output.txt").write_text(f"Error during PROPFIND request: {e} for user {self.user}.\n", mode='a')

    @task
    def upload_small(self):
        filename = Path("into-the-wild.png")
        try:
            with filename.open('rb') as f:
                response = self.client.put(f"/remote.php/dav/files/{self.user}/{filename.name}",
                                           auth=self.auth, data=f)
            if response.status_code not in [201, 204]:
                raise ValueError(f"Error during PUT request: {response.status_code}")
            
            self.client.delete(f"/remote.php/dav/files/{self.user}/{filename.name}",
                               auth=self.auth)
        except Exception as e:
            Path("output.txt").write_text(f"Error: {e} for user {self.user}.\n", mode='a')

    @task
    def get_request(self):
        self.client.get(f"/remote.php/dav/files/{self.user}/Readme.md",
                                auth=self.auth)

    @task
    def upload_big(self):
        filename = Path("big-file.png")
        try:
            with filename.open('rb') as f:
                response = self.client.put(f"/remote.php/dav/files/{self.user}/{filename.name}",
                                           auth=self.auth, data=f)
            if response.status_code not in [201, 204]:
                raise ValueError(f"Error during PUT request: {response.status_code}")
            
            self.client.delete(f"/remote.php/dav/files/{self.user}/{filename.name}",
                               auth=self.auth)
        except Exception as e:
            Path("output.txt").write_text(f"Error: {e} for user {self.user}.\n", mode='a')
        
