import json

import pytest
from flask import url_for

from project.auth import tokens
from project.users.models import create_user


@pytest.fixture(name='employer')
def employer_fixture():
    return create_user({
        'id': 1,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer'
    })


def test_get_not_authenticated(client):
    resp = client.post(url_for('tasks_create'))

    assert resp.status_code == 403
    assert resp.json['error_code'] == 'not_allowed'


def test_create_task(client, employer):
    resp = client.post(url_for('tasks_create'), data=json.dumps({
        'name': 'Task 1',
        'description': 'My first task',
        'price': 200,
    }), headers=[
        ('Authorization', 'Token ' + tokens.get_token(employer['id']))
    ])

    assert resp.status_code == 201
    assert resp.json['id'] > 0
    assert resp.json['name'] == 'Task 1'
    assert resp.json['price'] == 200
    assert resp.json['description'] == 'My first task'
    assert resp.json['author_id'] == employer['id']
    assert resp.json['status'] == 'open'


def test_create_minimal_params(client, employer):
    resp = client.post(url_for('tasks_create'), data=json.dumps({
        'name': 'Task 1'
    }), headers=[
        ('Authorization', 'Token ' + tokens.get_token(employer['id']))
    ])

    assert resp.status_code == 201
    assert resp.json['id'] > 0
    assert resp.json['name'] == 'Task 1'
    assert resp.json['price'] is None
    assert resp.json['description'] == ''


def test_create_missing_name(client, employer):
    resp = client.post(url_for('tasks_create'), data=json.dumps({}), headers=[
        ('Authorization', 'Token ' + tokens.get_token(employer['id']))
    ])

    assert resp.status_code == 400
    assert resp.json['error_code'] == 'bad_request'