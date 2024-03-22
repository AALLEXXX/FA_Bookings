from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
import sentry_sdk
from sqladmin import Admin

from .admin.auth import authentication_backend
from .admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from .bookings.router import router as router_bookings
from .config import settings
from .database import engine
from .hotels.rooms.router import router as rooms_router
from .custom_logger import logger
from .hotels.router import router as hotel_router
from .pages.router import router as pages_router
from .static.images.router import router as images_router
from .users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


# sentry_sdk.init(
#     dsn=settings.SENTRY_SDK,
#     traces_sample_rate=1.0,

#     profiles_sample_rate=1.0,
# )


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(hotel_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    lifespan=lifespan
    # description="Greet users with a nice message",
    # middleware=[Middleware(add_process_time_header, secret_key="mysecretkey")],
)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


app.mount("/app/static", StaticFiles(directory="app/static/"), "/static")

