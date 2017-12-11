import pytest

from ..models import create_user, update_user


def test_create_user():
    user = create_user({
        'id': None,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    })

    assert user['id'] > 0


def test_create_user_with_id():
    user = create_user({
        'id': 12,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    })

    assert user['id'] == 12


def test_update_user():
    user = create_user({
        'id': None,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    })

    insert_id = user['id']

    update_id = update_user(user)['id']

    assert update_id == insert_id


def test_update_non_existent_user():
    with pytest.raises(RuntimeError):
        update_user({
            'id': 1,
            'email': 'john@localhost',
            'password': '---',
            'type': 'employee'
        })
