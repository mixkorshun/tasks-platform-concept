import sys

from project import setup

setup()

from project import database

database.migrate()


def generate_fake_data():
    from project.users.models import make_user, create_user
    from project.users.password import encode_password
    from project.tasks.models import create_task, make_task
    from faker import Faker

    employer = create_user(make_user(
        email='employer@platform.loc',
        password=encode_password('qwerty'),
        type='employer',
    ))

    employee = create_user(make_user(
        email='employee@platform.loc',
        password=encode_password('qwerty'),
        type='employee',
    ))

    fake = Faker()

    for i in range(100):
        create_task(make_task(
            name=fake.sentence(),
            price=fake.pydecimal(4, 2, True),
            description=fake.text(),
            author_id=employer['id'],
            status='open'
        ))

    for i in range(50):
        create_task(make_task(
            name=fake.sentence(),
            price=fake.pydecimal(4, 2, True),
            description=fake.text(),
            author_id=employer['id'],
            employee_id=employee['id'],
            status='open' if fake.pybool() else 'done'
        ))


if '--fake' in sys.argv:
    generate_fake_data()
