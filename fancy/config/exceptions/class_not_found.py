class ClassNotFoundException(Exception):
    def __init__(self, cls: str):
        super().__init__(f'Class "{cls}" is not found.')
