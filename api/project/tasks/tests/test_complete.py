import pytest
from flask import url_for, request

from project import settings
from project.tasks.models import create_task, make_task, get_task_by_id, \
    update_task
from project.users.models import create_user, get_user_by_id
from project.users.tokens import get_token


@pytest.fixture(name='employee')
def employee_fixture():
    return create_user({
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee',
        'balance': 0,
    })


@pytest.fixture(name='employer')
def employer_fixture():
    return create_user({
        'id': 2,
        'email': 'employer@localhost',
        'password': '---',
        'type': 'employer',
        'balance': 0
    })


@pytest.fixture(name='task')
def task_fixture(employer):
    return create_task(make_task(**{
        'id': 1,
        'name': 'Task',
        'price': 300,
        'author_id': employer['id'],
        'description': '',
        'status': 'open',
        'ok': 1
    }))


def test_complete_task(client, task, employee):
    client.open()

    task['employee_id'] = employee['id']
    update_task(task)

    resp = client.post(url_for('tasks_complete', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])

    task = get_task_by_id(task['id'])

    assert resp.status_code == 200
    assert task['status'] == 'done'


def test_complete_deleted_task(client, employee):
    client.open()

    resp = client.post(url_for('tasks_complete', task_id=1), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])
    assert resp.status_code == 404


def test_cannot_complete_unassigned_task(client, task, employee):
    resp = client.post(url_for('tasks_complete', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])
    assert resp.status_code == 403


def test_cannot_complete_foreign_task(client, task, employee):
    task['employee_id'] = employee['id'] + 10
    update_task(task)

    resp = client.post(url_for('tasks_complete', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])
    assert resp.status_code == 403


def test_cannot_complete_already_done_task(client, task, employee):
    task['employee_id'] = employee['id']
    task['status'] = "done"
    update_task(task)

    resp = client.post(url_for('tasks_complete', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])
    assert resp.status_code == 403


def test_complete_add_money(client, task, employee):
    client.open()

    task['employee_id'] = employee['id']
    update_task(task)

    client.post(url_for('tasks_complete', task_id=task['id']), headers=[
        ('Authorization', 'Token ' + get_token(request, employee['id']))
    ])

    employee = get_user_by_id(employee['id'])

    assert employee['balance'] == 300 * (1 - settings.SYSTEM_COMMISSION)
