from typing import List, Optional

import phonenumbers
from phonenumbers import PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException
from pydantic import BaseModel
from pydantic.class_validators import validator

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class PhoneNumber(BaseModel):
    number: str

    @validator("number", always=True)
    def valid_number(cls, number: str) -> str:
        try:
            phone_number = phonenumbers.parse(number)
        except NumberParseException as exc:
            raise ValueError(exc)
        if not phonenumbers.is_possible_number(phone_number):
            raise ValueError(f"Provided number `{number}` is not possible")
        return phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)

    @validator("number", always=True)
    def number_len(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Number length should be greater than 6")
        if len(v) > 17:
            raise ValueError("Number length should be less than 17")
        return v


class StatusMessageMeta(BaseModel):
    status_code: int
    status_name: str
    status_description: str


class Message(RWModel, DateTimeModelMixin, IDModelMixin):
    content: str
    author_id: int
    numbers: List[PhoneNumber]
    status_meta: Optional[StatusMessageMeta]

    class Config:
        underscore_attrs_are_private = True

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
            raise ValueError("You can't create message with more than 20 numbeers")
        return v
