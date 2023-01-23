from typing import Any, Dict, Literal

from app.models.domain.rwmodel import RWModel
from app.models.schemas.rwschema import RWSchema


class SocketRequestArgument(RWSchema):
    arg: Literal["topics"]


class SocketRequest(RWSchema):
    method: Literal["subscribe"]
    arguments: Dict[SocketRequestArgument, Any]


class SocketRequestSchema(RWModel):
    request: SocketRequest
