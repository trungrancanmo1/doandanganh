class CustomException(Exception):
    '''
    - The template for a custom exception
    '''
    def __init__(self, message='default message'):
        self.message = message
        super().__init__(self.message)