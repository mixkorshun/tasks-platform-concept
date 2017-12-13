import pytest
from flask import url_for

from project.auth.tokens import get_token
from project.tasks.models import create_task, make_task, get_task_by_id, \
    update_task
from project.users.models import create_user


@pytest.fixture(name='employee')
def employee_fixture():
    return create_user({
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee'
    })


@pytest.fixture(name='employer')
def employer_fixture():
    return create_user({
        'id': 2,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer'
    })


@pytest.fixture(name='task')
def task_fixture(employer):
    return create_task(make_task(**{
        'id': 1,
        'name': 'Task',
        'price': 300,
        'author_id': employer['id'],
        'description': '',
        'status': 'open'
    }))


def test_assign_task(client, task, employee):
    resp = client.post(url_for('tasks_assign', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(employee['id']))
    ])
    task = get_task_by_id(task['id'])

    assert resp.status_code == 200
    assert task['employee_id'] == employee['id']


def test_assign_deleted_task(client, employee):
    resp = client.post(url_for('tasks_assign', task_id=1), headers=[
        ('Authorization', 'Token ' + get_token(employee['id']))
    ])
    assert resp.status_code == 404


def test_cannot_assign_already_assigned_task(client, task, employee):
    task['employee_id'] = 3
    update_task(task)

    resp = client.post(url_for('tasks_assign', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(employee['id']))
    ])

    assert resp.status_code == 403
