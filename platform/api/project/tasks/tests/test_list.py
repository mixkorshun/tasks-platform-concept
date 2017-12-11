import pytest
from flask import url_for

from project.users.models import create_user
from ..models import create_task, make_task


@pytest.fixture(name='employer')
def user_employer():
    return create_user({
        'id': 1,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer'
    })


@pytest.fixture(name='tasks')
def sample_tasks(employer):
    tasks = []
    for i in range(10):
        tasks.append(create_task(make_task(**{
            'id': i + 1,
            'name': 'Task %d' % (i + 1),
            'price': 300,
            'employer_id': employer['id'],
            'description': '',
            'status': 'open'
        })))

    return tasks


def test_tasks_list(client, tasks):
    resp = client.get(url_for('tasks_list'))

    assert resp.status_code == 200
    assert len(resp.json) == 10
    assert resp.json[0]['id'] == tasks[9]['id']


def test_tasks_list_limit(tasks, client):
    resp = client.get(url_for('tasks_list') + "?limit=5")

    assert resp.status_code == 200
    assert len(resp.json) == 5


def test_tasks_list_from_last_id(tasks, client):
    resp = client.get(url_for('tasks_list') + "?last_id=5")

    assert resp.status_code == 200
    assert len(resp.json) == 4

    for row in resp.json:
        assert row['id'] < 5
