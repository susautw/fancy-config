class ClassNotFoundException(Exception):
    def __init__(self, cls: str, *args):
        super().__init__(f'Class "{cls}" is not found.', *args)


class ContextNotLoadedError(RuntimeError):
    pass
