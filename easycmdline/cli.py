import argparse
import logging
import os
import sys
from core.config import load_config
from core.registry import import_class
from core.logging_setup import setup_logging, get_command_logger

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
        self.config_file = config_file or os.environ.get(
            "EASYCMDLINE_CONFIG", "easycmdline-config.yml"
        )
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

    def resolve_command(self, args, commands):
        """Resolve command configuration from args using the command path"""
        self.logger.debug(f"Resolving command with args: {vars(args)}")

        # Extract command path from args
        if hasattr(args, "_command_path"):
            cmd_path = args._command_path
            self.logger.debug(f"Found command path: {cmd_path}")

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
                    return cmd_cfg

                # Otherwise, move to the next level of subcommands
                if "subcommands" not in cmd_cfg:
                    err_msg = f"Command '{cmd}' has no subcommands but path continues"
                    cmd_logger.error(err_msg)
                    raise ValueError(err_msg)

                current_commands = cmd_cfg["subcommands"]

        # Fallback to old method if no path available
        if hasattr(args, "command") and args.command in commands:
            cmd_cfg = commands[args.command]
            if "subcommands" in cmd_cfg:
                return self.resolve_command(args, cmd_cfg["subcommands"])
            return cmd_cfg

        err_msg = f"Could not resolve command configuration"
        self.logger.error(err_msg)
        raise ValueError(err_msg)

    def create_parser(self, commands):
        """Create argument parser with all commands and subcommands"""
        parser = argparse.ArgumentParser(description="easycmdline CLI")
        self.create_subparsers(parser, commands)
        self.logger.debug("Command parser created with all subcommands")
        return parser

    def execute(self, args=None):
        """
        Execute a command based on the given arguments

        Args:
            args: Command line arguments. If None, sys.argv will be used.

        Returns:
            The result of the command execution
        """
        # Filter out any 'command' entries that might interfere with parsing
        commands = {
            k: v for k, v in self.config.get("commands", {}).items() if k != "command"
        }
        self.logger.debug(f"Filtered commands: {list(commands.keys())}")

        parser = self.create_parser(commands)

        # Parse the arguments
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

        cmd_cfg = self.resolve_command(args, commands)
        self.logger.debug(f"Resolved command configuration: {cmd_cfg}")

        # Get a command-specific logger based on command path
        cmd_logger = get_command_logger(
            args._command_path if hasattr(args, "_command_path") else [], self.config
        )

        try:
            cmd_cls = import_class(cmd_cfg["command_class"])
            cmd_logger.debug(f"Imported command class: {cmd_cls.__name__}")

            handler = None
            if "handler_class" in cmd_cfg:
                handler_cls = import_class(cmd_cfg["handler_class"])
                handler = handler_cls(args)  # Pass args to the handler
                cmd_logger.debug(f"Initialized handler: {handler_cls.__name__}")

            command = cmd_cls(args, handler)
            cmd_logger.info(
                f"Executing command: {' '.join(args._command_path) if hasattr(args, '_command_path') else args.command}"
            )

            result = command.run()
            cmd_logger.debug("Command execution completed successfully")
            return result

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

        cli = EasyCmdLine(config_file)
        return cli.execute()
    except Exception as e:
        logging.error(f"Unhandled error: {str(e)}")
        if os.environ.get("EASYCMDLINE_DEBUG"):
            logging.debug("Exception details:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run()
