from typing import Annotated

import fastapi


def calculate_skip(
    page: Annotated[int, fastapi.Query(ge=1)] = 1,
    limit: Annotated[int, fastapi.Query(ge=1)] = 10
) -> int:
    """
    Calculate the number of hotels to skip based on pagination.

    - `page` (int, query): The current page number (default: 1).
    - `limit` (int, query): The number of hotels per page (default: 10).

    Returns:
    - int: The number of hotels to skip based on pagination.
       """
    return limit * (page - 1)
