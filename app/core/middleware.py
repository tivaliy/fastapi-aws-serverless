from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

RequestResponseEndpoint = Callable[[Request], Awaitable[Response]]


class AWSAPIGatewayMiddleware(BaseHTTPMiddleware):
    """
    Handles the FastAPI root_path dynamically from the ASGI request data.

    https://github.com/jordaneremieff/mangum/issues/147
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        root_path = request.scope["root_path"]
        if root_path:
            # Assume set correctly in this case
            self.app.root_path = root_path

        else:
            # fetch from AWS requestContext
            if "aws.event" in request.scope:
                context = request.scope["aws.event"]["requestContext"]

                if "pathParameters" in request.scope["aws.event"]:
                    path_parameters = request.scope["aws.event"]["pathParameters"]
                    if path_parameters is not None and "proxy" in path_parameters:
                        request.scope["path"] = f"/{path_parameters['proxy']}"
                        root_path = context["path"][
                            : context["path"].find(path_parameters["proxy"])
                        ]
                        request.scope["root_path"] = root_path

        response = await call_next(request)
        return response
