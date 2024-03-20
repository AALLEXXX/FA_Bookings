from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from .admin.auth import authentication_backend
from .admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from .bookings.router import router as router_bookings
from .config import settings
from .database import engine
from .hotels.rooms.router import router as rooms_router
from .hotels.router import router as hotel_router
from .pages.router import router as pages_router
from .static.images.router import router as images_router
from .users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


app.mount("/static", StaticFiles(directory="static/"), "static")
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(hotel_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)


@app.get("/api/me")
async def home():
    pass
