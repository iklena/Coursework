import os

import requests
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

token = str(os.getenv("TOKEN"))
base_url = os.getenv("BASE_URL")
team_Id = os.getenv("TEAM_ID")

fake = Faker()

class SpacesApiHelper:
    def __init__(self):
        self.token_auth = token
        self.url = base_url
        self.teamId = team_Id
        self.headers_variable = {
            'Authorization': self.token_auth,
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }


    def create_space(self, name):
        response = requests.post(url=f"{self.url}/team/{self.teamId}/space", headers = self.headers_variable, json = {"name": name})
        return response

    def get_space_info(self, space_id):
        response = requests.get(url=f"{self.url}/space/{space_id}", headers=self.headers_variable)
        return response

    def get_spaces(self):
        response = requests.get(url=f"{self.url}/team/{self.teamId}/space", headers = self.headers_variable)
        return response

    def update_space(self, space_id, name_upd):
        response = requests.put(url=f"{self.url}/space/{space_id}", headers=self.headers_variable, json = {"name": name_upd})
        return response

    def delete_space(self, space_id):
        response = requests.delete(url=f"{self.url}/space/{space_id}", headers=self.headers_variable)
        return response