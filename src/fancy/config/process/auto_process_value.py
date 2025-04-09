from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .. import ConfigContext


def auto_process_value(raw_val: Any, transform: Callable[[Any], Any], context: "ConfigContext") -> Any:
    """
    Process a raw value using a transform function and configuration context.
    
    This function applies the provided transform function to the raw value and handles
    special cases for ConfigStructure instances, ensuring they're properly loaded
    with the given context.
    
    :param raw_val: The original value to be processed
    :param transform: A function that converts the raw value to the target type
    :param context: The configuration context used for loading structures
    :return: The processed value
    
    .. note::
        If the target value is a :class:`ConfigStructure` and it wasn't be loaded, 
        it will be loaded with the context.
    """

    from .. import ConfigStructure
    value = transform(raw_val)
    if isinstance(value, ConfigStructure):
        if not value.loaded:
            value.load_by_context(context, raw_val)
    return value
