# Style Guidelines

## Module

```python
"""
Module docstring.

* Avoid writing module docstrings when the module is containing only one public class.
"""

...
```


## Class

```python
class MyClass:
    """
    This is a docstring for MyClass.

    It describes the purpose of the class and its usage.

    * Don't put parameters in the class docstring.
    """

    member_variable: int
    """
    This is a docstring for member_variable.
    """

    def __init__(self, value: int):
        """
        This is a docstring for the __init__ method.

        * constructor should be the first method in the class.

        :param value: The value to initialize the member variable.
        """
        self.member_variable = value

    def public_method(self, param: int) -> None:
        """
        This is a docstring for the public_method.

        It describes what the method does.

        * Public methods should be documented in Sphinx style.
        * Public methods should write before private methods.

        :param param: The parameter for the method.
        :return: None
        :raises ValueError: If the parameter is invalid.
        """

    def _util_private_method(self, param: int) -> None:
        """
        This is a docstring for the _util_private_method.

        * A simple private method should avoid docstrings.

        :param param: The parameter for the method.
        :return: None
        """

    def _private_method1(self, param: int) -> None:
        """
        This is a docstring for the _private_method1.

        * A simple private method should avoid docstrings.
        :param param: The parameter for the method.
        :return: None
        """
        self._util_private_method(param)
        self._private_method2(param)


    def _private_method2(self, param: int) -> None:
        """
        This is a docstring for the _private_method2.

        * This method should write after the _private_method1 because it is called by it.

        * A simple private method should avoid docstrings.
        :param param: The parameter for the method.
        :return: None
        """
        self._util_private_method(param)

```


## Function

```python
def my_function(param1: int, param2: str) -> None:
    """
    This is a docstring for the my_function.

    It describes what the function does.

    * Functions should be documented in Sphinx style.
    * Functions should write before private functions.

    :param param1: The first parameter.
    :param param2: The second parameter.
    :return: None
    :raises ValueError: If the parameters are invalid.
    """
```

