import pytest

from datarails.contexts import DataBox


# This is a fixture that provides a fresh DataBox for each test that uses it.
@pytest.fixture
def dbx():
    return DataBox()


def test_add_df(dbx):
    df = [1, 2, 3]  # Mock DataFrame
    dbx.put_df("test_df", df)
    assert hasattr(dbx, "test_df"), "DataBox should have attribute 'test_df' after adding."
    assert dbx.test_df == df, "DataBox.test_df should be equal to the added DataFrame."


def test_get_df(dbx):
    df = [4, 5, 6]  # Mock DataFrame
    dbx.put_df("test_df", df)
    fetched_df = dbx.get_df("test_df")
    assert fetched_df == df, "get_df should return the added DataFrame."


def test_pop_df(dbx):
    df = [7, 8, 9]  # Mock DataFrame
    dbx.put_df("pop_test_df", df)
    popped_df = dbx.pop_df("pop_test_df")
    assert popped_df == df, "pop_df should return the added DataFrame."
    assert not hasattr(dbx, "pop_test_df"), "pop_test_df attribute should be deleted after popping."


def test_delete_df(dbx):
    df = [10, 11, 12]  # Mock DataFrame
    dbx.put_df("delete_test_df", df)
    dbx.delete_df("delete_test_df")
    assert not hasattr(dbx, "delete_test_df"), "delete_test_df attribute should be deleted."


def test_get_df_nonexistent(dbx):
    with pytest.raises(AttributeError):
        dbx.get_df("nonexistent_df")


def test_pop_df_nonexistent(dbx):
    with pytest.raises(AttributeError):
        dbx.pop_df("nonexistent_df")


def test_delete_df_nonexistent(dbx):
    with pytest.raises(AttributeError):
        dbx.delete_df("nonexistent_df")


def test_databox_constructor():
    test_kwargs = {"test_attr_1": "test_value_1", "test_attr_2": "test_value_2", "test_attr_3": "test_value_3"}
    context = DataBox(**test_kwargs)

    for key, value in test_kwargs.items():
        assert hasattr(context, key)
        assert getattr(context, key) == value
