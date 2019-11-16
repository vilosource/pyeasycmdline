"""
Custom exception classes for the easycmdline package.
"""


class CommandError(Exception):
    """
    Exception raised for errors in command execution.
    """

    def __init__(self, message, command_name=None):
        self.message = message
        self.command_name = command_name
        super().__init__(
            f"Command '{command_name}': {message}" if command_name else message
        )


class ConfigError(Exception):
    """
    Exception raised for errors in configuration.
    """

    def __init__(self, message, config_path=None):
        self.message = message
        self.config_path = config_path
        super().__init__(
            f"Configuration error in '{config_path}': {message}"
            if config_path
            else message
        )


class HandlerError(Exception):
    """
    Exception raised for errors in handlers.
    """

    def __init__(self, message, handler_name=None):
        self.message = message
        self.handler_name = handler_name
        super().__init__(
            f"Handler '{handler_name}': {message}" if handler_name else message
        )
