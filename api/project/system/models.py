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
        task['id']
    )


def pay_user_for_task(user_id, task):
    system_earning = money_from_float(
        task['price'] * Decimal.from_float(settings.SYSTEM_COMMISSION)
    )

    charge_money(user_id, task['price'] - system_earning, task['id'])

    logger.info('SYSTEM EARN: $%s' % system_earning)
