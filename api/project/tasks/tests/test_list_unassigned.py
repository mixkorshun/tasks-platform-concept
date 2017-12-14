import pytest
from flask import url_for, request

from project.auth.tokens import get_token
from project.users.models import create_user
from ..models import create_task, make_task


@pytest.fixture(name='employer')
def employer_fixture():
    return create_user({
        'id': 1,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer',
        'balance': 0,
    })


@pytest.fixture(name='employee')
def employee_fixture():
    return create_user({
        'id': 2,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee',
        'balance': 0,
    })


@pytest.fixture(name='tasks')
def tasks_fixture(employer):
    tasks = []
    for i in range(10):
        tasks.append(create_task(make_task(**{
            'id': i + 1,
            'name': 'Task %d' % (i + 1),
            'price': 300,
            'author_id': employer['id'],
            'description': '',
            'status': 'open'
        })))

    return tasks


def test_tasks_list(client, tasks, employee):
    client.open()

    resp = client.get(url_for('tasks_list_unassigned'), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])

    assert resp.status_code == 200
    assert len(resp.json) == 10
    assert resp.json[0]['id'] == tasks[9]['id']


def test_tasks_list_limit(tasks, client, employee):
    client.open()

    resp = client.get(url_for('tasks_list_unassigned') + "?limit=5", headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])

    assert resp.status_code == 200
    assert len(resp.json) == 5


def test_tasks_list_from_last_id(tasks, client, employee):
    client.open()

    resp = client.get(url_for('tasks_list_unassigned') + "?last_id=5",
                      headers=[
                          ('Authorization',
                           'Token ' + get_token(request, employee['id']))
                      ])

    assert resp.status_code == 200
    assert len(resp.json) == 4

    for row in resp.json:
        assert row['id'] < 5
