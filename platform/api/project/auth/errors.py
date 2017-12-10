class InvalidCredentials(Exception):
    code = 'invalid_credentials'
    message = 'Incorrect email or password.'

    def __init__(self, message=None):
        if message:
            self.message = message
