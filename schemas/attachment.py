from uuid import UUID

from pydantic import Field, BaseModel

from schemas.common import UpdateRequestSchema, IdentifiableSchema, TimestampedSchema


class AttachmentSchema(IdentifiableSchema, TimestampedSchema):
    post_id: UUID
    url: str = Field(...)

    class Config:
        orm_mode = True


class AttachmentCreateSchema(BaseModel):
    post_id: UUID
    url: str = Field(...)


class AttachmentUpdateSchema(UpdateRequestSchema):
    url: str = Field(...)
