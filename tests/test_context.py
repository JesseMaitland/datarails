import pytest

from datarails.contexts import DataRailsContext


def test_str_representation():
    context = DataRailsContext()
    assert str(context) == f"DataRailsContext({context.list_contents()})"


def test_get_value():
    context = DataRailsContext()
    context.put("test_name", "test_value")  # assuming _put works as expected
    assert context.get("test_name") == "test_value"


def test_put_value():
    context = DataRailsContext()
    context.put("test_name", "test_value")
    assert context._get("test_name") == "test_value"  # assuming _get works as expected


def test_pop_value():
    test_name = "this is a random value"
    context = DataRailsContext()
    context.put("test_name", test_name)  # assuming _put works as expected
    popped_value = context.pop("test_name")

    assert popped_value == test_name


def test_delete_value():
    context = DataRailsContext()
    context.put("test_name", "test_value")
    context.delete("test_name")

    with pytest.raises(AttributeError):
        context._get("test_name")


def test_context_constructor():
    test_kwargs = {"test_attr_1": "test_value_1", "test_attr_2": "test_value_2", "test_attr_3": "test_value_3"}
    context = DataRailsContext(**test_kwargs)

    for key, value in test_kwargs.items():
        assert hasattr(context, key)
        assert getattr(context, key) == value
