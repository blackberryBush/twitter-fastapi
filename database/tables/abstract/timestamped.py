from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class TimestampedAbstractTable(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now(), onupdate=func.now())
