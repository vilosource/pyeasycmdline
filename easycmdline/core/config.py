from typing import Dict, Any, cast
import yaml


def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path) as file:
        # Use cast to ensure the return type matches the declared type
        return cast(Dict[str, Any], yaml.safe_load(file))
