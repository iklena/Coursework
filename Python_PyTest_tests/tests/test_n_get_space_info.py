import os
import pytest
import requests

from dotenv import load_dotenv
from pathlib import Path
from helper.spaces_api_helper import SpacesApiHelper

current_dir = Path(__file__).parent
env_path = current_dir.parent / 'helper' / '.env'
load_dotenv(dotenv_path=env_path)

token = str(os.getenv("TOKEN"))
base_url = os.getenv("BASE_URL")
team = os.getenv("TEAM_ID")


@pytest.fixture(scope="function")
def space_helper():
    return SpacesApiHelper()


@pytest.fixture(scope="function")
def created_space_id(space_helper):

    response_post_space = space_helper.create_space('test_space')

    space_id = response_post_space.json()['id']

    yield space_id

    space_helper.delete_space(space_id)


@pytest.mark.parametrize('token_auth, space, response_status, description', [
    (token, '', 404, 'Get the space info with the empty Space ID'),
    ('pk_invalid1234', 'created_space_id', 401, 'Get the space info with the invalid token'),
    (token,'test_id', 400, 'Get the space info with the incorrect Space ID'),
])


def test_n_get_space_info_request(space_helper, created_space_id, token_auth, space, response_status, description):

    headers_variable = {
        'Authorization': token_auth,
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.get(url=f"{base_url}/space/{space}", headers=headers_variable)

    assert response.status_code == response_status

    print(description + ' is PASSED')