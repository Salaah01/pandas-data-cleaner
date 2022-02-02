"""This module constains an abstract base class for data cleaning strategies
that is used to define new cleaning strategies. It also contains the main
function that is used to run the cleaning strategy.
"""

import typing as _t
import pandas as pd
from abc import ABC, abstractmethod
from .exceptions import MissingOptionsError


class CleaningStrategy(ABC):
    """This class defines the strategy for cleaning data."""

    required_options: _t.List[str] = []

    def __init__(self, dataframe: pd.DataFrame, **options):
        """Initialize the cleaning strategy.

        Args:
            dataframe: A pandas dataframe.
            **options: Keyword arguments containing options for the cleaning
                strategy.
        """
        self.dataframe = dataframe
        self.dataset_has_been_reversed = False

        # Add all options to the `self` object
        for key, value in options.items():
            setattr(self, key, value)

    @classmethod
    def info(cls) -> str:
        """Returns a formatted version of the documentation."""
        return (
            cls.__doc__
            .replace('    ', '')
            .replace('\t', '')
            .replace('\n', ' ')
        )


    def can_use_cleaner(self) -> _t.Tuple[bool, _t.List[str]]:
        """Returns True if the cleaning strategy can be used.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a list of missing options.
        """
        missing_options = []
        for option in self.required_options:
            if not hasattr(self, option):
                missing_options.append(option)

        return (len(missing_options) == 0, missing_options)

    def validate_options(self) -> None:
        """Validates if the right options have been provided.

        Raises:
            MissingOptionsError: Raised when options are missing.
        """
        can_use, missing_options = self.can_use_cleaner()
        if not can_use:
            raise MissingOptionsError(missing_options)

    @abstractmethod
    def clean(self) -> pd.DataFrame:
        """This method cleans the data and returns a cleaned dataframe

        Args:
            dataframe - The dataframe to be cleaned.

        Returns:
            The cleaned dataframe.
        """
        pass


def clean_data(
    dataframe: pd.DataFrame,
    strategies: _t.List[CleaningStrategy],
    **options
) -> pd.DataFrame:
    """This function cleans the data using the given strategies and options for
    each strategy.

    Args:
        dataframe: A pandas dataframe.
        strategies: A list of cleaning strategies.
        **options: Keyword arguments containing options for the cleaning

    Returns:
        The cleaned dataframe.

    Raises:
        MissingOptionsError: Raised when options are missing.
    """

    df = dataframe.copy()
    for strategy in strategies:
        strat = strategy(df, **options)
        strat.validate_options()
        strat.clean()
        df = strat.dataframe
    return df
