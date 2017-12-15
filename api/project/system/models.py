from decimal import Decimal
from logging import getLogger

from project import settings
from project.transactions.actions import withdraw_money, charge_money
from project.utils import money_from_float

logger = getLogger('platform.system')


def charge_author_for_task(user_id, task):
    withdraw_money(
        user_id,
        money_from_float(task['price']),
        commission=0,
        task_id=task['id']
    )


def pay_user_for_task(user_id, task):
    commission = money_from_float(
        task['price'] * Decimal.from_float(settings.SYSTEM_COMMISSION)
    )

    charge_money(
        user_id,
        task['price'] - commission,
        commission=commission,
        task_id=task['id']
    )
