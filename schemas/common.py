from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, root_validator


class IdentifiableSchema(BaseModel):
    id: UUID = Field(...)


class TimestampedSchema(BaseModel):
    created_at: datetime
    modified_at: datetime


class UpdateRequestSchema(BaseModel):
    @root_validator(pre=True)
    def check_if_not_all_fields_are_none(cls, values):
        if not values:
            raise ValueError("At least one field has to be passed for update.")
        return values
