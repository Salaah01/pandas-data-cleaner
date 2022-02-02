"""Unitests for the `base` module."""

from unittest import TestCase
from types import SimpleNamespace
import pandas as pd
from pandas_data_cleaner import base, exceptions
from tests.utils import strategies


class TestCleaningStrategy(TestCase):
    """Unittests for the `CleaningStrategy` class."""

    def test_info(self):
        """Test that the `info` method returns a formated version of the
        docstring.
        """
        self.assertIsInstance(base.CleaningStrategy.info(), str)

    def test_can_use_cleaner_pass(self):
        """Test that the `can_use_cleaner` method indicates `True` when a
        model has the attributes the method expects.
        """

        instance = SimpleNamespace(
            dataframe=None,
            required_options=['option_1'],
            option_1=1,
        )
        self.assertEqual(
            base.CleaningStrategy.can_use_cleaner(instance),
            (True, [])
        )

    def test_can_use_cleaner_fail(self):
        """Test that the `can_use_cleaner` method indicates `False` when a
        model does not have the attributes the method expects.
        """

        instance = SimpleNamespace(
            dataframe=None,
            required_options=['option_1'],
        )

        can_use, missing_opts = base.CleaningStrategy.can_use_cleaner(instance)
        self.assertFalse(can_use, missing_opts)
        self.assertEqual(len(missing_opts), 1)

    def test_validate_options_pass(self):
        """Test that the `validate_options` method does not raise an error when
        the model has the attributes the method expects.
        """

        instance = SimpleNamespace(
            can_use_cleaner=lambda: (True, []),
        )
        base.CleaningStrategy.validate_options(instance)

    def test_validate_options_fail(self):
        """Test that the `validate_options` method raises an error when the
        model does not have the attributes the method expects.
        """

        instance = SimpleNamespace(
            dataframe=None,
            model=SimpleNamespace(),
            can_use_cleaner=lambda: (False, ["Failed"]),
        )
        with self.assertRaises(exceptions.MissingOptionsError):
            base.CleaningStrategy.validate_options(instance)


class TestCleanData(TestCase):
    """Unittests for the `clean_data` function."""

    def test_can_apply_strategies(self):
        """Test that the method is able to apply various cleaning strategies on
        a dataframe.
        """

        # Create a test dataframe.
        dataframe = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [4, 5, 6],
            "col3": [7, 8, 9],
        })

        # make a copy of the dataframe to test that the strategies are applied
        # in the correct order.
        results = base.clean_data(
            dataframe,
            [strategies.ReverseStrategy, strategies.FirstXRowsStrategy],
            x_top_rows=2
        ).reset_index(drop=True)

        expected_results = pd.DataFrame({
            "col1": [3, 2],
            "col2": [6, 5],
            "col3": [9, 8],
        })
        self.assertTrue(
            results.equals(expected_results),
            f"\nActual:\n{results}\nExpected:\n{expected_results}",
        )

    def test_no_mutations(self):
        """Test that the original dataframe is not mutated."""
        dataframe = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [4, 5, 6],
            "col3": [7, 8, 9],
        })

        dataframe_copy = dataframe.copy()
        base.clean_data(dataframe, [strategies.ReverseStrategy])
        self.assertTrue(dataframe.equals(dataframe_copy))
