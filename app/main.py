from fastapi import FastAPI, Request
from mangum import Mangum

from app.api.api_v1.api import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    """
    Creates and initializes FastAPI application.
    """
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

            if "pathParameters" in request.scope["aws.event"]:
                path_parameters = request.scope["aws.event"]["pathParameters"]
                if path_parameters is not None and "proxy" in path_parameters:
                    request.scope["path"] = f"/{path_parameters['proxy']}"
                    root_path = context["path"][: context["path"].find(path_parameters["proxy"])]
                    request.scope["root_path"] = root_path

    response = await call_next(request)
    return response


handler = Mangum(app)
