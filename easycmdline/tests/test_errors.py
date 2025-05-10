"""
Tests for the custom error classes in the errors module.
"""

from easycmdline.core.errors import CommandError, ConfigError, HandlerError


def test_command_error():
    """Test the CommandError exception"""
    error = CommandError("Test command error")
    assert str(error) == "Test command error"

    # Test with command name
    error = CommandError("Test command error", command_name="test_command")
    assert "Command 'test_command'" in str(error)
    assert "Test command error" in str(error)


def test_config_error():
    """Test the ConfigError exception"""
    error = ConfigError("Test config error")
    assert str(error) == "Test config error"

    # Test with config file path
    error = ConfigError("Test config error", config_path="test_config.yml")
    assert "Configuration error in 'test_config.yml'" in str(error)
    assert "Test config error" in str(error)


def test_handler_error():
    """Test the HandlerError exception"""
    error = HandlerError("Test handler error")
    assert str(error) == "Test handler error"

    # Test with handler name
    error = HandlerError("Test handler error", handler_name="TestHandler")
    assert "Handler 'TestHandler'" in str(error)
    assert "Test handler error" in str(error)
