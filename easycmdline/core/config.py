"""
Configuration module for loading YAML configuration files.
This module provides utility functions for loading and parsing configuration files.
"""

from typing import Dict, Any, cast
import yaml


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        Dictionary containing the parsed YAML configuration
    """
    with open(config_path, encoding="utf-8") as file:
        # Use cast to ensure the return type matches the declared type
        return cast(Dict[str, Any], yaml.safe_load(file))
