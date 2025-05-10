import argparse
import logging
import os
import sys
from typing import Dict, Any, List, Optional
from easycmdline.core.config import load_config
from easycmdline.core.registry import import_class
from easycmdline.core.logging_setup import setup_logging, get_command_logger

# Basic logging setup until we load config
logging.basicConfig(
    level=logging.WARNING,  # Default to WARNING
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class EasyCmdLine:
    """
    A class-based implementation of the easycmdline framework that can be used
    programmatically or as a command-line interface.
    """

    def __init__(self, config_file=None):
        """
        Initialize the EasyCmdLine with a configuration file.

        Args:
            config_file: Path to the YAML configuration file
        """
        if not config_file:
            # Look for config file in the package directory if not specified
            config_file = os.environ.get("EASYCMDLINE_CONFIG")
            if not config_file:
                package_dir = os.path.dirname(os.path.abspath(__file__))
                config_file = os.path.join(package_dir, "easycmdline-config.yml")

        self.config_file = config_file
        self.logger = logging.getLogger(__name__)

        # Load configuration early to set up logging properly
        self.config = load_config(self.config_file)
        setup_logging(self.config)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Loaded configuration from {self.config_file}")

    def create_subparsers(self, parser, commands, parents=None):
        """Create subparsers for commands with tracking of parent commands"""
        if parents is None:
            parents = []

        self.logger.debug(
            f"Creating subparsers for commands: {list(commands.keys())} with parents: {parents}"
        )
        subparsers = parser.add_subparsers(
            dest="command" if not parents else f"command_{len(parents)}"
        )

        for name, cfg in commands.items():
            current_path = parents + [name]
            subparser = subparsers.add_parser(name, help=cfg.get("description", ""))

            # Store full command path in parser defaults to track hierarchy
            path_key = "_command_path"
            subparser.set_defaults(**{path_key: current_path})

            # Add arguments if any
            for arg_cfg in cfg.get("arguments", []):
                arg_name = arg_cfg.pop("name")
                subparser.add_argument(arg_name, **arg_cfg)

            # Handle nested subcommands
            if "subcommands" in cfg:
                self.create_subparsers(subparser, cfg["subcommands"], current_path)

    def _extract_command_path(self, args: Any) -> List[str]:
        """
        Extract the command path from arguments if available.

        Command paths represent the hierarchical structure of nested commands
        (e.g., ['remote', 'origin', 'add']). They are stored in the '_command_path'
        attribute of the args Namespace by the argument parser.

        Args:
            args: Command line arguments, typically an argparse.Namespace

        Returns:
            List of command names forming a path, or empty list if not available
        """
        if isinstance(args, argparse.Namespace) and hasattr(args, "_command_path"):
            cmd_path = args._command_path
            self.logger.debug(f"Found command path: {cmd_path}")
            return cmd_path
        return []

    def _resolve_by_command_path(
        self, cmd_path: List[str], commands: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve command configuration by traversing the command path hierarchy.

        This method navigates through the nested command configuration structure
        to find the command configuration that matches the provided command path.

        Args:
            cmd_path: List of command names forming a path
            commands: Dictionary containing command configurations

        Returns:
            Command configuration dictionary

        Raises:
            ValueError: If a command in the path doesn't exist or a path continues
                       beyond a leaf command
        """
        # Get a logger specific to this command path
        cmd_logger = get_command_logger(cmd_path, self.config)
        cmd_logger.debug(f"Processing command: {' '.join(cmd_path)}")

        # Navigate through command hierarchy
        current_commands = commands
        for i, cmd in enumerate(cmd_path):
            if cmd not in current_commands:
                err_msg = f"Command '{cmd}' not found in path {cmd_path[:i]}"
                cmd_logger.error(err_msg)
                raise ValueError(err_msg)

            cmd_cfg = current_commands[cmd]

            # If this is the last part of the path, return it
            if i == len(cmd_path) - 1:
                cmd_cfg_typed: Dict[str, Any] = cmd_cfg
                return cmd_cfg_typed

            # Otherwise, move to the next level of subcommands
            if "subcommands" not in cmd_cfg:
                err_msg = f"Command '{cmd}' has no subcommands but path continues"
                cmd_logger.error(err_msg)
                raise ValueError(err_msg)

            current_commands = cmd_cfg["subcommands"]

        # This should never be reached if cmd_path is non-empty,
        # but we include it for completeness
        raise ValueError("Empty command path")

    def _resolve_by_command_attribute(
        self, args: Any, commands: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback to resolve command using the 'command' attribute.

        This handles the case for simple (non-nested) command structures where
        commands are identified by a single 'command' attribute in args.

        Args:
            args: Command line arguments, typically an argparse.Namespace
            commands: Dictionary containing command configurations

        Returns:
            Command configuration dictionary

        Raises:
            ValueError: If the command doesn't exist
        """
        if hasattr(args, "command") and args.command in commands:
            cmd_cfg = commands[args.command]
            if "subcommands" in cmd_cfg:
                return self.resolve_command(args, cmd_cfg["subcommands"])
            fallback_cfg: Dict[str, Any] = cmd_cfg
            return fallback_cfg

        err_msg = "Could not resolve command configuration"
        self.logger.error(err_msg)
        raise ValueError(err_msg)

    def resolve_command(self, args: Any, commands: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve command configuration from args using the command path or command attribute.

        This method determines which command should be executed based on the parsed command
        line arguments. It first tries to use the '_command_path' attribute for nested commands,
        and falls back to the 'command' attribute for simple commands.

        Args:
            args: Command line arguments, typically an argparse.Namespace
            commands: Dictionary of available commands from configuration

        Returns:
            Command configuration dictionary for the selected command

        Raises:
            ValueError: If no valid command can be resolved from the arguments
        """
        if isinstance(args, argparse.Namespace):
            self.logger.debug(f"Resolving command with args: {vars(args)}")
        else:
            self.logger.debug(f"Resolving command with non-Namespace args")

        # Try to resolve using command path first
        cmd_path = self._extract_command_path(args)
        if cmd_path:
            return self._resolve_by_command_path(cmd_path, commands)

        # Fall back to command attribute if path not available
        return self._resolve_by_command_attribute(args, commands)

    def create_parser(self, commands):
        """Create argument parser with all commands and subcommands"""
        parser = argparse.ArgumentParser(description="easycmdline CLI")
        self.create_subparsers(parser, commands)
        self.logger.debug("Command parser created with all subcommands")
        return parser

    def _get_filtered_commands(self) -> Dict[str, Any]:
        """
        Get available commands from configuration, filtering out any 'command' entries
        that might interfere with parsing.

        Returns:
            Dictionary of commands from configuration
        """
        commands = {
            k: v for k, v in self.config.get("commands", {}).items() if k != "command"
        }
        self.logger.debug(f"Filtered commands: {list(commands.keys())}")
        return commands

    def _parse_arguments(
        self, parser: argparse.ArgumentParser, args: Optional[List[str]]
    ) -> argparse.Namespace:
        """
        Parse command line arguments using the provided parser.

        Args:
            parser: ArgumentParser instance to use for parsing
            args: Command line arguments. If None, sys.argv will be used.

        Returns:
            Parsed arguments as an argparse.Namespace
        """
        if args is None:
            # If called from command line
            if len(sys.argv) >= 3 and sys.argv[1].endswith(".yml"):
                # Config file provided as first argument
                args = parser.parse_args(sys.argv[2:])
            else:
                # No config file in arguments
                args = parser.parse_args(sys.argv[1:])
        else:
            # Called programmatically with specific args
            args = parser.parse_args(args)

        self.logger.debug(f"Parsed arguments: {vars(args)}")
        return args

    def _normalize_args(self, args: argparse.Namespace) -> argparse.Namespace:
        """
        Normalize arguments by ensuring command_path is always available.

        Args:
            args: Parsed arguments

        Returns:
            Normalized arguments
        """
        # Make sure command_path is always available
        if not hasattr(args, "_command_path"):
            args._command_path = []
        return args

    def _has_command(self, args: Any) -> bool:
        """
        Check if arguments specify a command.

        Args:
            args: Parsed arguments

        Returns:
            True if a command is specified, False otherwise
        """
        if not isinstance(args, argparse.Namespace):
            return False

        has_command_path = hasattr(args, "_command_path") and bool(args._command_path)
        has_command_attr = hasattr(args, "command") and bool(args.command)

        return has_command_path or has_command_attr

    def _get_command_text(self, args: Any) -> str:
        """
        Get a text representation of the command being executed.

        Args:
            args: Parsed arguments

        Returns:
            String representation of the command
        """
        if isinstance(args, argparse.Namespace):
            if hasattr(args, "_command_path"):
                return " ".join(args._command_path)
            elif hasattr(args, "command"):
                return args.command
        return "unknown"

    def _create_and_run_command(
        self, cmd_cfg: Dict[str, Any], args: Any, cmd_logger: logging.Logger
    ) -> Any:
        """
        Create a command instance and run it.

        Args:
            cmd_cfg: Command configuration
            args: Parsed arguments
            cmd_logger: Logger for the command

        Returns:
            Result of the command execution

        Raises:
            Exception: Any exception raised during command execution
        """
        # Import the command class
        cmd_cls = import_class(cmd_cfg["command_class"])
        try:
            cmd_name = getattr(cmd_cls, "__name__", str(cmd_cls))
            cmd_logger.debug(f"Imported command class: {cmd_name}")
        except (AttributeError, TypeError):
            cmd_logger.debug(f"Imported command class: {cmd_cls}")

        # Create handler if specified
        handler = None
        if "handler_class" in cmd_cfg:
            handler_cls = import_class(cmd_cfg["handler_class"])
            handler = handler_cls(args)  # Pass args to the handler
            try:
                handler_name = getattr(handler_cls, "__name__", str(handler_cls))
                cmd_logger.debug(f"Initialized handler: {handler_name}")
            except (AttributeError, TypeError):
                cmd_logger.debug(f"Initialized handler: {handler_cls}")

        # Create and execute the command
        command = cmd_cls(args, handler)
        cmd_text = self._get_command_text(args)
        cmd_logger.info(f"Executing command: {cmd_text}")

        result = command.run()
        cmd_logger.debug("Command execution completed successfully")
        return result

    def execute(self, args: Optional[List[str]] = None) -> Any:
        """
        Execute a command based on the given arguments

        Args:
            args: Command line arguments. If None, sys.argv will be used.

        Returns:
            The result of the command execution
        """
        # Get commands and create parser
        commands = self._get_filtered_commands()
        parser = self.create_parser(commands)

        # Parse and normalize arguments
        args = self._parse_arguments(parser, args)
        args = self._normalize_args(args)

        # Get a command-specific logger
        cmd_path = args._command_path if hasattr(args, "_command_path") else []
        cmd_logger = get_command_logger(cmd_path, self.config)

        # Check if no command was specified and display help if needed
        if not self._has_command(args):
            self.logger.info("No command specified. Showing help message.")
            parser.print_help()
            return

        try:
            # Resolve and execute the command
            cmd_cfg = self.resolve_command(args, commands)
            self.logger.debug(f"Resolved command configuration: {cmd_cfg}")

            return self._create_and_run_command(cmd_cfg, args, cmd_logger)

        except Exception as e:
            cmd_logger.error(f"Error executing command: {str(e)}")
            cmd_logger.debug("Exception details:", exc_info=True)
            raise


# Provide a function interface for backward compatibility and as entrypoint
def run(config_file=None):
    """
    Run the CLI with the given configuration file.

    This function exists for backward compatibility and as an entrypoint.
    """
    # Allow setting debug level with environment variable
    if os.environ.get("EASYCMDLINE_DEBUG"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug logging enabled")

    try:
        # Check if config file is provided as first argument when called directly
        if config_file is None and len(sys.argv) > 1 and sys.argv[1].endswith(".yml"):
            config_file = sys.argv[1]

            # The config file path should be relative to where this file is located.
            where_this_file_is = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(where_this_file_is, config_file)
            print(f"Config file: {config_file}")

        cli = EasyCmdLine(config_file)
        return cli.execute()
    except Exception as e:
        logging.error(f"Unhandled error: {str(e)}")
        if os.environ.get("EASYCMDLINE_DEBUG"):
            logging.debug("Exception details:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    print("Running as a script")
    run()
