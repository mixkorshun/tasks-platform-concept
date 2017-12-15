import re

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # noqa:
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$',
    re.IGNORECASE)


def email(value):
    msg = 'Invalid email address.'

    if value and '@' in value:
        parts = value.split('@')

        try:
            parts[-1] = parts[-1].encode('idna')
        except UnicodeError:
            raise ValueError(msg)

    if not email_re.match(value):
        raise ValueError(msg)

    return value


def required(value):
    if not value:
        raise ValueError('Value is required')

    return value


def type(value, t):
    if value is not None and not isinstance(value, t):
        raise ValueError(
            '%s is not of type %s' % (value, str(t))
        )

    return value


def choices(value, ch):
    if value not in ch:
        raise ValueError(
            '%s is not %s' % (value, str(ch))
        )
    return value
