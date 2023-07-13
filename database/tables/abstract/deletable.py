from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class DeletableAbstractTable(Base):
    __abstract__ = True

    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
