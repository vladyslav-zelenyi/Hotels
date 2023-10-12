import contextlib

import fastapi

import database_client
from routers import hotels


@contextlib.asynccontextmanager
async def lifespan(_application: fastapi.FastAPI):
    yield
    await database_client.client.close()

app = fastapi.FastAPI(lifespan=lifespan)
app.include_router(hotels.router)
