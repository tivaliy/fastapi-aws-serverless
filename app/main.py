from fastapi import FastAPI, Request
from mangum import Mangum

from app.api.api_v1.api import api_router
from app.core.config import get_app_settings


def create_application() -> FastAPI:
    """
    Creates and initializes FastAPI application.
    """
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.include_router(api_router, prefix=settings.api_v1_prefix)

    return application


app = create_application()


@app.middleware("http")
async def set_root_path_for_api_gateway(request: Request, call_next):
    """
    Sets the FastAPI root_path dynamically from the ASGI request data.

    https://github.com/jordaneremieff/mangum/issues/147
    """

    root_path = request.scope["root_path"]
    if root_path:
        # Assume set correctly in this case
        app.root_path = root_path

    else:
        # fetch from AWS requestContext
        if "aws.event" in request.scope:
            context = request.scope["aws.event"]["requestContext"]

            if "customDomain" not in context:
                # Only works for stage deployments currently
                root_path = f"/{context['stage']}"

                if request.scope["path"].startswith(root_path):
                    request.scope["path"] = request.scope["path"][len(root_path) :]
                request.scope["root_path"] = root_path
                app.root_path = root_path

                # NOT IMPLEMENTED FOR customDomain
                # root_path = f"/{context['customDomain']['basePathMatched']}"

    response = await call_next(request)
    return response


handler = Mangum(app)
