import logging
import os
from typing import Dict, Any, Optional

# Default logging configuration
DEFAULT_LOG_LEVEL = "WARNING"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Map string log levels to logging module constants
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class CommandContextFilter(logging.Filter):
    """Adds command context to log records"""

    def __init__(self, command_path=None):
        super().__init__()
        self.command_path = command_path or []

    def filter(self, record):
        record.command_path = (
            ".".join(self.command_path) if self.command_path else "main"
        )
        return True


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Set up logging based on configuration dictionary

    Args:
        config: Dictionary containing logging configuration
    """
    log_config = config.get("logging", {})

    # Get default level from config or environment, fallback to WARNING
    default_level_name = (
        log_config.get("default_level")
        or os.environ.get("EASYCMDLINE_LOG_LEVEL")
        or DEFAULT_LOG_LEVEL
    )
    default_level = LOG_LEVELS.get(default_level_name.upper(), logging.WARNING)

    # Get format from config or use default
    log_format = log_config.get("format", DEFAULT_LOG_FORMAT)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(default_level)

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)


def get_command_logger(command_path: list, config: Dict[str, Any]) -> logging.Logger:
    """
    Get a logger for a specific command with the appropriate level

    Args:
        command_path: List representing the path to the command
        config: Full application configuration

    Returns:
        Logger configured for the command
    """
    # Create logger name based on command path
    logger_name = (
        f"easycmdline.command.{'.'.join(command_path)}"
        if command_path
        else "easycmdline"
    )
    logger = logging.getLogger(logger_name)

    # Determine log level for this command by traversing the command hierarchy
    level = None
    current_config = config.get("commands", {})
    current_path = []

    for cmd in command_path:
        current_path.append(cmd)
        if cmd in current_config:
            cmd_config = current_config[cmd]

            # Check if this command has a logging level
            if "logging_level" in cmd_config:
                level_name = cmd_config["logging_level"].upper()
                level = LOG_LEVELS.get(level_name)

            # Move to subcommands
            current_config = cmd_config.get("subcommands", {})
        else:
            break

    # If a level was found in the command hierarchy, set it
    if level is not None:
        logger.setLevel(level)

    # Add context filter to add command path info to log records
    context_filter = CommandContextFilter(command_path)
    logger.addFilter(context_filter)

    return logger
