from pytest_steps import test_steps
from faker import Faker

from helper.spaces_api_helper import SpacesApiHelper

fake = Faker()

@test_steps('Create a space', 'Update the created space', 'Get the space info', 'Delete the created space')

def test_put_space_request():

    space_helper = SpacesApiHelper()

    space_name = f"space_{fake.first_name_female()}"
    response_post_space = space_helper.create_space(space_name)

    print('Check a Status Code for Create Space: ', response_post_space.status_code)
    assert response_post_space.status_code == 200
    assert response_post_space.json()['name'] == space_name

    space_id = response_post_space.json()['id']
    print(f"The space is created. ID is {space_id}, Name is {response_post_space.json()['name']}")

    yield

    name_upd = f"space_{fake.first_name_female()}"
    response_put_space = space_helper.update_space(space_id, name_upd)

    assert response_put_space.status_code == 200
    assert response_put_space.json()['id'] == space_id
    assert response_put_space.json()['name'] == name_upd

    print('Check a Status Code for Get Space Info: ', response_put_space.status_code)
    print(f"New name is {name_upd}")

    print(f"The space contains the updated name: ID is {response_put_space.json()['id']}, Name is {response_put_space.json()['name']}")

    yield

    response_get_space_info = space_helper.get_space_info(space_id)

    assert response_get_space_info.status_code == 200
    assert response_get_space_info.json()['name'] == name_upd

    print(f"The space contains the updated name: ID is {response_get_space_info.json()['id']}, Name is {response_get_space_info.json()['name']}")

    yield

    response_delete_space = space_helper.delete_space(space_id)
    print('Check a Status Code for Delete Space: ', response_delete_space.status_code)

    assert response_delete_space.status_code == 200

    print('The space is deleted. ID is ' + space_id)

    yield