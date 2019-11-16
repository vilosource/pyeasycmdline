import logging
import pytest
from easycmdline.core.logging_setup import (
    setup_logging,
    get_command_logger,
    CommandContextFilter,
    LOG_LEVELS,
)


@pytest.fixture
def basic_config():
    """Basic configuration fixture"""
    return {
        "logging": {"default_level": "INFO", "format": "%(levelname)s - %(message)s"}
    }


@pytest.fixture
def command_config():
    """Configuration with command-specific logging levels"""
    return {
        "logging": {
            "default_level": "WARNING",
            "format": "%(levelname)s - %(message)s",
        },
        "commands": {
            "test": {
                "logging_level": "DEBUG",
                "subcommands": {"sub": {"logging_level": "INFO"}},
            },
            "normal": {},
        },
    }


def test_setup_logging(basic_config):
    """Test setting up logging system"""
    # Reset logging to default state
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Apply our configuration
    setup_logging(basic_config)

    # Check that configuration was applied
    assert logging.root.level == logging.INFO
    assert len(logging.root.handlers) > 0

    # Clean up
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


def test_get_command_logger_no_command_specific_config(command_config):
    """Test getting a logger for a command with no specific config"""
    logger = get_command_logger(["normal"], command_config)
    assert logger.level == logging.NOTSET  # Inherits from parent

    for filter_obj in logger.filters:
        if isinstance(filter_obj, CommandContextFilter):
            assert filter_obj.command_path == ["normal"]


def test_get_command_logger_with_command_specific_config(command_config):
    """Test getting a logger for a command with specific config"""
    logger = get_command_logger(["test"], command_config)
    assert logger.level == logging.DEBUG


def test_get_command_logger_with_nested_command(command_config):
    """Test getting a logger for a nested command"""
    logger = get_command_logger(["test", "sub"], command_config)
    assert logger.level == logging.INFO


def test_command_context_filter():
    """Test the CommandContextFilter functionality"""
    filter_obj = CommandContextFilter(["cmd", "subcmd"])

    # Create a test log record
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # Apply the filter
    result = filter_obj.filter(record)

    assert result is True  # Filter should always return True
    assert hasattr(record, "command_path")
    assert record.command_path == "cmd.subcmd"
