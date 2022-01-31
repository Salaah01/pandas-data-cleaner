"""Dummy models for testing."""

from dataclasses import dataclass
from types import SimpleNamespace


@dataclass
class User:
    """Dummy user model."""
    id: int
    name: str
    email: str
    age: int
    active: bool = True

    @property
    def objects(self):
        """Imitates the Django model manager. We don't need to mock the entire
        model manager, so we just mock what we need.
        """
        return SimpleNamespace(
            values_list=lambda *args, **kwargs: [1, 2]
        )

    class DataCleaner:
        remove_duplicates_subset_fields = ["id", "name"]


@dataclass
class Purchase:
    """Dummy purchase model."""
    id: int
    user_id: int
    product_id: int
    price: float
    quantity: int

    class DataCleaner:
        fk_map = {"model": User, "user_id": "id"}


@dataclass
class MisconfiguredModel:
    """Dummy model with no DataCleaner class."""
    id: int
    name: str
    email: str
    age: int
    active: bool = True
