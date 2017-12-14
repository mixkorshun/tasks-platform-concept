from datetime import datetime

import jwt

from project import settings

secret_key = 'session:' + settings.SECRET_KEY


def get_token(request, user_id):
    return jwt.encode({
        'uid': user_id,
        'ts': datetime.utcnow().timestamp(),
        'ip': request.remote_addr
    }, secret_key).decode()


def get_user_id(request, token):
    data = jwt.decode(token.encode(), secret_key)

    if data.get('ip') != request.remote_addr:
        return None

    if datetime.utcnow().timestamp() - (data.get('ts') or 0) > 3600 * 6:
        return None

    return data['uid']


DecodeError = jwt.DecodeError
