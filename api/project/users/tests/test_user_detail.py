import pytest
from flask import url_for

from ..models import create_user


@pytest.fixture(name='employee')
def user_employee():
    return create_user({
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee'
    })


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
