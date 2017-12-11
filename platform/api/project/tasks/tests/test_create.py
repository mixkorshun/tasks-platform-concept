import json

import pytest
from flask import url_for

from project.auth import tokens
from project.auth.models import Store
from project.users.models import create_user


@pytest.fixture(name='employer')
def user_employer():
    return create_user({
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee'
    })


def test_get_not_authenticated(client):
    resp = client.post(url_for('tasks_list'))

    assert resp.status_code == 403
    assert resp.json['error_code'] == 'not_allowed'


def test_create_task(client, employer):
    resp = client.post(url_for('tasks_list'), data=json.dumps({
        'name': 'Task 1',
        'description': 'My first task',
        'price': 200,
    }), headers=[
        ('Authorization', 'Token ' + tokens.encode(Store(
            user_id=employer['id']
        )))
    ])

    assert resp.status_code == 201
    assert resp.json['id'] > 0
    assert resp.json['name'] == 'Task 1'
    assert resp.json['price'] == 200
    assert resp.json['description'] == 'My first task'
    assert resp.json['employer_id'] == employer['id']
    assert resp.json['status'] == 'open'


def test_create_minimal_params(client, employer):
    resp = client.post(url_for('tasks_list'), data=json.dumps({
        'name': 'Task 1'
    }), headers=[
        ('Authorization', 'Token ' + tokens.encode(Store(
            user_id=employer['id']
        )))
    ])

    assert resp.status_code == 201
    assert resp.json['id'] > 0
    assert resp.json['name'] == 'Task 1'
    assert resp.json['price'] is None
    assert resp.json['description'] == ''


def test_create_missing_name(client, employer):
    resp = client.post(url_for('tasks_list'), data=json.dumps({}), headers=[
        ('Authorization', 'Token ' + tokens.encode(Store(
            user_id=employer['id']
        )))
    ])

    assert resp.status_code == 400
    assert resp.json['error_code'] == 'bad_request'
