from locust import HttpUser, task
from requests.auth import HTTPBasicAuth
import requests
import random

def write_log(message):
    with open("output.txt", "a") as log_file:
        log_file.write(message + "\n")

write_log("_________________________________________________")

class UserSimulator(HttpUser):
    login_auth = None
    available_users = [f"user{n}" for n in range(40)]

    def on_start(self):
        self.current_user = random.choice(self.available_users)
        self.available_users.remove(self.current_user)
        password = 'test_password1234!'
        self.login_auth = HTTPBasicAuth(self.current_user, password)
        self.check_auth()

    def check_auth(self):
        resp = self.client.head("/remote.php/dav", auth=self.login_auth)
        if resp.status_code != 200:
            write_log(f"Auth failed for {self.current_user}: {resp.text}")
            raise Exception(f"Auth failed for {self.current_user}")

    @task
    def find_properties(self):
        try:
            self.client.request("PROPFIND", "/remote.php/dav", auth=self.login_auth).raise_for_status()
        except Exception as error:
            write_log(f"PROPFIND error: {error} for {self.current_user}")
    """
    @task
    def small_upload(self):
        pic = "into-the-wild.png"
        with open(pic, 'rb') as image:
            put_resp = self.client.put(f"/remote.php/dav/files/{self.current_user}/{pic}",
                                       auth=self.login_auth, data=image, name=f"/remote.php/dav/files/[user]/{pic}")
        
        if put_resp.status_code not in [201, 204]:
            write_log(f"PUT error: {put_resp.status_code} for {self.current_user}")

        self.perform_actions(pic)
    """

    @task
    def medium_upload(self):
        pic = "medium-file.txt"
        with open(pic, 'rb') as image:
            put_resp = self.client.put(f"/remote.php/dav/files/{self.current_user}/{pic}",
                                       auth=self.login_auth, data=image, name=f"/remote.php/dav/files/{self.current_user}/{pic}")

                
        if put_resp.status_code not in [201, 204]:
            write_log(f"PUT error: {put_resp.status_code} for {self.current_user}")

        self.perform_actions(pic)

    """
    @task
    def big_upload(self):
        pic = "big-file.txt"
        with open(pic, 'rb') as image:
            put_resp = self.client.put(f"/remote.php/dav/files/{self.current_user}/{pic}",
                                       auth=self.login_auth, data=image, name=f"/remote.php/dav/files/[user]/{pic}")

    
        
        if put_resp.status_code not in [201, 204]:
            write_log(f"PUT error: {put_resp.status_code} for {self.current_user}")

        self.perform_actions(pic)
        
    """

    def perform_actions(self, pic):
        for _ in range(5):
            self.client.get(f"/remote.php/dav/files/{self.current_user}/{pic}",
                            auth=self.login_auth, name=f"/remote.php/dav/files/{self.current_user}/{pic}")
        self.client.delete(f"/remote.php/dav/files/{self.current_user}/{pic}",
                           auth=self.login_auth, name=f"/remote.php/dav/files/{user}/{pic}")
