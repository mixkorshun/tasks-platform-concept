import pytest

from project.transactions.actions import withdraw_money, charge_money
from project.users.models import create_user, get_user_by_id


@pytest.fixture(name='employee')
def employee_fixture():
    return create_user({
        'id': 1,
        'email': 'employee@localhost',
        'password': '---',
        'type': 'employee',
        'balance': 1000,
    })


def test_withdraw_money(employee):
    withdraw_money(employee['id'], 200)

    employee = get_user_by_id(employee['id'])

    assert employee['balance'] == 800


def test_charge_money(employee):
    charge_money(employee['id'], 200)

    employee = get_user_by_id(employee['id'])

    assert employee['balance'] == 1200
