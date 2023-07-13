from uuid import UUID

from pydantic import BaseModel, Field

from config import VALUE_MAX_LENGTH
from schemas.common import IdentifiableSchema, TimestampedSchema, UpdateRequestSchema


class PostSchema(IdentifiableSchema, TimestampedSchema):
    author_id: UUID
    text: str = Field(..., max_length=VALUE_MAX_LENGTH)
    is_public: bool | None = Field(True)

    class Config:
        orm_mode = True


class PostCreateSchema(BaseModel):
    text: str = Field(..., max_length=VALUE_MAX_LENGTH)
    is_public: bool | None = Field(True)


class PostUpdateSchema(UpdateRequestSchema):
    text: str | None = Field(None, max_length=VALUE_MAX_LENGTH)
    is_public: bool | None
