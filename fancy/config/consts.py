IGNORED_NAME = '_'
"""
Create a placeholder with this name will cause the placeholder cannot be loaded using a ConfigLoader

.. note:: It can be use with cfg.Lazy. A Lazy with this name will be ignored in to_dict and __setitem__ of its owner

.. warning:: Don't use it with required=True
"""