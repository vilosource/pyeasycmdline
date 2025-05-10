from abc import ABC, abstractmethod
from typing import Any, Optional
import argparse


class BaseCommand(ABC):
    def __init__(
        self, args: argparse.Namespace, handler: Optional["BaseHandler"] = None
    ):
        self.args: argparse.Namespace = args
        self.handler: Optional["BaseHandler"] = handler

    @abstractmethod
    def run(self) -> Any:
        pass


class BaseHandler(ABC):
    def __init__(self, args: Optional[argparse.Namespace] = None):
        self.args: Optional[argparse.Namespace] = args

    @abstractmethod
    def run(self, args: Optional[argparse.Namespace] = None) -> Any:
        pass
