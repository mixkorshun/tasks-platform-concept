import json

import pytest
from flask import url_for, request

from project.users.models import create_user
from project.users.password import encode_password
from .. import tokens


@pytest.fixture(name='user')
def fixture_user():
    return create_user({
        'id': 1,
        'email': 'one@platform.loc',
        'password': encode_password('qwerty'),
        'type': 'employee',
        'balance': 0,
    })


def test_correct_login(user, client):
    resp = client.post(
        url_for('users_login'),
        data=json.dumps({
            'email': user['email'],
            'password': 'qwerty'
        })
    )

    assert resp.status_code == 200
    assert tokens.get_user_id(request, resp.json['token']) == 1


def test_incorrect_login(user, client):
    resp = client.post(
        url_for('users_login'),
        data=json.dumps({
            'email': 'missing@platform.loc',
            'password': 'qwerty'
        })
    )

    assert resp.status_code == 400
    assert resp.json['error_code'] == 'invalid_credentials'


def test_incorrect_password(user, client):
    resp = client.post(
        url_for('users_login'),
        data=json.dumps({
            'email': user['email'],
            'password': 'qwerty1234'
        })
    )

    assert resp.status_code == 400
    assert resp.json['error_code'] == 'invalid_credentials'
