class CannotCreateException(Exception):
    def __init__(self, message: str = "Cannot create resource"):
        self.message = message
        super().__init__(self.message)