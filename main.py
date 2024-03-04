from fastapi import FastAPI
from src.routes import auth, contacts, db, seed

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from src.routes import contacts, db, auth
from src.conf.config import settings

import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome! This is Homework 13"}


app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(db.router, prefix="")
app.include_router(seed.router, prefix="")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     r = await redis.Redis(
#         host=config.REDIS_DOMAIN,
#         port=config.REDIS_PORT,
#         db=0,
#         password=config.REDIS_PASSWORD,
#         encoding="utf-8",
#         decode_responses=True,
#     )
#     delay = await FastAPILimiter.init(r)
#     yield delay


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
