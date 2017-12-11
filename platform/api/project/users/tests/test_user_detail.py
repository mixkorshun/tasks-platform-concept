import pytest
from flask import url_for

from ..models import save_user


@pytest.fixture(name='employee')
def user_employee():
    user = {
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee'
    }
    save_user(user, force_create=True)

    return user


@pytest.fixture(name='employer')
def user_employer():
    user = {
        'id': 2,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer'
    }
    save_user(user, force_create=True)

    return user


def test_get_user(client, employee):
    resp = client.get(url_for('users_detail', user_id=employee['id']))

    assert resp.status_code == 200
    assert resp.json['id'] == employee['id']
    assert resp.json['email'] == employee['email']
    assert resp.json['type'] == employee['type']


def test_get_not_existent_user(client):
    resp = client.get(url_for('users_detail', user_id=1))

    assert resp.status_code == 404
    assert resp.json['error_code'] == 'not_found'
