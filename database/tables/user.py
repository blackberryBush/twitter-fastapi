from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database.tables.abstract.deletable import DeletableAbstractTable
from database.tables.abstract.identifiable import IdentifiableAbstractTable
from database.tables.abstract.timestamped import TimestampedAbstractTable


class User(DeletableAbstractTable, IdentifiableAbstractTable, TimestampedAbstractTable):
    __tablename__ = 'user'
    username = Column(String, unique=True)
    password_hash = Column(String)

    posts = relationship('Post', order_by='Post.id', back_populates='author')

    @staticmethod
    def all_fields():
        return [__class__.id,
                __class__.username,
                __class__.created_at,
                __class__.modified_at,
                __class__.is_deleted]