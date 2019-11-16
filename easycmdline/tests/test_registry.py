import pytest
from collections import Counter
from easycmdline.core.registry import import_class


def test_import_class_builtin():
    """Test importing a built-in class"""
    cls = import_class("collections.Counter")
    assert cls is Counter
    assert cls.__name__ == "Counter"


def test_import_class_local(monkeypatch):
    """Test importing a local class with monkeypatch to simulate import"""
    import sys

    # Create a mock module for testing
    class MockClass:
        pass

    # Create a mock module
    class MockModule:
        TestClass = MockClass

    # Add the mock module to sys.modules
    monkeypatch.setitem(sys.modules, "mock_module", MockModule)

    # Import the test class
    cls = import_class("mock_module.TestClass")

    assert cls is MockClass
    assert cls.__name__ == "MockClass"


def test_import_class_not_found():
    """Test importing a non-existent class"""
    with pytest.raises(ModuleNotFoundError):
        import_class("nonexistent_module.NonExistentClass")


def test_import_class_attribute_error():
    """Test importing a non-existent class from a valid module"""
    with pytest.raises(AttributeError):
        import_class("collections.NonExistentClass")
