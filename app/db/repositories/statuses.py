from typing import List

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.schemas.statuses import StatusMeta


class StatusesRepository(BaseRepository):
    async def get_status_by_id(self, *, status_id: int) -> StatusMeta:
        status_row = await queries.get_status_by_id(
            self.connection, status_id=status_id
        )
        if status_row:
            return StatusMeta(**dict(status_row))

        raise EntityDoesNotExist(f"Status row ID: {status_id} does not exist")

    async def get_statuses_by_header_id(self, *, header_id: int) -> List[StatusMeta]:
        status_rows = await queries.get_statuses_by_header_id(
            self.connection, header_id=header_id
        )
        if status_rows:
            return [StatusMeta(**dict(row)) for row in status_rows]

        raise EntityDoesNotExist(f"Statuses for header ID: {header_id} does not exist")
