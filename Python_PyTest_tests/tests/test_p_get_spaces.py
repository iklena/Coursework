from pytest_steps import test_steps
from faker import Faker

from helper.spaces_api_helper import SpacesApiHelper
fake = Faker()


@test_steps('Create 2 spaces', 'Get spaces', 'Delete all spaces')

def test_get_spaces_request():
    global space_name
    global space_id
    space_helper = SpacesApiHelper()

    created_spaces_ids = []

    for i in range(2):

        space_name = f"space_{fake.first_name_female()}"

        # print(space_name)
        response_post_space = space_helper.create_space(space_name)

        assert response_post_space.status_code == 200
        assert response_post_space.json()['name'] == space_name

        space_id = response_post_space.json()['id']
        created_spaces_ids.append(space_id)

        print(f"The space is created. ID is {space_id}, Name is {response_post_space.json()['name']}")

    yield

    response_get_spaces = space_helper.get_spaces()

    print('Check a Status Code for Get Spaces: ', response_get_spaces.status_code)
    assert response_get_spaces.status_code == 200

    spaces_array = response_get_spaces.json()['spaces']

    l = len(spaces_array)

    assert spaces_array[l - 1]['id'] == space_id
    assert spaces_array[l-1]['name'] == space_name

    print(f'Space has the correct name: ID is {space_id}, Name is {space_name}')

    yield

    for space_id in created_spaces_ids:

        response_delete_space = space_helper.delete_space(space_id)
        print(f'Check a Status Code for Delete Space {space_id}: ', response_delete_space.status_code)
        assert response_delete_space.status_code == 200

    yield