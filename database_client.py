from motor import motor_asyncio

import settings


class MongoDBAsyncClient:
    """
    A MongoDB asynchronous client wrapper for interacting with a MongoDB database.

    This class provides a convenient and asynchronous interface for connecting to a MongoDB
    database using Motor and performing database operations.

    Args:
        host (str): The MongoDB server host.
        port (str): The MongoDB server port.

    Attributes:
        _client (motor_asyncio.AsyncIOMotorClient): The Motor asynchronous MongoDB client.
    """
    def __init__(self, host: str, port: int):
        self._client = motor_asyncio.AsyncIOMotorClient(f'mongodb://{host}:{port}')

    async def close(self):
        """Asynchronously closes the MongoDB client connection if a connection has been
        established."""
        if self._client.is_mongos:
            await self._client.close()

    def get_hotels_database(self):
        """Retrieves the MongoDB database for hotels."""
        return self._client['fornova_hotels']

    def get_hotels_collection(self):
        """Retrieves the MongoDB collection for hotel records."""
        return self.get_hotels_database()['hotels']


client = MongoDBAsyncClient(host=settings.DB_HOST, port=settings.DB_PORT)
