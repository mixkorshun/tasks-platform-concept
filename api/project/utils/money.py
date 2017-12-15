from decimal import Decimal


def money_from_float(value):
    return Decimal(value).quantize(Decimal('.00'))
