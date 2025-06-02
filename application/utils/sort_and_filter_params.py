from flask import request


class SortAndFilterParams:
    """Encapsulate sorting/filtering options passed in via query params order_by, desc, and search."""

    # Might want to make this a form, but I'm going to keep it simple for now

    # constructor: just use request args
    def __init__(self) -> None:
        self.order_by = request.args.get("order_by") or "date"
        self.desc = (request.args.get("desc").lower() == "true") if request.args.get("desc") else True
        self.search = request.args.get("search").lower().strip() if request.args.get("search") else None

    order_by: str  # The column to sort by
    desc: bool  # Whether sorting should be in descending order
    search: str | None  # Text to search
