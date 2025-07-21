from typing import Generic, TypeVar

from flask_sqlalchemy.pagination import Pagination

T = TypeVar("T")


class TypedPagination(Pagination, Generic[T]):
    """Pagination of a certain type, so items will be typed."""

    items: list[T]
