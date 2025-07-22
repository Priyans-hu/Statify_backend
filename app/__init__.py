import asyncio
import os
from contextlib import asynccontextmanager

import redis.asyncio as redis
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.core.event_loop import set_event_loop
from app.middleware.org_slug_middleware import OrgSlugResolverMiddleware
from app.routes import (
    auth_routes,
    incident_routes,
    logs_route,
    metrics_router,
    organization_router,
    service_routes,
    status_routes,
    ws_routes,
)


def create_app():
    load_dotenv()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Redis cache setup
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))

        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=False,
        )

        FastAPICache.init(RedisBackend(redis_client), prefix="statify-cache")
        yield
        await redis_client.close()

    app = FastAPI(lifespan=lifespan)
    set_event_loop(asyncio.get_running_loop())

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # OrgSlug middleware
    app.add_middleware(OrgSlugResolverMiddleware)

    # Include routers
    app.include_router(auth_routes.router)
    app.include_router(logs_route.router)
    app.include_router(service_routes.router)
    app.include_router(ws_routes.router)
    app.include_router(incident_routes.router)
    app.include_router(status_routes.router)
    app.include_router(organization_router.router)
    app.include_router(metrics_router.router)

    return app
