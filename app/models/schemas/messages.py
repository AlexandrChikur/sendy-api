from typing import List

import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat
from pydantic import PrivateAttr
from pydantic.class_validators import validator

from app.models.domain.messages import Message
from app.models.schemas.rwschema import RWSchema


class MessageInCreate(RWSchema):
    content: str
    numbers: List[str]
    _status_code: int = PrivateAttr(
        110
    )  # TODO: Dont use numeric. Do it with enums or kinda like that

    @property
    def status_code(self) -> int:
        return self._status_code

    @validator("content")
    def min_content_len(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Message length should be greater than 6")
        return v

    @validator("numbers")
    def numbers_list_len(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("You must specify at least one phone number")
        if len(v) > 20:
            raise ValueError("You can't create message with more than 20 numbers")
        return v

    @validator("numbers", always=True, each_item=True)
    def valid_number(cls, number: str) -> str:
        if len(number) < 6:
            raise ValueError("Number length should be greater than 6")
        if len(number) > 17:
            raise ValueError("Number length should be less than 17")
        try:
            phone_number = phonenumbers.parse(number)
        except NumberParseException as exc:
            raise ValueError(exc)
        if not phonenumbers.is_possible_number(phone_number):
            raise ValueError(f"Provided number `{number}` is not possible")
        return phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)


class MessagesInResponse(RWSchema):
    messages: List[Message]
