import os
import pytest
import requests

from dotenv import load_dotenv
from pathlib import Path

current_dir = Path(__file__).parent
env_path = current_dir.parent / 'helper' / '.env'
load_dotenv(dotenv_path=env_path)

token = str(os.getenv("TOKEN"))
base_url = os.getenv("BASE_URL")
team = os.getenv("TEAM_ID")


@pytest.mark.parametrize('token_auth, team_id, response_status, description', [
    (token, None, 400, 'Get spaces with the empty Team ID'),
    ('pk_invalid1234', team, 401, 'Get spaces with the invalid token'),
    (token,'1', 401, 'Get spaces with the incorrect Team ID')
])


def test_n_get_spaces_request(token_auth, team_id, response_status, description):

    headers_variable = {
        'Authorization': token_auth,
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = (requests.get(url=f"{base_url}/team/{team_id}/space", headers = headers_variable))

    assert response.status_code == response_status

    print(description + ' is PASSED')