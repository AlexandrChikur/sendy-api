from typing import List

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.messages import Message, PhoneNumber, StatusMessageMeta
from app.models.schemas.messages import MessageInCreate
from app.models.schemas.users import User


class MessagesRepository(BaseRepository):
    async def get_message_by_id(self, *, message_id: int) -> Message:
        message_row = await queries.get_message_by_id(
            self.connection, message_id=message_id
        )
        if message_row:
            message_meta = StatusMessageMeta(**dict(message_row))
            return Message(
                **dict(message_row),
                numbers=[PhoneNumber(number=n) for n in message_row["numbers_arr"]],
                status_meta=message_meta,
            )

        raise EntityDoesNotExist(f"Message with ID: {message_id} does not exist")

    async def get_message_numbers_by_id(self, message_id: int) -> List[PhoneNumber]:
        phones_rows = await queries.get_message_numbers(
            self.connection, message_id=message_id
        )
        return [PhoneNumber(**dict(row)) for row in phones_rows]

    async def create_message(
        self, *, user: User, message_body: MessageInCreate
    ) -> Message:
        message = Message(**message_body.dict(), author_id=user.id)
        async with self.connection.transaction():
            message_row = await queries.create_message(
                self.connection,
                content=message.content,
                user_id=user.id,
                status_code=message_body.status_code,
                created_at=message.created_at,
                updated_at=message.updated_at,
            )
            message = message.copy(update=dict(message_row))
            numbers_rows = []
            for n in message.numbers:
                row = await queries.create_message_number(
                    self.connection, number=n.number, message_id=message.id
                )
                numbers_rows.append(row)
        return await self.get_message_by_id(message_id=message.id)

    async def update_status_code(
        self, *, message: Message, status_code: int
    ) -> Message:
        updated_message = Message(
            id=message.id,
            content=message.content,
            numbers=message.numbers,
            author_id=message.author_id,
        )
        if message:
            async with self.connection.transaction():
                message_row = await queries.update_status_code(
                    self.connection,
                    message_id=updated_message.id,
                    updated_at=updated_message.updated_at,
                    status_code=status_code,
                )
        return await self.get_message_by_id(message_id=updated_message.id)

    async def get_user_messages(
        self, *, user_id: int, sent_included: bool
    ) -> List[Message]:
        if sent_included:
            messages_rows = await queries.get_user_messages(
                self.connection, user_id=user_id, status_code=140
            )  # TODO: Refactor to use statuses correctly
        else:
            messages_rows = await queries.get_user_messages(
                self.connection, user_id=user_id, status_code=130
            )  # TODO: Refactor to use statuses correctly
        result = []
        for row in messages_rows:
            meta = StatusMessageMeta(**dict(row))
            print(row)
            msg = Message(
                **dict(row),
                status_meta=meta,
                numbers=[PhoneNumber(number=n) for n in row["numbers_arr"]],
            )
            result.append(msg)

        return result
