"""This module contains shared methods for cleaning data."""

import typing as _t
import pandas as pd
from .base import CleaningStrategy


class RemoveDuplicates(CleaningStrategy):
    """Deletes duplicate data from the dataframe keeping on the last row."""

    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Checks if the model can use the cleaner.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        can_use = super().can_use_cleaner()
        if not can_use[0]:
            return can_use
        can_use = hasattr(
            self.model.DataCleaner, "remove_duplicates_subset_fields"
        )
        if not can_use:
            return (
                False,
                "Model missing `DataCleaner.remove_duplicates_subset_fields`  "
                "attribute. This attribute is required for to know which "
                "fields to remove duplicates from. "
                "`remove_duplicates_subset_fields =['field_1', 'field_2']`",
            )
        return True, None

    def clean(self) -> pd.DataFrame:
        """Executes the cleaning task."""
        self.validate_model()
        self.dataframe.drop_duplicates(
            subset=self.model.DataCleaner.remove_duplicates_subset_fields,
            keep="last",
            inplace=True,
        )


class RenameHeaders(CleaningStrategy):
    """Renames the headers of the dataframe."""

    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Checks if the model can use the cleaner.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        can_use = super().can_use_cleaner()
        if not can_use[0]:
            return can_use
        can_use = hasattr(self.model.DataCleaner, "rename_headers_header_map")
        if not can_use:
            return (
                False,
                "Model missing `DataCleaner.rename_headers_header_map` "
                "attribute. This attribute is required to know which fields "
                "to rename. `rename_headers_header_map` = "
                "{'old_header': 'new_header'}",
            )
        return True, None

    def clean(self) -> pd.DataFrame:
        """Executes the cleaning task."""
        self.validate_model()
        self.dataframe.rename(
            columns=self.model.DataCleaner.rename_headers_header_map,
            inplace=True,
        )


class DjFilterValidForeignKeys(CleaningStrategy):
    """This is a Django only method.
    Where a data that is being imported contains foreign key(s), check that
    the respective primary key exists in the database table which the foreign
    key is associated with.
    """

    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Checks if the model can use the cleaner.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        can_use = super().can_use_cleaner()
        if not can_use[0]:
            return can_use
        can_use = hasattr(self.model.DataCleaner, "fk_map")
        if not can_use:
            return (
                False,
                "Model missing `DataCleaner.fk_map` attribute. This "
                "attribute is a dictionary mapping fields to models and "
                "field: {'field': {'model': Model', 'field': 'field'}}",
            )
        return True, None

    def clean(self):
        """Executes the cleaning task."""
        self.validate_model()

        columns = list(self.model.DataCleaner.fk_map.keys())

        for column in columns:
            model = self.model.DataCleaner.fk_map[column]["model"]
            field = self.model.DataCleaner.fk_map[column]["field"]

            # Get a set of all the primary keys from the model
            pk_set = set(model.objects.values_list(field, flat=True))

            # Get a set of all the foreign keys from the dataframe
            fk_set = set(self.dataframe[column].unique())

            # Check if the foreign keys are valid
            invalid_fk_set = fk_set - pk_set
            # Remove rows that contain invalid foreign keys
            self.dataframe.drop(
                self.dataframe[
                    self.dataframe[column].isin(invalid_fk_set)
                ].index,
                inplace=True,
            )


class RemoveColumns(CleaningStrategy):
    """Removes columns from a dataframe."""

    def can_use_cleaner(self) -> _t.Tuple[bool, _t.Union[str, None]]:
        """Checks if the model can use the cleaner.

        Returns:
            A tuple containing a boolean indicating if the cleaning strategy
            can be used and a string containing an error message if the
            cleaning strategy cannot be used. If the cleaning strategy can be
            used, the error message will be None.
        """
        can_use = super().can_use_cleaner()
        if not can_use[0]:
            return can_use
        can_use = hasattr(self.model.DataCleaner, "remove_columns")
        if not can_use:
            return (
                False,
                "Model missing `DataCleaner.remove_columns` attribute. This "
                "attribute is a list of columns to remove from the dataframe.",
            )
        return True, None

    def clean(self) -> pd.DataFrame:
        """Executes the cleaning task."""
        self.validate_model()
        self.dataframe.drop(
            self.model.DataCleaner.remove_columns, axis=1, inplace=True
        )
