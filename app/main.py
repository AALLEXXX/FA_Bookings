from fastapi import FastAPI
from sqladmin import Admin
from .bookings.router import router as router_bookings 
from .users.router import router as router_users 
from .hotels.router import router as hotel_router
from .hotels.rooms.router import router as rooms_router
from .pages.router import router as pages_router
from .static.images.router import router as images_router 
from fastapi.staticfiles import StaticFiles  
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from .database import engine
from .config import settings

from .admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from .admin.auth import authentication_backend

@asynccontextmanager
async def lifespan(app: FastAPI):
    # logger.info("Service started")
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # logger.info("Service exited")


app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


app.mount('/static', StaticFiles(directory='app/static'), 'static')
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(hotel_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)

# @app.get('/api')
# async def home():
#     return {'message':'Alexandria'}



@app.get('/api/me')
async def home():
    pass