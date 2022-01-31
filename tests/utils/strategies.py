"""Contains dummy strategies for unittesting."""


from data_cleaners import base
import pandas as pd


class ReverseStrategy(base.CleaningStrategy):
    """A strategy that reverses the dataframe."""

    def clean(self) -> pd.DataFrame:
        """Reverses the dataframe in place."""
        self.dataframe = self.dataframe.iloc[::-1]


class FirstTwoRowsStrategy(base.CleaningStrategy):
    """A strategy that shrinks the dataframe to only the first two rows."""

    def clean(self) -> pd.DataFrame:
        """Shrinks the dataframe to only the first two rows."""
        self.dataframe = self.dataframe.iloc[:2]
