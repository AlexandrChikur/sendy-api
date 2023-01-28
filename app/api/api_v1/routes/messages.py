from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_websocket_pubsub.pub_sub_server import PubSubEndpoint
from fastapi_websocket_rpc.logger import LoggingModes
from fastapi_websocket_rpc.logger import logging_config as ws_logging_config

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.messages import MessagesRepository
from app.models.domain.messages import Message
from app.models.schemas.messages import MessageInCreate, MessagesInResponse
from app.models.schemas.users import User
from app.resources import strings
from app.services.sockets import publish_content

ws_logging_config.set_mode(
    LoggingModes.LOGURU, level=get_app_settings().logging_level
)  # TODO: Not might be here
settings = get_app_settings()
router = APIRouter()

ws_endpoint = PubSubEndpoint()
ws_endpoint.register_route(router, "/subscribe")


@router.get(
    "/",
    response_model=MessagesInResponse,
    name="messages:get-messages",
    status_code=status.HTTP_200_OK,
    summary="Get user's messages",
)  # TODO: Do nice paging
async def get_messages(
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    sent_included: bool = Query(
        False,
        title="With sent messages",
        description="Include sent messages in response",
    ),
    user: User = Depends(get_current_user_authorizer()),
) -> MessagesInResponse:
    """An interface for retrieving user's messages.
    Now able to return last 5000 messages
    """
    msgs = await messages_repo.get_user_messages(
        user_id=user.id, sent_included=sent_included
    )
    return MessagesInResponse(messages=msgs)


@router.post(
    "/create",
    response_model=Message,
    name="messages:create-message",
    summary="Create message that should be sent out",
)
async def create_message(
    message: MessageInCreate = Body(
        ...,
        example=MessageInCreate(
            content="Example message content",
            numbers=["+77863335334", "+7(925)-38-161-74"],
        ),
    ),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
    """An interface for retrieving user's messages"""
    message = await messages_repo.create_message(user=user, message_body=message)
    await publish_content(
        endpoint=ws_endpoint,
        topic=f"messages:/uid-{user.id}/uname-{user.username}",
        data=message,
    )
    updated_message = await messages_repo.update_status_code(
        message=message, status_code=120
    )  # TODO: Refactor to use statuses correctly
    return updated_message


@router.get(
    "/{id}",
    name="messages:get-concrete-message",
    response_model=Message,
    summary="Get concrete message",
)
async def get_concrete_message(
    message_id: int = Query(..., alias="id", le=1, title="Message ID"),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
    """Get concrete message with it's meta info on current moment"""
    try:
        message = await messages_repo.get_message_by_id(message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.MESSAGE_DOES_NOT_EXIST_ERROR,
        )
    if message.author_id != user.id:  # TODO: Maybe move to services
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.NOT_OBJECT_OWNER
        )
    return message


@router.post(
    "/{id}/received",
    name="messages:mark-message-as-received",
    response_model=Message,
    summary="Mark message as received",
    tags=["Internal"],
    include_in_schema=settings.debug,
)
async def mark_as_received(
    message_id: int = Query(..., alias="id"),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
    """When client-side application (e.g. like mobile app) got some message
    it should tell about it's **received** this message
    """
    try:
        message = await messages_repo.get_message_by_id(message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.MESSAGE_DOES_NOT_EXIST_ERROR,
        )
    if message.author_id != user.id:  # TODO: Maybe move to services
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.NOT_OBJECT_OWNER
        )
    updated_message = await messages_repo.update_status_code(
        message=message, status_code=130
    )  # TODO: Refactor to use statuses correctly
    return updated_message


@router.post(
    "/{id}/sent",
    name="messages:mark-message-as-sent",
    response_model=Message,
    summary="Mark message as sent",
    tags=["Internal"],
    include_in_schema=settings.debug,
)
async def mark_as_sent(
    message_id: int = Query(..., alias="id"),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
    """When client-side application (e.g. like mobile app) got some message,
    it should tell about it's **sent** this message
    """
    try:
        message = await messages_repo.get_message_by_id(message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.MESSAGE_DOES_NOT_EXIST_ERROR,
        )
    if message.author_id != user.id:  # TODO: Maybe move to services
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.NOT_OBJECT_OWNER
        )
    updated_message = await messages_repo.update_status_code(
        message=message, status_code=140
    )  # TODO: Refactor to use statuses correctly
    return updated_message
