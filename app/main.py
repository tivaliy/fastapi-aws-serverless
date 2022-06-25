from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.api.health import health_router
from app.core.config import get_app_settings
from app.core.events import create_start_app_handler
from app.core.middleware import AWSAPIGatewayMiddleware


def create_application() -> FastAPI:
    """
    Creates and initializes FastAPI application.
    """
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.include_router(api_router, prefix=settings.api_v1_prefix)
    application.include_router(health_router, prefix="/ping", tags=["ping"])

    # Configure middleware
    application.add_middleware(AWSAPIGatewayMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )

    return application


app = create_application()


handler = Mangum(app)
