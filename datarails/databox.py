from datarails.type_vars import DataFrame


class DataBox:
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

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
