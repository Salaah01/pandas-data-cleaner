"""Custom exceptions."""

import typing as _t


class MissingOptionsError(Exception):
    """Raised when options are missing."""

    def __init__(self, missing_options: _t.List[str]):
        """Initialize the exception."""
        self.missing_options = missing_options
        super().__init__(missing_options)

    def __str__(self):
        """Return a string representation of the exception."""
        missing_opts_str = "\n".join(self.missing_options)
        return f"Missing kwargs:\n{missing_opts_str}"
