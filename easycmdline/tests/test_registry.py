from easycmdline.core.registry import import_class


def test_import_class():
    cls = import_class("collections.Counter")
    assert cls.__name__ == "Counter"
