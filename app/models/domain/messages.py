from typing import List, Optional

from pydantic import BaseModel

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class StatusMessageMeta(BaseModel):
    status_code: int
    status_name: str
    status_description: str


class Message(RWModel, DateTimeModelMixin, IDModelMixin):
    content: str
    author_id: int
    numbers: List[str]
    status_meta: Optional[StatusMessageMeta]

    class Config:
        underscore_attrs_are_private = True
