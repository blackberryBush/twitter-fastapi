from typing import List
from uuid import UUID

from sqlalchemy import select, update

from database import SessionScope
from database.tables import Attachment
from schemas.attachment import AttachmentCreateSchema, AttachmentSchema, AttachmentUpdateSchema
from schemas.paginator import Paginator


class AttachmentService:

    @staticmethod
    async def create_attachment(attachment_data: AttachmentCreateSchema) -> AttachmentSchema:
        new_attachment = Attachment(**dict(attachment_data))
        async with SessionScope.get_session() as session:
            session.add(new_attachment)
            await session.commit()
            await session.refresh(new_attachment)
        return AttachmentSchema.from_orm(new_attachment)

    @staticmethod
    async def get_attachments(skip: int = 0, limit: int | None = None) -> List[AttachmentSchema]:
        stmt = Paginator.add_pagination_rules(select(Attachment), skip, limit).where(Attachment.is_deleted == False)
        async with SessionScope.get_session() as session:
            attachments = (await session.execute(stmt)).scalars()
            return [AttachmentSchema.from_orm(attachment) for attachment in attachments]

    @staticmethod
    async def get_attachment(id: UUID) -> AttachmentSchema | None:
        stmt = select(Attachment).where(Attachment.id == id, Attachment.is_deleted == False)
        async with SessionScope.get_session() as session:
            attachment = (await session.execute(stmt)).scalar()
            if attachment:
                return AttachmentSchema.from_orm(attachment)

    @staticmethod
    async def update_attachment(id: UUID, attachment_data: AttachmentUpdateSchema) -> AttachmentSchema | None:
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                update(Attachment).where(Attachment.id == id, Attachment.is_deleted == False).values(
                    **attachment_data.dict(exclude_unset=True)
                ).returning(*Attachment.all_fields())
            )).all()
            if result:
                await session.commit()
                return AttachmentSchema.from_orm(*result)

    @staticmethod
    async def delete_attachment(id: UUID) -> AttachmentSchema | None:
        async with SessionScope.get_session() as session:
            result = (await session.execute(
                update(Attachment).where(Attachment.id == id, Attachment.is_deleted == False).values(
                    is_deleted=True
                ).returning(*Attachment.all_fields())
            )).all()
            if result:
                await session.commit()
                return AttachmentSchema.from_orm(*result)
