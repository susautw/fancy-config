class ClassNotFoundException(Exception):
    """
    Exception raised when a class is not found.
    """
    def __init__(self, cls: str, *args):
        super().__init__(f'Class "{cls}" is not found.', *args)


class ContextNotLoadedError(RuntimeError):
    """
    Error raised when getting a context that is not loaded.
    """


class DuplicatedNameError(RuntimeError):
    """
    Detects a config class has duplicated name in its placeholders.
    """