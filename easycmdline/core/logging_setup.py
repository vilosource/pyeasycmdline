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
        if not hasattr(record, "command_path"):
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
    # Replace %(command_path)s with main if it exists in the format to avoid KeyError
    log_format = log_config.get("format", DEFAULT_LOG_FORMAT)
    if "%(command_path)s" in log_format:
        # Fix the format to use a default value for command_path
        log_format = log_format.replace("%(command_path)s", "main")

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(default_level)

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler with proper formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)

    # Make sure all root logger handlers have a CommandContextFilter
    command_filter = CommandContextFilter([])
    if not any(isinstance(f, CommandContextFilter) for f in root_logger.filters):
        root_logger.addFilter(command_filter)


def _build_logger_name(command_path: list) -> str:
    """
    Build a logger name based on the command path.

    Args:
        command_path: List representing the path to the command

    Returns:
        Formatted logger name
    """
    return (
        f"easycmdline.command.{'.'.join(command_path)}"
        if command_path
        else "easycmdline"
    )


def _find_command_log_level(
    command_path: list, config: Dict[str, Any]
) -> Optional[int]:
    """
    Find the appropriate log level for a command by traversing its hierarchy.

    Args:
        command_path: List representing the path to the command
        config: Full application configuration

    Returns:
        Log level if found, otherwise None
    """
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

    return level


def _ensure_command_context_filter(logger: logging.Logger, command_path: list) -> None:
    """
    Ensure the logger has a CommandContextFilter applied to add command path context to log records.

    A CommandContextFilter is a logging filter that enriches log records with command path
    information. This makes it possible to identify which command generated a particular log
    message, which is especially useful in applications with nested command hierarchies.

    This function checks if the logger already has a CommandContextFilter attached.
    If not, it creates a new filter with the provided command path and adds it to
    the logger. The filter adds a 'command_path' attribute to all log records processed
    by this logger, which is used in log formatting patterns like '%(command_path)s'.

    Args:
        logger: Logger to configure with the context filter
        command_path: List representing the path to the command, used to create the filter
    """
    has_filter = any(isinstance(f, CommandContextFilter) for f in logger.filters)
    if not has_filter:
        context_filter = CommandContextFilter(command_path)
        logger.addFilter(context_filter)


def get_command_logger(command_path: list, config: Dict[str, Any]) -> logging.Logger:
    """
    Get a logger for a specific command with the appropriate level

    Args:
        command_path: List representing the path to the command
        config: Full application configuration

    Returns:
        Logger configured for the command
    """
    # Get a logger with the appropriate name
    logger_name = _build_logger_name(command_path)
    logger = logging.getLogger(logger_name)

    # Set the appropriate log level if found in the command hierarchy
    level = _find_command_log_level(command_path, config)
    if level is not None:
        logger.setLevel(level)

    # Ensure the logger has a command context filter
    _ensure_command_context_filter(logger, command_path)

    return logger
