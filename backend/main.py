import uvicorn
from contextlib import asynccontextmanager
from models import Base
from db import session_manager
from fastapi import FastAPI
from api.base import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with session_manager.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield

    finally:
        if session_manager.engine is not None:
            # async with session_manager.engine.begin() as connection:
            #     await connection.run_sync(Base.metadata.drop_all)
            await session_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
