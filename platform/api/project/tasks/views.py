import json

from flask import request, jsonify, url_for
from werkzeug.exceptions import NotFound, BadRequest, Forbidden

from project import app
from project.auth.shortcuts import only_authorized
from project.tasks.models import select_tasks, make_task, create_task, \
    get_task_by_id
from project.users.models import get_user_by_id
from project.utils import qb


@app.route('/tasks/', methods=['GET', 'POST'])
@only_authorized
def tasks_list():
    if request.method == 'GET':
        last_id = request.args.get('last_id', -1, int)
        limit = min(request.args.get('limit', 20, int), 1000)

        q = qb.make('select')
        qb.add_ordering(q, ('id', 'DESC'))

        if last_id > 0:
            qb.add_where(q, 'id < {last_id}', {
                'last_id': last_id
            })
        qb.set_limit(q, limit)

        qb.add_where(q, 'employee_id IS NULL')
        qb.add_where(q, 'status = "open"')

        tasks = select_tasks(q)

        return jsonify(list(tasks))
    elif request.method == 'POST':
        user = get_user_by_id(request.user_id)
        if user['type'] != 'employer':
            raise Forbidden(
                'Sorry, you cannot create new tasks.'
            )

        post_data = json.loads(request.data.decode())

        try:
            name = post_data['name']
            description = post_data.get('description', '')
            price = post_data.get('price')
        except KeyError:
            raise BadRequest(
                'Missing one of following required params: (name,)'
            )

        task = create_task(make_task(
            name=name,
            description=description,
            price=price,

            author_id=request.user_id,
            status='open',
        ))

        response = jsonify(task)
        response.status_code = 201
        response.headers['Location'] = url_for(
            'tasks_detail', task_id=task['id']
        )

        return response


@app.route('/tasks/<int:task_id>/', methods=['GET'])
def tasks_detail(task_id):
    task = get_task_by_id(task_id)

    if not task:
        raise NotFound('Task not found.')

    return jsonify(task)
