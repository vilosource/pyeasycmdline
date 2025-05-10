#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for the EasyCmdLine class functionality
"""
import os
import sys
import argparse
import logging
import pytest
from unittest.mock import MagicMock, patch, call
from typing import Dict, Any, List

from easycmdline.cli import EasyCmdLine
from easycmdline.core.config import load_config


@pytest.fixture
def mock_config():
    """
    Mock configuration for testing
    """
    return {
        "commands": {
            "simple": {
                "description": "A simple command",
                "command_class": "easycmdline.commands.simplecmd.SimpleCommand",
                "arguments": [
                    {
                        "name": "--message",
                        "help": "Message to display",
                        "default": "Hello",
                    }
                ],
            },
            "nested": {
                "description": "A command with subcommands",
                "subcommands": {
                    "sub": {
                        "description": "A subcommand",
                        "command_class": "easycmdline.commands.subcmd.SubCommand",
                        "arguments": [
                            {
                                "name": "--option",
                                "help": "An option",
                                "default": "value",
                            }
                        ],
                    }
                },
            },
            "command": {  # This one should be filtered out
                "description": "Should be filtered",
                "command_class": "easycmdline.commands.invalidcmd.InvalidCommand",
            },
        }
    }


@pytest.fixture
def cli_instance(mock_config):
    """
    Create a test instance of EasyCmdLine with mocked dependencies
    """
    with patch("easycmdline.cli.load_config", return_value=mock_config), patch(
        "easycmdline.cli.setup_logging"
    ), patch("easycmdline.cli.logging.getLogger"):

        cli = EasyCmdLine("mock_config.yml")
        cli.config = mock_config
        return cli


class TestGetFilteredCommands:
    """Test case for _get_filtered_commands method"""

    def test_filters_out_command_entry(self, cli_instance):
        """Should filter out the 'command' entry from commands dict"""
        commands = cli_instance._get_filtered_commands()

        # Should contain 'simple' and 'nested'
        assert "simple" in commands
        assert "nested" in commands

        # Should not contain 'command'
        assert "command" not in commands


class TestParseArguments:
    """Test case for _parse_arguments method"""

    def test_parse_with_explicit_args(self, cli_instance):
        """Should correctly parse explicitly provided args"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--test")

        args = cli_instance._parse_arguments(parser, ["--test", "value"])

        assert args.test == "value"

    @patch("easycmdline.cli.sys.argv", ["program", "--test", "value"])
    def test_parse_with_sys_argv(self, cli_instance):
        """Should use sys.argv when args is None"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--test")

        args = cli_instance._parse_arguments(parser, None)

        assert args.test == "value"

    @patch("easycmdline.cli.sys.argv", ["program", "config.yml", "--test", "value"])
    def test_parse_with_config_in_argv(self, cli_instance):
        """Should handle when config file is in argv"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--test")

        with patch(
            "easycmdline.cli.sys.argv", ["program", "config.yml", "--test", "value"]
        ):
            args = cli_instance._parse_arguments(parser, None)

        assert args.test == "value"


class TestNormalizeArgs:
    """Test case for _normalize_args method"""

    def test_adds_command_path_if_missing(self, cli_instance):
        """Should add _command_path if missing"""
        args = argparse.Namespace()

        args = cli_instance._normalize_args(args)

        assert hasattr(args, "_command_path")
        assert args._command_path == []

    def test_preserves_existing_command_path(self, cli_instance):
        """Should preserve existing _command_path"""
        args = argparse.Namespace(_command_path=["test", "path"])

        args = cli_instance._normalize_args(args)

        assert args._command_path == ["test", "path"]


class TestHasCommand:
    """Test case for _has_command method"""

    def test_with_command_path(self, cli_instance):
        """Should return True if args has _command_path"""
        args = argparse.Namespace(_command_path=["command"])

        assert cli_instance._has_command(args) is True

    def test_with_command_attribute(self, cli_instance):
        """Should return True if args has command attribute"""
        args = argparse.Namespace(command="command")

        assert cli_instance._has_command(args) is True

    def test_with_empty_command_path(self, cli_instance):
        """Should return False if _command_path is empty"""
        args = argparse.Namespace(_command_path=[])

        assert cli_instance._has_command(args) is False

    def test_with_non_namespace_args(self, cli_instance):
        """Should return False if args is not Namespace"""
        args = {"not": "namespace"}

        assert cli_instance._has_command(args) is False

    def test_no_command_info(self, cli_instance):
        """Should return False if no command info"""
        args = argparse.Namespace()

        assert cli_instance._has_command(args) is False


