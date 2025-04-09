from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .. import ConfigContext


def auto_process_value(raw_val: Any, transform: Callable[[Any], Any], context: "ConfigContext") -> Any:
    """
    Process the raw value to the target value with transform.

    .. note::
        If the target value is a :class:`ConfigStructure` and it wasn't be loaded, it will be loaded with the context.
    """

    from .. import ConfigStructure
    value = transform(raw_val)
    if isinstance(value, ConfigStructure):
        if not value.loaded:
            value.load_by_context(context, raw_val)
    return value
