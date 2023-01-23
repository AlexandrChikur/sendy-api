from typing import List

from pydantic import PrivateAttr

from app.models.domain.messages import Message, PhoneNumber
from app.models.schemas.rwschema import RWSchema


class MessageInCreate(RWSchema):
    content: str
    numbers: List[PhoneNumber]
    _status_code: int = PrivateAttr(
        110
    )  # TODO: Dont use numeric. Do it with enums or kinda like that

    @property
    def status_code(self) -> int:
        return self._status_code


class MessagesInResponse(RWSchema):
    messages: List[Message]