class TestGetCommandText:
    """Test case for _get_command_text method"""

    def test_with_command_path(self, cli_instance):
        """Should return space-joined _command_path"""
        args = argparse.Namespace(_command_path=["nested", "sub"])

        assert cli_instance._get_command_text(args) == "nested sub"

    def test_with_command_attribute(self, cli_instance):
        """Should return command attribute if no _command_path"""
        args = argparse.Namespace(command="simple")

        assert cli_instance._get_command_text(args) == "simple"

    def test_with_no_command_info(self, cli_instance):
        """Should return 'unknown' if no command info"""
        args = argparse.Namespace()

        assert cli_instance._get_command_text(args) == "unknown"

    def test_with_non_namespace_args(self, cli_instance):
        """Should return 'unknown' if args is not Namespace"""
        args = {"not": "namespace"}

        assert cli_instance._get_command_text(args) == "unknown"


class TestCreateAndRunCommand:
    """Test case for _create_and_run_command method"""

    def test_creates_and_runs_command(self, cli_instance):
        """Should import class, create command and run it"""
        cmd_cfg = {"command_class": "mock.command.Class"}
        args = argparse.Namespace(_command_path=["test"])
        cmd_logger = MagicMock()

        mock_command_class = MagicMock()
        mock_command_class.__name__ = "MockCommandClass"  # Add __name__ attribute
        mock_command = MagicMock()
        mock_command_class.return_value = mock_command
        mock_command.run.return_value = "result"

        with patch("easycmdline.cli.import_class", return_value=mock_command_class):
            result = cli_instance._create_and_run_command(cmd_cfg, args, cmd_logger)

        mock_command_class.assert_called_once_with(args, None)
        assert mock_command.run.call_count == 1
        assert result == "result"

    def test_creates_handler_if_specified(self, cli_instance):
        """Should create handler if specified in config"""
        cmd_cfg = {
            "command_class": "mock.command.Class",
            "handler_class": "mock.handler.Class",
        }
        args = argparse.Namespace(_command_path=["test"])
        cmd_logger = MagicMock()

        mock_command_class = MagicMock()
        mock_command_class.__name__ = "MockCommandClass"  # Add __name__ attribute
        mock_handler_class = MagicMock()
        mock_handler_class.__name__ = "MockHandlerClass"  # Add __name__ attribute
        mock_handler = MagicMock()
        mock_command = MagicMock()

        mock_handler_class.return_value = mock_handler
        mock_command_class.return_value = mock_command
        mock_command.run.return_value = "result"

        with patch(
            "easycmdline.cli.import_class",
            side_effect=[mock_command_class, mock_handler_class],
        ):
            result = cli_instance._create_and_run_command(cmd_cfg, args, cmd_logger)

        mock_handler_class.assert_called_once_with(args)
        mock_command_class.assert_called_once_with(args, mock_handler)
        assert mock_command.run.call_count == 1
        assert result == "result"


