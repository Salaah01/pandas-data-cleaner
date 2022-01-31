"""This module constains an abstract base class for data cleaning strategies
that is used to define new cleaning strategies. It also contains the main
function that is used to run the cleaning strategy.
"""

import typing as _t
import pandas as pd
from abc import ABC, abstractmethod


class CleaningStrategy(ABC):
    """This class defines the strategy for cleaning data."""

    requires_django: bool = False

    def __init__(self, dataframe: pd.DataFrame, model):
        """Initialize the cleaning strategy.

        Args:
            dataframe: A pandas dataframe.
            model: A django model.
        """
        self.dataframe = dataframe
        self.model = model
        self.dataset_has_been_reversed = False

    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Returns True if the cleaning strategy can be used.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        # Check Django requirements
        if self.requires_django:
            try:
                import django  # noqa: F401
            except ImportError:
                return (
                    False,
                    "This cleaning strategy requires django to be installed.",
                )

        # Check if the model has the required attributes
        can_use = hasattr(self.model, "DataCleaner")
        if not can_use:
            return False, "The model does not have a DataCleaner class."
        return True, None

    def validate_model(self) -> None:
        """Validates if the model can run a cleaning strategy. If not, raise
        an error.
        """
        can_use, error_message = self.can_use_cleaner()
        if not can_use:
            raise NotImplementedError(error_message)

    @abstractmethod
    def clean(self) -> pd.DataFrame:
        """This method cleans the data and returns a cleaned dataframe

        Args:
            dataframe - The dataframe to be cleaned.
            model - The model which the data is being cleaned for.

        Returns:
            The cleaned dataframe.
        """
        pass


def clean_data(
    dataframe: pd.DataFrame,
    model,
    strategies: _t.List[CleaningStrategy],
) -> pd.DataFrame:
    """This function cleans the data using the given strategies.

    Args:
        dataframe: A pandas dataframe.
        model: A django model.
        strategies: A list of cleaning strategies.

    Returns:
        The cleaned dataframe.
    """

    df = dataframe.copy()
    for strategy in strategies:
        strat = strategy(df, model)
        strat.clean()
        df = strat.dataframe
    return df
