from flask import request, jsonify
from werkzeug.exceptions import NotFound, BadRequest, Forbidden

from project import app
from project.users.shortcuts import only_authorized
from project.utils import get_post_data, validators as v, money_from_float
from project.utils.pagination import paginate_by_pk
from .actions import assign_task, complete_task, add_task
from .lists import build_authored, build_unassigned, build_assigned
from .models import select_tasks


@app.route('/tasks/', methods=['POST'])
@only_authorized
def tasks_create():
    data = get_post_data(request, {
        'name': '',
        'price': None,
        'description': ''
    })

    try:
        v.required(data['name'])
        v.type(v.required(data['price']), (int, float))
        v.greater_then(data['price'], 0)
    except ValueError:
        raise BadRequest(
            'Invalid form params.'
        )

    data['price'] = money_from_float(data['price'])

    try:
        task = add_task(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            author_id=request.user_id
        )
    except PermissionError as e:
        raise Forbidden(
            'Permission error: %s' % (e.args[0] if e.args else 'Unknown')
        )

    response = jsonify(task)
    response.status_code = 201
    return response


@app.route('/tasks/unassigned/', methods=['GET'])
@only_authorized
def tasks_list_unassigned():
    last_id = request.args.get('last_id', None, int)
    limit = min(request.args.get('limit', 20, int), 1000)

    q = build_unassigned()
    paginate_by_pk(q, last_id, limit)
    tasks = select_tasks(q)

    return jsonify(list(tasks))


@app.route('/tasks/assigned/', methods=['GET'])
@only_authorized
def tasks_list_assigned():
    last_id = request.args.get('last_id', None, int)
    limit = min(request.args.get('limit', 20, int), 1000)

    q = build_assigned(request.user_id)
    paginate_by_pk(q, last_id, limit)
    tasks = select_tasks(q)

    return jsonify(list(tasks))


@app.route('/tasks/authored/', methods=['GET'])
@only_authorized
def tasks_list_authored():
    last_id = request.args.get('last_id', None, int)
    limit = min(request.args.get('limit', 20, int), 1000)

    q = build_authored(request.user_id)
    paginate_by_pk(q, last_id, limit)

    tasks = select_tasks(q)

    return jsonify(list(tasks))


@app.route('/tasks/<int:task_id>/assign/', methods=['POST'])
@only_authorized
def tasks_assign(task_id):
    try:
        assign_task(task_id, request.user_id)
    except LookupError:
        raise NotFound('Task not found')
    except PermissionError as e:
        raise Forbidden(
            'Permission error: %s' % (e.args[0] if e.args else 'Unknown')
        )

    return jsonify({})


@app.route('/tasks/<int:task_id>/complete/', methods=['POST'])
@only_authorized
def tasks_complete(task_id):
    try:
        complete_task(task_id, request.user_id)
    except LookupError:
        raise NotFound('Task not found')
    except PermissionError as e:
        raise Forbidden(
            'Permission error: %s' % (e.args[0] if e.args else 'Unknown')
        )

    return jsonify({})
