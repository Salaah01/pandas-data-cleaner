"""Contains dummy strategies for unittesting."""


from pandas_data_cleaner import base
import pandas as pd


class ReverseStrategy(base.CleaningStrategy):
    """A strategy that reverses the dataframe."""

    def clean(self) -> pd.DataFrame:
        """Reverses the dataframe in place."""
        self.dataframe = self.dataframe.iloc[::-1]


class FirstXRowsStrategy(base.CleaningStrategy):
    """A strategy that shrinks the dataframe to x number of rows."""

    required_options = ['x_top_rows']

    def clean(self) -> pd.DataFrame:
        """Shrinks the dataframe to x number of rows."""
        self.dataframe = self.dataframe.iloc[:2]
