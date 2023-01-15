from typing import Any

from fastapi.routing import APIRouter
from fastapi_versioning import versioned_api_route


class VersionedAPIRouter(APIRouter):
    def __init__(
        self, major: int = 1, minor: int = 0, *args: Any, **kwargs: Any
    ) -> None:
        versioned_route_class = versioned_api_route(major, minor)
        super().__init__(*args, **kwargs, route_class=versioned_route_class)
        self.major = major
        self.minor = minor

    def include_router(self, *args, **kwargs):
        super().include_router(*args, **kwargs)
        for route in self.routes:
            try:
                route.endpoint._api_version = (self.major, self.minor)
            except AttributeError:
                # Support bound methods
                route.endpoint.__func__._api_version = (self.major, self.minor)
