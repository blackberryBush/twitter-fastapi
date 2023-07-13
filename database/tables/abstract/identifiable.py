from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PSQL_UUID

from database.base import Base


class IdentifiableAbstractTable(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(PSQL_UUID(as_uuid=True), primary_key=True, default=uuid4)
