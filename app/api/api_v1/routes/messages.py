from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_websocket_pubsub.pub_sub_server import PubSubEndpoint

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.messages import MessagesRepository
from app.models.domain.messages import Message
from app.models.schemas.messages import MessageInCreate, MessagesInReponse
from app.models.schemas.users import User
from app.resources import strings
from app.services.sockets import publish_content

router = APIRouter()

pubsub_endpoint = PubSubEndpoint()
pubsub_endpoint.register_route(router, "/subscribe")


# TODO: !!!!!! DOCUMENTATION EXAMPLES ETC...


@router.get(
    "/", response_model=MessagesInReponse, name="messages:get-messages"
)  # TODO: Do nice paging
async def get_messages(
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    sent_included: bool = Query(False),
    user: User = Depends(get_current_user_authorizer()),
) -> MessagesInReponse:
    """Returns last 5000 messages"""
    msgs = await messages_repo.get_user_messages(
        user_id=user.id, sent_included=sent_included
    )
    return MessagesInReponse(messages=msgs)


@router.post("/create", response_model=Message, name="messages:create-message")
async def create_message(
    message: MessageInCreate = Body(...),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
    message = await messages_repo.create_message(user=user, message_body=message)
    await publish_content(
        endpoint=pubsub_endpoint,
        topic=f"messages:/uid-{user.id}/uname-{user.username}",
        data=message,
    )
    updated_message = await messages_repo.update_status_code(
        message=message, status_code=120
    )  # TODO: Refactor to use statuses correctly
    return updated_message


@router.get(
    "/{id}", name="messages:get-concrete-message"
)  # TODO: !!!!!!! Maybe `fastapi_websocket_pubsub` provides functionality to receive response from socket. Can be implemented better.
async def get_concrete_message(
    message_id: int = Query(..., alias="id"),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
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
    "/{id}/received", name="messages:mark-message-as-received"
)  # TODO: !!!!!!! Maybe `fastapi_websocket_pubsub` provides functionality to receive response from socket. Can be implemented better.
async def mark_as_received(
    message_id: int = Query(..., alias="id"),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
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
    "/{id}/sent", name="messages:mark-message-as-sent"
)  # TODO: !!!!!!! Maybe `fastapi_websocket_pubsub` provides functionality to receive response from socket. Can be implemented better.
async def mark_as_sent(
    message_id: int = Query(..., alias="id"),
    messages_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> Message:
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


# @router.post()

# @router.get("/{id}/")
#
# @router.get("/{id}/status")
#
#
#
# @router.post("/my")
