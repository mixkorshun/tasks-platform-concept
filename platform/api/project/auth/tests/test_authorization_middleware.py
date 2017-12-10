from flask import request

from .. import tokens
from ..models import Store


def test_forbidden_when_no_header(client):
    client.get('/', headers=[])

    assert request.session is None


def test_forbidden_when_invalid_type(client):
    client.get('/', headers=[
        ('Authorization', 'basic abacaba:abacaba')
    ])

    assert request.session is None


def test_forbidden_when_empty_token(client):
    client.get('/', headers=[
        ('Authorization', 'Token')
    ])

    assert request.session is None


def test_forbidden_when_invalid_token(client):
    client.get('/', headers=[
        ('Authorization', 'Token abacaba')
    ])

    assert request.session is None


def test_valid_token(client):
    token = tokens.encode(Store(user_id=12))

    client.get('/', headers=[
        ('Authorization', 'Token %s' % token)
    ])

    assert request.session.user_id == 12
