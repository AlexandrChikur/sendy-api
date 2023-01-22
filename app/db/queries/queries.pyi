"""Typings for queries generated by aiosql"""
import datetime

from asyncpg import Connection, Record

class UsersQueriesMixin:
    async def get_user_by_email(self, conn: Connection, *, email: str) -> Record: ...
    async def get_user_by_username(
        self, conn: Connection, *, username: str
    ) -> Record: ...
    async def create_new_user(
        self,
        conn: Connection,
        *,
        username: str,
        email: str,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        salt: str,
        hashed_password: str,
        is_active: bool
    ) -> Record: ...

class Queries(
    UsersQueriesMixin,
): ...

queries: Queries
