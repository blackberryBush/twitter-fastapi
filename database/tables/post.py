from sqlalchemy import Column, String, ForeignKey, Boolean, Uuid
from sqlalchemy.orm import relationship

from database.tables.abstract.deletable import DeletableAbstractTable
from database.tables.abstract.identifiable import IdentifiableAbstractTable
from database.tables.abstract.timestamped import TimestampedAbstractTable


class Post(DeletableAbstractTable, IdentifiableAbstractTable, TimestampedAbstractTable):
    __tablename__ = 'post'
    author_id = Column(Uuid, ForeignKey('user.id'))
    author = relationship('User', back_populates='posts')
    text = Column(String)
    is_public = Column(Boolean)

    attachments = relationship('Attachment', order_by='Attachment.id', back_populates='post')

    @staticmethod
    def all_fields():
        return [__class__.id,
                __class__.author_id,
                __class__.text,
                __class__.is_public,
                __class__.created_at,
                __class__.modified_at,
                __class__.is_deleted]
