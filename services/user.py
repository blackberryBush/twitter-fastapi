from typing import List
from uuid import UUID

from sqlalchemy import select, update

from database.session import SessionScope
from database.tables import User
from schemas.paginator import Paginator
from schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema
from services.hashing import HashingService


class UserService:

    @staticmethod
    async def create_user(user_data: UserCreateSchema) -> UserSchema:
        new_user = User(username=user_data.username, password_hash=HashingService.hash_password(user_data.password))
        async with SessionScope.get_session() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        return UserSchema.from_orm(new_user)

    @staticmethod
    async def get_user(id: UUID | None = None, username: str | None = None) -> UserSchema | None:
        if not id and not username:
            return None
        stmt = select(User).where(User.id == id if id else User.username == username)
        async with SessionScope.get_session() as session:
            user = (await session.execute(stmt)).scalar()
            if user:
                return UserSchema.from_orm(user)

    @staticmethod
    async def get_users(skip: int = 0, limit: int | None = None) -> List[UserSchema]:
        stmt = Paginator.add_pagination_rules(select(User), skip, limit).where(User.is_deleted == False)
        async with SessionScope.get_session() as session:
            users = (await session.execute(stmt)).scalars()
            return [UserSchema.from_orm(user) for user in users]

    @staticmethod
    async def update_user(id: UUID, user_data: UserUpdateSchema) -> UserSchema | None:
        raise ValueError(id, user_data)
        if user_data.password is not None:
            user_data.password_hash = HashingService.hash_password(user_data.password)
        print(user_data)
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                update(User).where(User.id == id, User.is_deleted == False).values(
                    **user_data.dict(exclude_unset=True)
                ).returning(*User.all_fields())
            )).all()
            if result:
                await session.commit()
                return UserSchema.from_orm(*result)

    @staticmethod
    async def delete_user(id: UUID) -> UserSchema | None:
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                update(User).where(User.id == id, User.is_deleted == False).values(
                    is_deleted=True
                ).returning(*User.all_fields())
            )).all()
            if result:
                await session.commit()
                return UserSchema.from_orm(*result)

    @staticmethod
    async def authenticate_user(username: str, password: str) -> UserSchema | None:
        password_hash = HashingService.hash_password(password)
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                select(User).where(
                    User.is_deleted == False and User.username == username and User.password_hash == password_hash)
            )).scalar()
            if result:
                return UserSchema.from_orm(result)
