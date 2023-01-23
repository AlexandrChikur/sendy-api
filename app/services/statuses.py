from typing import List

from fastapi import Depends

from app.api.dependencies.database import get_repository
from app.db.repositories.statuses import StatusesRepository
from app.models.schemas.statuses import StatusMeta


async def get_statuses_by_header_id(
    repo: StatusesRepository = Depends(get_repository(StatusesRepository)), *, header_id
) -> List[StatusMeta]:
    return await repo.get_statuses_by_header_id(header_id=header_id)
