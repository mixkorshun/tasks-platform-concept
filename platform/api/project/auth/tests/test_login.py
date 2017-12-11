import json

import pytest
from flask import url_for

from project import database, queries
from project.users.password import encode_password
from .. import tokens


@pytest.fixture(name='load_users', scope="module")
def db_users():
    queries.save_object(database.get_connection(), 'users', {
        'id': 1,
        'email': 'one@localhost',
        'password': encode_password('qwerty'),
        'type': 'employee',
    }, force_create=True)


def test_correct_login(load_users, client):
    resp = client.post(
        url_for('authorize'),
        data=json.dumps({
            'email': 'one@localhost',
            'password': 'qwerty'
        })
    )

    assert resp.status_code == 200
    assert tokens.decode(resp.json['token']).user_id == 1


def test_incorrect_login(load_users, client):
    resp = client.post(
        url_for('authorize'),
        data=json.dumps({
            'email': 'missing@localhost',
            'password': 'qwerty'
        })
    )

    assert resp.status_code == 400
    assert resp.json['error_code'] == 'invalid_credentials'


def test_incorrect_password(load_users, client):
    resp = client.post(
        url_for('authorize'),
        data=json.dumps({
            'email': 'one@localhost',
            'password': 'qwerty1234'
        })
    )

    assert resp.status_code == 400
    assert resp.json['error_code'] == 'invalid_credentials'
