import json

from flask import url_for


def test_register(client):
    resp = client.post(
        url_for('users_register'),
        data=json.dumps({
            'email': 'john@platform.loc',
            'password': 'qwerty',
            'type': 'employee',
        })
    )

    assert resp.status_code == 200
    assert resp.json['email'] == 'john@platform.loc'
    assert 'password' not in resp.json


def test_register_and_login(client):
    client.post(
        url_for('users_register'),
        data=json.dumps({
            'email': 'john@platform.loc',
            'password': 'qwerty',
            'type': 'employee',
        })
    )

    resp = client.post(
        url_for('users_login'),
        data=json.dumps({
            'email': 'john@platform.loc',
            'password': 'qwerty'
        })
    )

    assert resp.status_code == 200
    assert resp.json['token']
