from fastapi import FastAPI, Request, status
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ipaddress import ip_address
from src.conf.config import settings
from src.routes import auth, contacts, users, db, seed
from typing import Callable

import re
import redis.asyncio as redis
import uvicorn

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


banned_ips = [
    # ip_address("127.0.0.1"),
    ip_address("0.0.0.1"),
]


@app.middleware("http")
async def ban_ips(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip in banned_ips:
        print(f"{ip = }")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"}
        )
    response = await call_next(request)
    return response


user_agent_ban_list = [r"Googlebot", r"Python-urllib"]


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            print(f"{ban_pattern = }")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "You are banned"},
            )
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Welcome! This is Homework 13"}


app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")
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
