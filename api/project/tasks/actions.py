from project.system.models import pay_user_for_task, charge_author_for_task
from project.users.models import get_user_by_id
from project.utils import qb, money_from_float
from .models import get_task_by_id, update_tasks, make_task, create_task, \
    mark_task_ok


def add_task(name, author_id, price, description):
    user = get_user_by_id(author_id)
    if user['type'] != 'employer':
        raise PermissionError('Only employer can add tasks.')

    task = create_task(make_task(
        name=name,
        description=description,
        price=money_from_float(price),

        author_id=author_id,
        status='open',
        ok=0
    ))

    charge_author_for_task(author_id, task)

    mark_task_ok(task['id'])

    return task


def assign_task(task_id, user_id):
    task = get_task_by_id(task_id)

    if not task:
        raise LookupError('Task not found.')

    if task['employee_id'] is not None:
        raise PermissionError("Task already assigned.")

    q = qb.make('update')
    qb.add_values(q, [
        ('employee_id', '{employee_id}')
    ], {'employee_id': user_id})

    qb.add_where(q, [
        'id = {id}',
        'employee_id IS NULL',
        'ok = 1'
    ], {'id': task_id, 'user_id': user_id})

    c = update_tasks(q)

    if c == 0:
        raise PermissionError("Task already assigned.")


def complete_task(task_id, user_id):
    task = get_task_by_id(task_id)

    if not task:
        raise LookupError('Task not found.')

    if task['employee_id'] != user_id:
        raise PermissionError("Not assigned to you.")

    if task['status'] == 'done':
        raise PermissionError("Already done.")

    q = qb.make('update')
    qb.add_values(q, [
        ('status', '"done"'),
        ('ok', 0)
    ])

    qb.add_where(q, [
        'id = {id}',
        'status = "open"',
        'ok = 1'
    ], {'id': task_id})

    c = update_tasks(q)

    if c == 0:
        raise PermissionError("Already done.")

    pay_user_for_task(user_id, task)

    mark_task_ok(task_id)