class TestCreateAndRunCommandErrors:
    """Test case for error handling in _create_and_run_command"""

    def test_handles_name_attribute_error(self, cli_instance):
        """Should handle AttributeError when accessing __name__"""
        cmd_cfg = {"command_class": "mock.command.Class"}
        args = argparse.Namespace(_command_path=["test"])
        cmd_logger = MagicMock()

        # Create a mock that raises AttributeError when __name__ is accessed
        mock_command_class = MagicMock()
        # Delete the __name__ attribute to cause getattr to use fallback
        del mock_command_class.__name__
        mock_command = MagicMock()
        mock_command_class.return_value = mock_command
        mock_command.run.return_value = "result"

        with patch("easycmdline.cli.import_class", return_value=mock_command_class):
            result = cli_instance._create_and_run_command(cmd_cfg, args, cmd_logger)

        # Verify the command still ran despite the AttributeError
        assert result == "result"

    def test_handler_name_attribute_error(self, cli_instance):
        """Should handle AttributeError when accessing handler __name__"""
        cmd_cfg = {
            "command_class": "mock.command.Class",
            "handler_class": "mock.handler.Class",
        }
        args = argparse.Namespace(_command_path=["test"])
        cmd_logger = MagicMock()

        # Create mocks
        mock_command_class = MagicMock()
        mock_command_class.__name__ = "MockCommandClass"

        # Create handler mock that raises AttributeError when __name__ is accessed
        mock_handler_class = MagicMock()
        del mock_handler_class.__name__  # Delete the attribute to trigger fallback

        mock_handler = MagicMock()
        mock_command = MagicMock()

        mock_handler_class.return_value = mock_handler
        mock_command_class.return_value = mock_command
        mock_command.run.return_value = "result"

        with patch(
            "easycmdline.cli.import_class",
            side_effect=[mock_command_class, mock_handler_class],
        ):
            result = cli_instance._create_and_run_command(cmd_cfg, args, cmd_logger)

        # Verify the command still ran despite the AttributeError
        assert result == "result"


class TestExecute:
    """Test case for execute method"""

    def test_prints_help_if_no_command(self, cli_instance):
        """Should print help if no command is specified"""
        mock_parser = MagicMock()
        mock_filtered_commands = {"simple": {}}

        with patch.object(
            cli_instance, "_get_filtered_commands", return_value=mock_filtered_commands
        ), patch.object(
            cli_instance, "create_parser", return_value=mock_parser
        ), patch.object(
            cli_instance, "_parse_arguments", return_value=argparse.Namespace()
        ), patch(
            "easycmdline.cli.get_command_logger"
        ):

            cli_instance.execute()

        mock_parser.print_help.assert_called_once()

    def test_executes_command(self, cli_instance):
        """Should resolve and execute command"""
        # Mock arguments with a command
        mock_args = argparse.Namespace(_command_path=["simple"])
        mock_cmd_cfg = {"command_class": "mock.command.Class"}
        mock_filtered_commands = {"simple": mock_cmd_cfg}
        mock_logger = MagicMock()

        # Create Mock objects for methods we want to verify
        mock_resolve_command = MagicMock(return_value=mock_cmd_cfg)
        mock_create_and_run_command = MagicMock(return_value="result")

        # Save original methods
        original_resolve_command = cli_instance.resolve_command
        original_create_and_run_command = cli_instance._create_and_run_command

        try:
            # Replace methods with mocks
            cli_instance.resolve_command = mock_resolve_command
            cli_instance._create_and_run_command = mock_create_and_run_command

            with patch.object(
                cli_instance,
                "_get_filtered_commands",
                return_value=mock_filtered_commands,
            ), patch.object(cli_instance, "create_parser"), patch.object(
                cli_instance, "_parse_arguments", return_value=mock_args
            ), patch(
                "easycmdline.cli.get_command_logger", return_value=mock_logger
            ):

                result = cli_instance.execute()

            # Verify method calls
            assert mock_resolve_command.call_count == 1
            assert mock_create_and_run_command.call_count == 1
            mock_create_and_run_command.assert_called_with(
                mock_cmd_cfg, mock_args, mock_logger
            )
            assert result == "result"

        finally:
            # Restore original methods
            cli_instance.resolve_command = original_resolve_command
            cli_instance._create_and_run_command = original_create_and_run_command

    def test_handles_exceptions(self, cli_instance):
        """Should handle and re-raise exceptions"""
        mock_args = argparse.Namespace(_command_path=["simple"])
        mock_filtered_commands = {"simple": {}}
        mock_logger = MagicMock()

        with patch.object(
            cli_instance, "_get_filtered_commands", return_value=mock_filtered_commands
        ), patch.object(cli_instance, "create_parser"), patch.object(
            cli_instance, "_parse_arguments", return_value=mock_args
        ), patch.object(
            cli_instance, "resolve_command", side_effect=ValueError("Test error")
        ), patch(
            "easycmdline.cli.get_command_logger", return_value=mock_logger
        ), pytest.raises(
            ValueError
        ):

            cli_instance.execute()

        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


