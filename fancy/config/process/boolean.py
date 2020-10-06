from typing import Any

TRUE_CHOICES = {"on", "1", "true", "yes", "==TRUE=="}
FALSE_CHOICES = {"off", "0", "false", "no", "==FALSE=="}


def boolean(value: Any) -> bool:
    if isinstance(value, str):
        _value = value.lower().strip()
        if _value in TRUE_CHOICES:
            return True
        if _value in FALSE_CHOICES:
            return False
        raise ValueError(
            f"unexpected value: {value}, expected choices:"
            f" {str(TRUE_CHOICES.union(FALSE_CHOICES))}"
        )
    return bool(value)
