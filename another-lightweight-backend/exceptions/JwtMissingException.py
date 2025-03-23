class JwtMissingException(Exception):
    '''
    - The Jwt in the Authorization header is missing
    '''
    def __init__(self, message='The Jwt in the Authorization header is missing'):
        self.message = message
        super().__init__(self.message)