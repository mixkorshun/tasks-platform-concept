import json

from flask import request, jsonify, url_for
from werkzeug.exceptions import NotFound, Forbidden, BadRequest

from project import app
from project.tasks.models import select_tasks, make_task, create_task, \
    get_task_by_id
from project.utils import qb


@app.route('/tasks/', methods=['GET', 'POST'])
def tasks_list():
    if request.method == 'GET':
        last_id = request.args.get('last_id', -1, int)
        limit = min(request.args.get('limit', 20, int), 1000)

        status = request.args.get('status')

        q = qb.make('select')
        qb.add_ordering(q, ('id', 'DESC'))

        if last_id > 0:
            qb.add_where(q, 'id < :last_id', {
                'last_id': last_id
            })
        qb.set_limit(q, limit)

        if status:
            qb.add_where(q, 'status = :status', {
                'status': status
            })

        tasks = select_tasks(q)

        return jsonify(list(tasks))
    elif request.method == 'POST':
        if not request.session:
            raise Forbidden()

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

            employer_id=request.session.user_id,
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
