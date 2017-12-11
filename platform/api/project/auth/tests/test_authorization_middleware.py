from flask import request

from .. import tokens


def test_forbidden_when_no_header(client):
    client.get('/', headers=[])

    assert request.user_id is None


def test_forbidden_when_invalid_type(client):
    client.get('/', headers=[
        ('Authorization', 'basic abacaba:abacaba')
    ])

    assert request.user_id is None


def test_forbidden_when_empty_token(client):
    client.get('/', headers=[
        ('Authorization', 'Token')
    ])

    assert request.user_id is None


def test_forbidden_when_invalid_token(client):
    client.get('/', headers=[
        ('Authorization', 'Token abacaba')
    ])

    assert request.user_id is None


def test_valid_token(client):
    token = tokens.get_token(12)

    client.get('/', headers=[
        ('Authorization', 'Token %s' % token)
    ])

    assert request.user_id == 12
