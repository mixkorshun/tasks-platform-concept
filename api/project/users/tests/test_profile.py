import pytest
from flask import url_for, request

from project.users import tokens
from project.users.models import create_user


@pytest.fixture(name='employee')
def user_employee():
    return create_user({
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee',
        'balance': 0,
    })


def test_get_not_authenticated(client):
    resp = client.get(url_for('users_me'))

    assert resp.status_code == 403
    assert resp.json['error_code'] == 'not_allowed'


def test_get_profile(client, employee):
    client.open()

    resp = client.get(url_for('users_me'), headers=[
        ('Authorization', 'Token ' + tokens.get_token(request, employee['id']))
    ])

    assert resp.status_code == 200
    assert resp.json['id'] == employee['id']
    assert resp.json['email'] == employee['email']
    assert resp.json['type'] == employee['type']
