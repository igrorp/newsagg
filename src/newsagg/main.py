from contextlib import asynccontextmanager

from fastapi import FastAPI

from newsagg.config.database import on_startup
from newsagg.routers.rest_api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # App startup
    await on_startup()
    yield
    # App shutdown


app = FastAPI(lifespan=lifespan)

app.include_router(router)
