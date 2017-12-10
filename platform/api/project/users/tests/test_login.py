import json

import pytest
from flask import url_for

from project.db import get_db_connection
from project.session import from_jwt_token
from ..password import encode_password


@pytest.fixture(name='load_users', scope="module")
def db_users():
    query = '''
INSERT INTO users(id, email, password, type) VALUES (
  1, 'one@localhost', '%(qwerty_password)s', 'employee'
);
''' % {
        'qwerty_password': encode_password('qwerty')
    }
    db = get_db_connection()

    db.executescript(query)


def test_correct_login(load_users, client):
    resp = client.post(
        url_for('authorize'),
        data=json.dumps({
            'email': 'one@localhost',
            'password': 'qwerty'
        })
    )

    assert resp.status_code == 200
    assert from_jwt_token(resp.json['token']).user_id == 1


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
