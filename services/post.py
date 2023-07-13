from typing import List
from uuid import UUID

from sqlalchemy import select, update

from database import SessionScope
from database.tables import Post, Attachment
from schemas.paginator import Paginator
from schemas.post import PostCreateSchema, PostSchema, PostUpdateSchema


class PostService:

    @staticmethod
    async def create_post(post_data: PostCreateSchema, user_id: UUID) -> PostSchema:
        new_post = Post(author_id=user_id, **dict(post_data))
        async with SessionScope.get_session() as session:
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
        return PostSchema.from_orm(new_post)

    @staticmethod
    async def get_posts(skip: int = 0, limit: int | None = None) -> List[PostSchema]:
        stmt = Paginator.add_pagination_rules(select(Post), skip, limit).where(Post.is_deleted == False)
        async with SessionScope.get_session() as session:
            posts = (await session.execute(stmt)).scalars()
            return [PostSchema.from_orm(post) for post in posts]

    @staticmethod
    async def get_post(id: UUID) -> PostSchema | None:
        stmt = select(Post).where(Post.id == id, Post.is_deleted == False)
        async with SessionScope.get_session() as session:
            post = (await session.execute(stmt)).scalar()
            if post:
                return PostSchema.from_orm(post)

    @staticmethod
    async def update_post(id: UUID, post_data: PostUpdateSchema) -> PostSchema | None:
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                update(Post).where(Post.id == id, Post.is_deleted == False).values(
                    **post_data.dict(exclude_unset=True)
                ).returning(*Post.all_fields())
            )).all()
            if result:
                await session.commit()
                return PostSchema.from_orm(*result)

    @staticmethod
    async def delete_post(id: UUID) -> PostSchema | None:
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                update(Post).where(Post.id == id, Post.is_deleted == False).values(
                    is_deleted=True
                ).returning(*Post.all_fields())
            )).all()
            if result:
                await session.execute(
                    update(Attachment).where(Attachment.post_id == id).values(
                        is_deleted=True
                    )
                )
                await session.commit()
                return PostSchema.from_orm(*result)
