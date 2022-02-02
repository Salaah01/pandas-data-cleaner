"""This module contains shared methods for cleaning data."""

import pandas as pd
from .base import CleaningStrategy


class RemoveDuplicates(CleaningStrategy):
    """Deletes duplicate data from the dataframe.

    Required options:
        `remove_duplicates_subset_fields` - (_t.List[str]) A list of fields
            to check for duplicates.
        `remove_duplicates_keep` - ('first'|'last'|False) Whether to keep
            the first or last occurrence of a duplicate  or drop all
            duplicates.
            More information available at:
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html#pandas.DataFrame.drop_duplicates
    """

    required_options = [
        "remove_duplicates_subset_fields",
        "remove_duplicates_keep"
    ]

    def clean(self) -> pd.DataFrame:
        """Executes the cleaning task."""
        self.dataframe.drop_duplicates(
            subset=self.remove_duplicates_subset_fields,
            keep=self.remove_duplicates_keep,
            inplace=True,
        )


class RenameHeaders(CleaningStrategy):
    """Renames the headers of the dataframe.

    Required options:
        `rename_headers_header_map` - (_t.Dict[str, str]) A dictionary
            mapping the old header names to the new header names.
    """

    required_options = ["rename_headers_header_map"]

    def clean(self) -> pd.DataFrame:
        """Executes the cleaning task."""
        self.dataframe.rename(
            columns=self.rename_headers_header_map,
            inplace=True,
        )


class FilterValidForeignKeys(CleaningStrategy):
    """This is a Django only method.
    Where a dataframe is being cleaned where a field in the dataframe must
    exist in another dataframe, this method will filter out any rows that
    contain invalid foreign keys.

    Required options:
        `filter_valid_fk_df` - (pd.DataFrame) The dataframe which this
            dataframe is being compared to.
        `filter_valid_pk_field` - (str) The field in the compared dataframe
            which contains the primary key.
        `filter_valid_fk_field` - (str) The field in the this dataframe which
            contains the foreign key.
    """

    required_options = [
        "filter_valid_fk_df",
        "filter_valid_pk_field",
        "filter_valid_fk_field",
    ]

    def clean(self):
        """Executes the cleaning task."""

        # Get the set of unique values in the foreign key column
        unique_fk_values = set(
            self.dataframe[self.filter_valid_fk_field].unique()
        )

        # Get the set of unique values in the primary key column
        unique_pk_values = set(self.filter_valid_fk_df[
            self.filter_valid_pk_field
        ].unique())

        # Get the set of values that are in the foreign key column but not in
        # the primary key column
        invalid_fk_values = unique_fk_values - unique_pk_values

        # Filter out the invalid foreign keys
        self.dataframe.drop(
            self.dataframe[
                self.dataframe[
                    self.filter_valid_fk_field
                ].isin(invalid_fk_values)
            ].index,
            inplace=True
        )


class RemoveColumns(CleaningStrategy):
    """Removes columns from a dataframe.

    Required options:
        `remove_columns` - (_t.List[str]) A list of columns to remove.
    """

    required_options = ["remove_columns"]

    def clean(self) -> pd.DataFrame:
        """Executes the cleaning task."""
        self.dataframe.drop(
            self.remove_columns, axis=1, inplace=True
        )
