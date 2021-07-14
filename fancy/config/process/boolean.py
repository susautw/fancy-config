from typing import Any, AbstractSet

TRUE_CHOICES = {"on", "1", "true", "yes", "==TRUE=="}
FALSE_CHOICES = {"off", "0", "false", "no", "==FALSE=="}


def make_boolean(true_choices: AbstractSet = None, false_choices: AbstractSet = None):
    def _inner(value):
        return boolean(value, true_choices, false_choices)
    return _inner


def boolean(value: Any, true_choices: AbstractSet = None, false_choices: AbstractSet = None) -> bool:
    if true_choices is None:
        true_choices = TRUE_CHOICES
    if false_choices is None:
        false_choices = FALSE_CHOICES
    if isinstance(value, str):
        _value = value.strip()
        if _value in true_choices:
            return True
        if _value in false_choices:
            return False
        raise ValueError(
            f"unexpected value: {value}, expected choices:"
            f" {str(true_choices.union(false_choices))}"
        )
    return bool(value)
