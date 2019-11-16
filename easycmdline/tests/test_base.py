import pytest
from easycmdline.core.base import BaseCommand, BaseHandler


class ConcreteCommand(BaseCommand):
    """Concrete implementation of BaseCommand for testing"""

    def run(self):
        return "command executed"


class ConcreteHandler(BaseHandler):
    """Concrete implementation of BaseHandler for testing"""

    def run(self, args=None):
        return "handler executed"


class TestBaseCommand:
    def test_init(self):
        """Test BaseCommand initialization"""
        args = type("TestArgs", (), {"test_arg": "test_value"})()
        handler = object()

        cmd = ConcreteCommand(args, handler)

        assert cmd.args == args
        assert cmd.handler == handler

    def test_abstract_method(self):
        """Test that BaseCommand.run() is abstract"""
        with pytest.raises(TypeError) as excinfo:
            BaseCommand(None)
        assert "abstract class" in str(excinfo.value)
        assert "run" in str(excinfo.value)


class TestBaseHandler:
    def test_init(self):
        """Test BaseHandler initialization"""
        args = type("TestArgs", (), {"test_arg": "test_value"})()

        handler = ConcreteHandler(args)

        assert handler.args == args

    def test_init_no_args(self):
        """Test BaseHandler initialization without args"""
        handler = ConcreteHandler()

        assert handler.args is None

    def test_abstract_method(self):
        """Test that BaseHandler.run() is abstract"""
        with pytest.raises(TypeError) as excinfo:
            BaseHandler()  # This will fail if we try to use the method
            BaseHandler().run()  # This line won't execute but shows intent
        assert "abstract class" in str(excinfo.value)
        assert "run" in str(excinfo.value)
