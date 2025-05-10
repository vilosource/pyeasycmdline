from typing import Type, Any, Tuple, cast
import importlib


def import_class(class_path: str) -> Type[Any]:
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    # Use cast to ensure the return type matches the declared type
    return cast(Type[Any], getattr(module, class_name))
