from pydantic import Field, BaseModel

from config import NAME_MAX_LENGTH
from schemas.common import IdentifiableSchema, TimestampedSchema, UpdateRequestSchema


class UserSchema(IdentifiableSchema, TimestampedSchema):
    username: str = Field(..., max_length=NAME_MAX_LENGTH)

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=NAME_MAX_LENGTH)
    password: str = Field(..., min_length=8, max_length=64,
                          regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')


class UserUpdateSchema(UpdateRequestSchema):
    username: str | None = Field(None, max_length=NAME_MAX_LENGTH)
    password: str | None = Field(None, min_length=8, max_length=64,
                                 regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
