#!/usr/bin/env python3
"""Runs the test suite."""

import unittest
import sys
import os
# Add `data_cleaner` to the path which is a sibling of `tests`
sys.path.insert(
    0,
    (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
)


def suite():
    """Runs the test suite."""
    return unittest.TestLoader().discover('.')


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