class TestExecuteErrorHandling:
    """Test execution error handling scenarios"""

    def test_command_execution_error(self, cli_instance):
        """Should properly log and re-raise errors during command execution"""
        mock_args = argparse.Namespace(_command_path=["simple"])
        mock_cmd_cfg = {"command_class": "mock.command.Class"}
        mock_filtered_commands = {"simple": mock_cmd_cfg}
        mock_logger = MagicMock()

        with patch.object(
            cli_instance, "_get_filtered_commands", return_value=mock_filtered_commands
        ), patch.object(cli_instance, "create_parser"), patch.object(
            cli_instance, "_parse_arguments", return_value=mock_args
        ), patch.object(
            cli_instance, "resolve_command", return_value=mock_cmd_cfg
        ), patch.object(
            cli_instance,
            "_create_and_run_command",
            side_effect=RuntimeError("Execution failed"),
        ), patch(
            "easycmdline.cli.get_command_logger", return_value=mock_logger
        ), pytest.raises(
            RuntimeError
        ):

            cli_instance.execute()

        # Verify error is logged
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


class TestResolveByCommandPath:
    """Test case for _resolve_by_command_path method"""

    def test_command_not_found_error(self, cli_instance):
        """Should raise ValueError if command not found in path"""
        cmd_path = ["nonexistent", "command"]
        commands = {"existing": {"description": "Exists"}}

        with patch("easycmdline.cli.get_command_logger"), pytest.raises(
            ValueError
        ) as excinfo:
            cli_instance._resolve_by_command_path(cmd_path, commands)

        assert "Command 'nonexistent' not found" in str(excinfo.value)

    def test_no_subcommands_error(self, cli_instance):
        """Should raise ValueError if path continues beyond leaf command"""
        cmd_path = ["simple", "nonexistent"]
        commands = {"simple": {"description": "Simple command with no subcommands"}}

        with patch("easycmdline.cli.get_command_logger"), pytest.raises(
            ValueError
        ) as excinfo:
            cli_instance._resolve_by_command_path(cmd_path, commands)

        assert "has no subcommands but path continues" in str(excinfo.value)

    def test_empty_path_error(self, cli_instance):
        """Should raise ValueError if path is empty"""
        cmd_path = []
        commands = {"simple": {"description": "Simple command"}}

        with patch("easycmdline.cli.get_command_logger"), pytest.raises(
            ValueError
        ) as excinfo:
            cli_instance._resolve_by_command_path(cmd_path, commands)

        assert "Empty command path" in str(excinfo.value)


class TestResolveByCommandAttribute:
    """Test case for _resolve_by_command_attribute method"""

    def test_command_not_found_error(self, cli_instance):
        """Should raise ValueError if command not found in args"""
        args = argparse.Namespace(command="nonexistent")
        commands = {"existing": {"description": "Exists"}}

        with pytest.raises(ValueError) as excinfo:
            cli_instance._resolve_by_command_attribute(args, commands)

        assert "Could not resolve command configuration" in str(excinfo.value)

    def test_resolves_nested_subcommand(self, cli_instance):
        """Should resolve nested subcommand using command attribute"""
        # Create nested structure with command+subcommand_0+nested_cmd
        nested_cmd_cfg = {"command_class": "nested.command"}
        subcommands = {"nested_cmd": nested_cmd_cfg}
        cmd_cfg = {"subcommands": subcommands}
        commands = {"main_cmd": cmd_cfg}

        # Setup args with command and command_0 set
        args = argparse.Namespace(
            command="main_cmd",
            command_0="nested_cmd",
        )

        # Mock resolve_command to handle recursive call
        with patch.object(cli_instance, "resolve_command", return_value=nested_cmd_cfg):
            result = cli_instance._resolve_by_command_attribute(args, commands)

        assert result == nested_cmd_cfg


