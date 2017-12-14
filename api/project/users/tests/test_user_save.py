from ..models import create_user


def test_create_user():
    user = create_user({
        'id': None,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee',
        'balance': 0,
    })

    assert user['id'] > 0


def test_create_user_with_id():
    user = create_user({
        'id': 12,
        'email': 'john@localhost',
        'password': '---',
        'type': 'employee',
        'balance': 0,
    })

    assert user['id'] == 12
