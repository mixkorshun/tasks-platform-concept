from logging import getLogger

from project import settings
from project.transactions.actions import withdraw_money, charge_money

logger = getLogger('platform.system')


def charge_author_for_task(user_id, task):
    withdraw_money(
        user_id,
        task['price'],
        task['id']
    )


def pay_user_for_task(user_id, task):
    charge_money(
        user_id,
        float(task['price']) * (1 - settings.SYSTEM_COMMISSION),
        task['id']
    )

    logger.info('earn $%s' % task['price'])
