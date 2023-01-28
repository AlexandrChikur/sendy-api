import uuid
from typing import Union

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.resources import strings


def _capitalize_first_words(exc_list: str) -> str:
    """Capitalize first words in each sentence in exception message"""
    return ". ".join(
        [
            sentence[0].title() + sentence[1:]
            for sentence in [
                sentence[0].strip() + sentence[1:] for sentence in exc_list.split(".")
            ]
        ]
    )


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        {"errors": [_capitalize_first_words(exc.detail)]}, status_code=exc.status_code
    )


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}


async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    error_link_id = uuid.uuid4()
    logger.exception(
        f"Got an unexpected error with id-{error_link_id}, err: {exc}. URL: {request.url}"
    )
    client_message = f"{_capitalize_first_words(strings.INTERNAL_ERROR_MESSAGE)}. Error ID: {error_link_id}. Give it to support."
    return JSONResponse(
        {"errors": [client_message]}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
