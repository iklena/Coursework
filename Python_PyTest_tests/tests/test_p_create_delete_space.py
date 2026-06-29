from pytest_steps import test_steps
from faker import Faker

from helper.spaces_api_helper import SpacesApiHelper

fake = Faker()

@test_steps('Create a space', 'Delete the created space')

def test_create_delete_space_request():

    space_helper = SpacesApiHelper()

    space_name = f"space_{fake.first_name_female()}"
    response_post_space = space_helper.create_space(space_name)

    print('Check a Status Code for Space Creating: ', response_post_space.status_code)
    assert response_post_space.status_code == 200
    assert response_post_space.json()['name'] == space_name

    space_id = response_post_space.json()['id']
    print(f"The space is created. ID is {space_id}, Name is {response_post_space.json()['name']}")

    yield

    response_delete_space = space_helper.delete_space(space_id)
    print('Check a Status Code for Space Delete: ', response_delete_space.status_code)
    assert response_delete_space.status_code == 200
    print('The space is deleted. ID is ' + space_id)

    yield