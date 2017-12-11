import pytest

from ..models import save_user


def test_create_user():
    user_id = save_user({
        'id': None,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    })

    assert user_id > 0


def test_force_create_user():
    user_id = save_user({
        'id': 12,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    }, force_create=True)

    assert user_id == 12


def test_update_user():
    user_id = save_user({
        'id': None,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    })

    user = {
        'id': user_id,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee'
    }

    user_id = save_user(user)

    assert user_id == user['id']


def test_update_non_existent_user():
    with pytest.raises(RuntimeError):
        save_user({
            'id': 1,
            'email': 'john@localhost',
            'password': '---',
            'type': 'employee'
        })
