"""Unittests for the `methods` module."""

import unittest
import pandas as pd
from data_cleaners import strategies
from data_cleaners.exceptions import MissingOptionsError


class TestRemoveDuplicates(unittest.TestCase):
    """Unittests for the `RemoveDuplicates` class."""

    def test_invalid_options(self):
        """Test that when no options are provided, the `can_use_cleaner` method
        indicates that there is an error.
        """

        strategy = strategies.RemoveDuplicates(pd.DataFrame({'a': [1, 2, 3]}))
        can_use, missing_options = strategy.can_use_cleaner()
        self.assertFalse(can_use)
        self.assertEqual(len(missing_options), 2)

    def test_clean_keep_last(self):
        """Test that the `clean` method removes duplicates where `keep` is set
        to `last`.
        """

        dataframe = pd.DataFrame(
            {
                "id": [1, 2, 1],
                "name": ["a", "a", "a"],
                "email": ['a@a.com', 'b@b.com', 'a@a.com'],
                "age": [1, 2, 1],
                "active": [True, True, False],  # Note: This is the only change
            }
        )

        strategy = strategies.RemoveDuplicates(
            dataframe,
            remove_duplicates_subset_fields=['id'],
            remove_duplicates_keep='last'
        )
        strategy.clean()
        results = strategy.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "id": [2, 1],
                "name": ["a", "a"],
                "email": ['b@b.com', 'a@a.com'],
                "age": [2, 1],
                "active": [True, False]
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )

    def test_clean_keep_first(self):
        """Test that the `clean` method removes duplicates where `keep` is set
        to `first`.
        """

        dataframe = pd.DataFrame(
            {
                "id": [1, 2, 1],
                "name": ["a", "a", "a"],
                "email": ['a@a.com', 'b@b.com', 'a@a.com'],
                "age": [1, 2, 1],
                "active": [True, True, False],  # Note: This is the only change
            }
        )

        strategy = strategies.RemoveDuplicates(
            dataframe,
            remove_duplicates_subset_fields=['id'],
            remove_duplicates_keep='first'
        )
        strategy.clean()
        results = strategy.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "id": [1, 2],
                "name": ["a", "a"],
                "email": ['a@a.com', 'b@b.com'],
                "age": [1, 2],
                "active": [True, True]
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )


class TestRenameHeaders(unittest.TestCase):
    """Unittests for the `RenameHeaders` class."""

    def test_invalid_options(self):
        """Test that when no options are provided, the `can_use_cleaner` method
        indicates that there is an error.
        """

        strategy = strategies.RenameHeaders(pd.DataFrame({'a': [1, 2, 3]}))
        can_use, missing_options = strategy.can_use_cleaner()
        self.assertFalse(can_use)
        self.assertEqual(len(missing_options), 1)

    def test_clean_rename_headers(self):
        """Test that the `clean` method renames headers."""

        dataframe = pd.DataFrame(
            {
                "id": [1, 2, ],
                "name": ["a", "b"]
            }
        )
        strategy = strategies.RenameHeaders(
            dataframe,
            rename_headers_header_map={'id': 'customer_id'}
        )
        strategy.clean()
        results = strategy.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "customer_id": [1, 2],
                "name": ["a", "b"]
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )


class TestFilterValidForeignKeys(unittest.TestCase):
    """Unittests for the `FilterValidationForeignKeys` class."""

    def test_invalid_options(self):
        """Test that when no options are provided, the `can_use_cleaner` method
        indicates that there is an error.
        """

        strategy = strategies.FilterValidForeignKeys(
            pd.DataFrame({'a': [1, 2, 3]})
        )
        can_use, missing_options = strategy.can_use_cleaner()
        self.assertFalse(can_use)
        self.assertEqual(len(missing_options), 3)

    def test_clean_filter_valid_foreign_keys(self):
        """Test that the `clean` method removes invalid foreign keys."""

        dataframe_1 = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "letter": ["a", "b", "c"]
            }
        )

        dataframe_2 = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "fk": [1, 2, 5],
            }
        )

        strategy = strategies.FilterValidForeignKeys(
            dataframe_2,
            filter_valid_fk_df=dataframe_1,
            filter_valid_pk_field='id',
            filter_valid_fk_field='fk'
        )

        strategy.clean()

        results = strategy.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "id": [1, 2],
                "fk": [1, 2],
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )


class TestRemoveColumns(unittest.TestCase):
    """Unittests for the `RemoveColumns` class."""

    def test_invalid_options(self):
        """Test that when no options are provided, the `can_use_cleaner` method
        indicates that there is an error.
        """

        strategy = strategies.FilterValidForeignKeys(
            pd.DataFrame({'a': [1, 2, 3]})
        )
        can_use, missing_options = strategy.can_use_cleaner()
        self.assertFalse(can_use)
        self.assertEqual(len(missing_options), 3)

    def test_clean_remove_columns(self):
        """Test that the `clean` method removes the columns specified."""

        dataframe = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "col1": [1, 2, 3],
                "col2": [1, 2, 3],
                "col3": [1, 2, 3],
            }
        )

        strategy = strategies.RemoveColumns(
            dataframe,
            remove_columns=['col1', 'col2']
        )
        strategy.clean()
        results = strategy.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "col3": [1, 2, 3],
            }
        )

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )
