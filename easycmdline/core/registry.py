"""
Module for dynamically importing and registering classes.
This module provides utility functions to import classes by their string path.
"""

from typing import Type, Any, cast
import importlib


def import_class(class_path: str) -> Type[Any]:
    """
    Import a class dynamically from a string path.

    Args:
        class_path: String representation of the class path in format 'module.submodule.ClassName'

    Returns:
        The class object
    """
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    # Use cast to ensure the return type matches the declared type
    return cast(Type[Any], getattr(module, class_name))
