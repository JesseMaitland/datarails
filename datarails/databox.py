from typing import List

from datarails.type_vars import DataFrame


class DataBox:
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        return f"DataBox({self.list_contents()})"

    def get_df(self, name: str) -> DataFrame:
        return getattr(self, name)

    def add_df(self, name: str, df: DataFrame) -> None:
        setattr(self, name, df)

    def pop_df(self, name: str) -> DataFrame:
        df = self.get_df(name)
        delattr(self, name)
        return df

    def delete_df(self, name: str) -> None:
        delattr(self, name)

    def list_contents(self) -> List[str]:
        return [k for k in vars(self).keys()]
