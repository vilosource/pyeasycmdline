"""
Base classes for the command-line interface framework.

This module defines the abstract base classes that serve as the foundation
for implementing commands and handlers in the easycmdline framework.
It establishes the contract that concrete implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import argparse


class BaseCommand(ABC):
    """
    Abstract base class for all command implementations.

    Commands represent the actions that can be executed via the command line.
    Concrete implementations should override the abstract methods.
    """

    def __init__(
        self, args: argparse.Namespace, handler: Optional["BaseHandler"] = None
    ):
        """
        Initialize a command instance.

        Args:
            args: The parsed command-line arguments
            handler: Optional handler to process the command
        """
        self.args: argparse.Namespace = args
        self.handler: Optional["BaseHandler"] = handler

    @abstractmethod
    def run(self) -> Any:
        """
        Execute the command.

        Returns:
            The result of the command execution (type varies by implementation)
        """


class BaseHandler(ABC):
    """
    Abstract base class for all command handlers.

    Handlers contain the business logic that commands may use.
    Concrete implementations should override the abstract methods.
    """

    def __init__(self, args: Optional[argparse.Namespace] = None):
        """
        Initialize a handler instance.

        Args:
            args: The parsed command-line arguments (optional)
        """
        self.args: Optional[argparse.Namespace] = args

    @abstractmethod
    def run(self, args: Optional[argparse.Namespace] = None) -> Any:
        """
        Process the command with the given arguments.

        Args:
            args: The parsed command-line arguments (optional)

        Returns:
            The result of the handler execution (type varies by implementation)
        """
