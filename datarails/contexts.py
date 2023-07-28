from typing import Any, List, Union

from datarails.type_vars import DataFrame


class _BaseContext:
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def list_contents(self) -> List[str]:
        return [k for k in vars(self).keys()]

    def _get(self, name: str) -> Union[Any, None]:
        return getattr(self, name)

    def _put(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    def _pop(self, name: str) -> DataFrame:
        item = self._get(name)
        delattr(self, name)
        return item

    def _delete(self, name: str) -> None:
        delattr(self, name)


class DataRailsContext(_BaseContext):
    """DataRailsContext provides an interface to interact with its data."""

    def __str__(self) -> str:
        """Returns a string representation of the context."""
        return f"DataRailsContext({self.list_contents()})"

    def get(self, name: str) -> Union[Any, None]:
        """
        Gets a value from the context based on its name.

        Args:
            name (str): The name of the value to get.

        Returns:
            Union[Any, None]: The value associated with the name, or None if it doesn't exist.
        """
        return self._get(name)

    def put(self, name: str, value: Any) -> None:
        """
        Puts a value into the context with a specified name.

        Args:
            name (str): The name to associate with the value.
            value (Any): The value to put into the context.
        """
        self._put(name, value)

    def pop(self, name: str) -> DataFrame:
        """
        Pops a value from the context based on its name.

        Args:
            name (str): The name of the value to pop.

        Returns:
            DataFrame: The DataFrame associated with the name.
        """
        return self._pop(name)

    def delete(self, name: str) -> None:
        """
        Deletes a value from the context based on its name.

        Args:
            name (str): The name of the value to delete.
        """
        self._delete(name)


class DataBox(_BaseContext):
    """DataBox provides an interface to interact with its DataFrame data."""

    def __str__(self) -> str:
        """Returns a string representation of the DataBox."""
        return f"DataBox({self.list_contents()})"

    def get_df(self, name: str) -> DataFrame:
        """
        Gets a DataFrame from the DataBox based on its name.

        Args:
            name (str): The name of the DataFrame to get.

        Returns:
            DataFrame: The DataFrame associated with the name.
        """
        return self._get(name)

    def put_df(self, name: str, df: DataFrame) -> None:
        """
        Puts a DataFrame into the DataBox with a specified name.

        Args:
            name (str): The name to associate with the DataFrame.
            df (DataFrame): The DataFrame to put into the DataBox.
        """
        self._put(name, df)

    def pop_df(self, name: str) -> DataFrame:
        """
        Pops a DataFrame from the DataBox based on its name.

        Args:
            name (str): The name of the DataFrame to pop.

        Returns:
            DataFrame: The DataFrame associated with the name.
        """
        return self._pop(name)

    def delete_df(self, name: str) -> None:
        """
        Deletes a DataFrame from the DataBox based on its name.

        Args:
            name (str): The name of the DataFrame to delete.
        """
        self._delete(name)
