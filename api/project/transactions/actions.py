from project.users.models import decrease_user_amount, increase_user_amount
from .models import make_transaction, create_transaction


def withdraw_money(user_id, amount, task_id=None):
    transaction = make_transaction(
        user_id=user_id,
        task_id=task_id,
        amount=-amount
    )

    create_transaction(transaction)
    decrease_user_amount(user_id, amount)


def charge_money(user_id, amount, task_id=None):
    transaction = make_transaction(
        user_id=user_id,
        task_id=task_id,
        amount=amount
    )

    create_transaction(transaction)
    increase_user_amount(user_id, amount)
