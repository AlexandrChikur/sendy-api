from pydantic.class_validators import validator

from app.models.common import IDModelMixin
from app.models.schemas.rwschema import RWSchema


class Status(RWSchema, IDModelMixin):
    status_header_id: int
    status_code: int

    @validator("status_header_id")
    def valid_status_header_id(cls, id_: int) -> int:
        if (id_ % 100) != 0:
            raise Exception(f"Invalid status header ID provided: {id_}")

        return id_

    @validator("status_code")
    def valid_status_code_id(cls, code: int) -> int:
        if code < 1:
            raise Exception(
                f"Invalid status code provided: {code}. It can't be negative or decimal"
            )

        if code >= 100:
            raise Exception(
                f"Invalid status code provided: {code}. It can't be more than 99"
            )

        return code


class ConcreteStatusMeta(Status):
    status_code_name: str
    status_code_description: str


class StatusMeta(ConcreteStatusMeta):
    status_header_name: str
    status_header_description: str


# class MessageStatus(StatusMixin, IDModelMixin):
#     message_id: str
#
#
# class MessageStatusMeta(StatusMetaMixin, IDModelMixin):
#     message_id: str
