import math
from typing import Annotated

import fastapi
from fastapi import responses
from motor import core as motor_core

import database_client
import dependencies

router = fastapi.APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("/retrieve")
async def retrieve_hotels(
    *,
    page: Annotated[int, fastapi.Query(ge=1)] = 1,
    limit: Annotated[int, fastapi.Query(ge=1)] = 10,
    skip: Annotated[int, fastapi.Depends(dependencies.calculate_skip)],
    collection: Annotated[
        motor_core.AgnosticCollection,
        fastapi.Depends(database_client.client.get_hotels_collection)
    ]
) -> responses.JSONResponse:
    """
    Retrieve all hotels records.

    Retrieves a list of hotels with optional pagination.

    - `page` (int, query): The current page number (default: 1).
    - `limit` (int, query): The number of hotels per page (default: 10).
    - `skip` (int, calculated): The number of hotels to skip based on pagination.
    - `collection` (motor_core.AgnosticCollection, dependency): MongoDB collection for hotels.

    Returns:
    - JSONResponse: A JSON response containing hotel data, pagination info, and the limit.
    """

    cursor = collection.find(
        {},
        projection={'_id': 0, 'id': 1, 'city': 1, 'country': 1, 'name': 1}
    ).skip(skip).limit(limit)
    found_hotels_number = await collection.count_documents({})
    pages = math.ceil(found_hotels_number / limit)

    hotels = await cursor.to_list(length=limit)
    return responses.JSONResponse(
        content={'current_page': page, 'pages': pages, 'hotels': hotels, 'limit': limit}
    )


@router.post("/retrieve_filtered")
async def retrieve_filtered_hotels(
    *,
    page: Annotated[int, fastapi.Query(ge=1)] = 1,
    limit: Annotated[int, fastapi.Query(ge=1)] = 10,
    skip: Annotated[int, fastapi.Depends(dependencies.calculate_skip)],
    search_word: Annotated[str, fastapi.Body(min_length=3)],
    collection: Annotated[
        motor_core.AgnosticCollection,
        fastapi.Depends(database_client.client.get_hotels_collection)
    ],
) -> responses.JSONResponse:
    """
    Retrieve filtered hotels records.

    Retrieves a list of hotels based on a search word with optional pagination.

    Parameters:
    - `page` (int, query): The current page number (default: 1).
    - `limit` (int, query): The number of hotels per page (default: 10).
    - `skip` (int, calculated): The number of hotels to skip based on pagination.
    - `search_word` (str, body): The search word used to filter hotels (min length: 3).
    - `collection` (motor_core.AgnosticCollection, dependency): MongoDB collection for hotels.

    Returns:
    - JSONResponse: A JSON response containing filtered hotel data, pagination info, and the limit.
    """

    search_filter = {
        '$or': [
            {'city': {'$regex': f'.*{search_word}.*', '$options': 'i'}},
            {'country': {'$regex': f'.*{search_word}.*', '$options': 'i'}},
            {'name': {'$regex': f'.*{search_word}.*', '$options': 'i'}}
        ]
    }
    cursor = collection.find(
        search_filter,
        projection={'_id': 0, 'id': 1, 'city': 1, 'country': 1, 'name': 1}
    ).sort('id').skip(skip).limit(limit)
    found_hotels_number = await collection.count_documents(search_filter)
    pages = math.ceil(found_hotels_number / limit)

    hotels = await cursor.to_list(length=limit)
    return responses.JSONResponse(content={
        'current_page': page, 'pages': pages, 'hotels': hotels, 'limit': limit
    })