class TestEasyCmdLineIntegration:
    """Integration tests for EasyCmdLine class"""

    def test_full_command_execution_flow(self, cli_instance):
        """
        Test the full command execution flow
        This is an integration test that ensures all methods work together
        """
        # Create mock classes for command execution
        mock_command_class = MagicMock()
        mock_command = MagicMock()
        mock_command_class.return_value = mock_command
        mock_command.run.return_value = "command result"

        # Setup nested command structure to verify subcommand resolution
        mock_config = {
            "commands": {
                "parent": {
                    "description": "Parent command",
                    "subcommands": {
                        "child": {
                            "description": "Child command",
                            "command_class": "mock.ChildCommand",
                            "arguments": [{"name": "--option", "help": "An option"}],
                        }
                    },
                }
            }
        }

        # Mock command line arguments
        mock_args = ["parent", "child", "--option", "value"]

        with patch.object(cli_instance, "config", mock_config), patch(
            "easycmdline.cli.import_class", return_value=mock_command_class
        ), patch("easycmdline.cli.get_command_logger"), patch.object(
            argparse.ArgumentParser,
            "parse_args",
            return_value=argparse.Namespace(
                _command_path=["parent", "child"], option="value"
            ),
        ):

            result = cli_instance.execute(mock_args)

        # Verify command was executed
        assert result == "command result"
        assert mock_command.run.call_count == 1

    def test_end_to_end_with_handler(self, cli_instance):
        """
        End-to-end test with a handler class
        Tests the complete flow including handler creation
        """
        # Create mock classes for command and handler
        mock_command_class = MagicMock()
        mock_handler_class = MagicMock()
        mock_handler = MagicMock()
        mock_command = MagicMock()

        mock_handler_class.return_value = mock_handler
        mock_command_class.return_value = mock_command
        mock_command.run.return_value = "command with handler result"

        # Setup command with handler
        mock_config = {
            "commands": {
                "cmd": {
                    "description": "Command with handler",
                    "command_class": "mock.TestCommand",
                    "handler_class": "mock.TestHandler",
                    "arguments": [{"name": "--option", "help": "An option"}],
                }
            }
        }

        # Mock command line arguments
        mock_args = ["cmd", "--option", "value"]

        with patch.object(cli_instance, "config", mock_config), patch(
            "easycmdline.cli.import_class",
            side_effect=[mock_command_class, mock_handler_class],
        ), patch("easycmdline.cli.get_command_logger"), patch.object(
            argparse.ArgumentParser,
            "parse_args",
            return_value=argparse.Namespace(
                _command_path=["cmd"], option="value", command="cmd"
            ),
        ):

            result = cli_instance.execute(mock_args)

        # Verify command and handler were created and used
        assert result == "command with handler result"
        assert mock_handler_class.call_count == 1
        assert mock_command_class.call_count == 1
        assert mock_command.run.call_count == 1


class TestInitialization:
    """Test case for EasyCmdLine initialization"""

    @patch("os.path.dirname")
    @patch("os.path.abspath")
    @patch("os.path.join")
    @patch("easycmdline.cli.load_config")
    @patch("easycmdline.cli.setup_logging")
    @patch("easycmdline.cli.logging.getLogger")
    def test_default_config_file_path(
        self,
        mock_getLogger,
        mock_setup_logging,
        mock_load_config,
        mock_join,
        mock_abspath,
        mock_dirname,
    ):
        """Should use default config file path if not provided"""
        # Setup mocks
        mock_dirname.return_value = "/mock/package/dir"
        mock_abspath.return_value = "/mock/package/dir/cli.py"
        mock_join.return_value = "/mock/package/dir/easycmdline-config.yml"
        mock_load_config.return_value = {"commands": {}}

        # Test with no config file
        with patch.dict("os.environ", {}, clear=True):
            cli = EasyCmdLine()

        # Verify correct path construction
        mock_dirname.assert_called_once_with(mock_abspath.return_value)
        mock_join.assert_called_once_with("/mock/package/dir", "easycmdline-config.yml")
        assert cli.config_file == "/mock/package/dir/easycmdline-config.yml"

    @patch("easycmdline.cli.load_config")
    @patch("easycmdline.cli.setup_logging")
    @patch("easycmdline.cli.logging.getLogger")
    def test_env_var_config_file_path(
        self, mock_getLogger, mock_setup_logging, mock_load_config
    ):
        """Should use config file path from environment variable if set"""
        mock_load_config.return_value = {"commands": {}}

        # Test with environment variable
        with patch.dict(
            "os.environ", {"EASYCMDLINE_CONFIG": "/env/var/config.yml"}, clear=True
        ):
            cli = EasyCmdLine()

        assert cli.config_file == "/env/var/config.yml"


