import pytest
from flask import url_for

from project.users.models import create_user
from ..models import create_task, make_task


@pytest.fixture(name='employer')
def employer_fixture():
    return create_user({
        'id': 1,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer'
    })


@pytest.fixture(name='task')
def task_fixture(employer):
    return create_task(make_task(**{
        'id': 1,
        'name': 'Sample task',
        'price': 300,
        'employer_id': employer['id'],
        'description': 'My first example task',
        'status': 'open'
    }))


def test_get_task(client, task):
    resp = client.get(url_for('tasks_detail', task_id=task['id']))

    assert resp.status_code == 200
    assert resp.json['id'] == task['id']
    assert resp.json['name'] == task['name']


def test_get_not_existent_task(client):
    resp = client.get(url_for('tasks_detail', task_id=1))

    assert resp.status_code == 404
    assert resp.json['error_code'] == 'not_found'
