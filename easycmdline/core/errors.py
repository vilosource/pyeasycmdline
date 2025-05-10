"""
Custom exception classes for the easycmdline package.
"""

from typing import Optional


class CommandError(Exception):
    """
    Exception raised for errors in command execution.
    """

    def __init__(self, message: str, command_name: Optional[str] = None):
        self.message: str = message
        self.command_name: Optional[str] = command_name
        super().__init__(
            f"Command '{command_name}': {message}" if command_name else message
        )


class ConfigError(Exception):
    """
    Exception raised for errors in configuration.
    """

    def __init__(self, message: str, config_path: Optional[str] = None):
        self.message: str = message
        self.config_path: Optional[str] = config_path
        super().__init__(
            f"Configuration error in '{config_path}': {message}"
            if config_path
            else message
        )


class HandlerError(Exception):
    """
    Exception raised for errors in handlers.
    """

    def __init__(self, message: str, handler_name: Optional[str] = None):
        self.message: str = message
        self.handler_name: Optional[str] = handler_name
        super().__init__(
            f"Handler '{handler_name}': {message}" if handler_name else message
        )
