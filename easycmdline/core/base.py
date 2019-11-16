from abc import ABC, abstractmethod


class BaseCommand(ABC):
    def __init__(self, args, handler=None):
        self.args = args
        self.handler = handler

    @abstractmethod
    def run(self):
        pass


class BaseHandler(ABC):
    def __init__(self, args=None):
        self.args = args

    @abstractmethod
    def run(self, args=None):
        pass
