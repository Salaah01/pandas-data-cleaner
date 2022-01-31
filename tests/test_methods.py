"""Unittests for the `methods` module."""

import unittest
import pandas as pd
from data_cleaners import methods
from tests.utils import models


class TestRemoveDuplicates(unittest.TestCase):
    """Unittests for the `RemoveDuplicates` class."""

    def test_clean_invalid_model(self):
        """Test that when a module is provided for which a field map has not
        been defined, an `ImplementationError` is raised.
        """
        remove_duplicates = methods.RemoveDuplicates(
            pd.DataFrame({"a": [1, 2, 3]}),
            models.MisconfiguredModel
        )
        with self.assertRaises(NotImplementedError):
            remove_duplicates.clean()

    def test_with_model(self):
        """Test that the data for a valid model is cleaned correctly."""
        dataframe = pd.DataFrame(
            {
                "id": [1, 2, 1],
                "name": ["a", "a", "a"],
                "email": ['a@a.com', 'b@b.com', 'a@a.com'],
                "age": [1, 2, 1],
                "active": [True, True, False],  # Note: This is the only change
            }
        )
        remove_duplicates = methods.RemoveDuplicates(
            dataframe,
            models.User
        )
        remove_duplicates.clean()
        results = remove_duplicates.dataframe.reset_index(drop=True)

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


class TestFilterValidForeignKeys(unittest.TestCase):
    """Unittests for the `FilterValidForeignKeys` class."""

    def test_ad_group(self):
        """Test that the `clean` removes the correct data when being used for
        the `campaign_models.AdGroup` class.
        """

        # Load the Campaign model with data as the AdGroup model contains a
        # foreign key to the Campaign model.
        dataframe = pd.DataFrame({
            "id": [1, 2, 3],
            "user_id": [1, 2, 3],
            "product_id": [1, 2, 3],
            "price": [1, 2, 3],
            "quantity": [1, 2, 3],
        })

        filter_valid_fks = methods.DjFilterValidForeignKeys(
            dataframe,
            models.Purchase
        )
        filter_valid_fks.clean()
        results = filter_valid_fks.dataframe.reset_index(drop=True)

        expected_results = pd.DataFrame({
            "id": [1, 2],
            "user_id": [1, 2],
            "product_id": [1, 2],
            "price": [1, 2],
            "quantity": [1, 2],
        })

        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )


# class RemoveColumns(unittest.TestCase):
#     """Unittests for the `RemoveColumns` class."""

#     def test_remove_columns(self):
#         """Test that the `clean` method removes the correct columns."""
#         dataframe = pd.DataFrame(
#             {
#                 "a": [1, 2, 3],
#                 "b": [1, 2, 3],
#                 "c": [1, 2, 3],
#             }
#         )

#         model = SimpleNamespace(
#             DataCleaner=SimpleNamespace(remove_columns=["a", "b"])
#         )

#         remove_columns = methods.RemoveColumns(dataframe, model)
#         remove_columns.clean()
#         results = remove_columns.dataframe.reset_index(drop=True)

#         expected_results = pd.DataFrame({"c": [1, 2, 3]})

#         self.assertTrue(
#             results.equals(expected_results),
#             f"\nActual:\n{results}\nExpected:\n{expected_results}",
#         )


# if __name__ == "__main__":
#     unittest.main()
