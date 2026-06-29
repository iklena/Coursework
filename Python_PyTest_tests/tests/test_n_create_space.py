import os
import pytest
import requests

from dotenv import load_dotenv
from pathlib import Path

from faker import Faker

from helper.spaces_api_helper import SpacesApiHelper

fake = Faker()

current_dir = Path(__file__).parent
env_path = current_dir.parent / 'helper' / '.env'
load_dotenv(dotenv_path=env_path)

token = str(os.getenv("TOKEN"))
base_url = os.getenv("BASE_URL")
team = os.getenv("TEAM_ID")

space_name_n_uniq = f"space_{fake.first_name_female()}"


@pytest.fixture(scope="module")
def spaces_cleanup():
    space_helper = SpacesApiHelper()
    response_post_space = space_helper.create_space(space_name_n_uniq)
    space_id = response_post_space.json()['id']

    yield space_id

    response_delete_space = space_helper.delete_space(space_id)
    print('Check a Status Code for Space Delete: ', response_delete_space.status_code)


@pytest.mark.parametrize('token_auth, space_name, team_id, response_status, description', [
    (token, '', team, 400, 'Creation a space with an empty Space Name'),
    ('pk_invalid1234', 'space_name_new', team, 401, 'Creation a space with the invalid token'),
    (token,'test_name', '',404, 'Creation a space with the empty Team ID'),
    (token, space_name_n_uniq, team, 400, 'Creation a space with the non-unique Space Name'),
])


def test_n_create_space_request(token_auth, space_name, team_id, response_status, description, spaces_cleanup):

    headers_variable = {
        'Authorization': token_auth,
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url=f"{base_url}/team/{team_id}/space", headers=headers_variable, json={"name": space_name})

    assert response.status_code == response_status

    print(description + ' is PASSED')