def test_entrypoint_function():
    """Test the run() function which serves as the entrypoint"""

    mock_config = {"commands": {"test": {"description": "Test command"}}}
    mock_cli = MagicMock()
    mock_cli.return_value.execute.return_value = "entrypoint result"

    with patch(
        "easycmdline.cli.EasyCmdLine", return_value=mock_cli.return_value
    ), patch("easycmdline.cli.load_config", return_value=mock_config), patch.dict(
        "os.environ", {"EASYCMDLINE_DEBUG": "1"}, clear=True
    ), patch(
        "easycmdline.cli.logging"
    ):

        from easycmdline.cli import run

        run("test_config.yml")

    mock_cli.return_value.execute.assert_called_once()


class TestRunFunction:
    """Test the run() entrypoint function"""

    def test_with_debug_environment_var(self):
        """Should set debug level when EASYCMDLINE_DEBUG is set"""
        mock_cli = MagicMock()
        mock_cli.execute.return_value = "debug result"
        logger_mock = MagicMock()

        with patch("easycmdline.cli.EasyCmdLine", return_value=mock_cli), patch.dict(
            "os.environ", {"EASYCMDLINE_DEBUG": "1"}, clear=True
        ), patch("easycmdline.cli.sys.exit") as mock_exit, patch(
            "easycmdline.cli.logging.debug"
        ) as mock_debug, patch(
            "easycmdline.cli.logging.getLogger"
        ) as mock_getLogger, patch(
            "easycmdline.cli.load_config"
        ):

            mock_getLogger.return_value = logger_mock

            from easycmdline.cli import run

            result = run("test_config.yml")

        # Verify debug was used
        mock_debug.assert_any_call("Debug logging enabled")
        assert result == "debug result"

    def test_config_file_from_argv(self):
        """Should use config file from sys.argv if provided"""
        mock_cli = MagicMock()
        mock_cli.execute.return_value = "argv result"

        # Mock the command line arguments
        mock_argv = ["program", "custom-config.yml"]

        with patch("easycmdline.cli.EasyCmdLine", return_value=mock_cli), patch(
            "easycmdline.cli.sys.argv", mock_argv
        ), patch("easycmdline.cli.os.path.dirname", return_value="/mock/path"), patch(
            "easycmdline.cli.os.path.abspath"
        ), patch(
            "easycmdline.cli.os.path.join", return_value="/mock/path/custom-config.yml"
        ), patch(
            "easycmdline.cli.sys.exit"
        ), patch(
            "easycmdline.cli.load_config"
        ):

            from easycmdline.cli import run

            result = run()

        # Verify correct config file was used
        mock_cli.execute.assert_called_once()
        assert result == "argv result"

    def test_handles_exceptions(self):
        """Should handle exceptions and exit with error code 1"""
        with patch(
            "easycmdline.cli.EasyCmdLine", side_effect=ValueError("Test error")
        ), patch("easycmdline.cli.logging.error") as mock_error, patch(
            "easycmdline.cli.sys.exit"
        ) as mock_exit, patch(
            "easycmdline.cli.load_config"
        ):

            from easycmdline.cli import run

            run()

        # Verify error handling
        mock_error.assert_called_once()
        mock_exit.assert_called_once_with(1)

    def test_exception_with_debug_mode(self):
        """Should log detailed exception info when in debug mode"""
        with patch(
            "easycmdline.cli.EasyCmdLine", side_effect=ValueError("Debug test error")
        ), patch("easycmdline.cli.logging.error"), patch(
            "easycmdline.cli.logging.debug"
        ) as mock_debug, patch(
            "easycmdline.cli.sys.exit"
        ), patch.dict(
            "os.environ", {"EASYCMDLINE_DEBUG": "1"}, clear=True
        ), patch(
            "easycmdline.cli.load_config"
        ):

            from easycmdline.cli import run

            run()

        # Verify debug logging of exception details with exc_info
        assert mock_debug.call_count >= 1  # Called at least once
        mock_debug.assert_any_call("Exception details:", exc_info=True)
