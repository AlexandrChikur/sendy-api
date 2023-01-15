from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_versioning import VersionedFastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api import api_v1
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.core.config import get_app_settings
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    # Include version routers
    application.include_router(api_v1.router)

    versioned_application = VersionedFastAPI(
        application,
        version_format="{major}.{minor}",
        prefix_format=settings.api_prefix + "/v{major}",
        default_version=(
            int(settings.version.split(".")[0]),
            int(settings.version.split(".")[1]),
        ),
        enable_latest=True,
        version=settings.version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )

    versioned_application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    versioned_application.add_event_handler(
        "startup",
        create_start_app_handler(versioned_application, settings),
    )
    versioned_application.add_event_handler(
        "shutdown",
        create_stop_app_handler(versioned_application),
    )

    versioned_application.add_exception_handler(HTTPException, http_error_handler)
    versioned_application.add_exception_handler(
        RequestValidationError, http422_error_handler
    )

    return versioned_application


app = get_application()
