from sqlalchemy import Column, String, ForeignKey, Uuid
from sqlalchemy.orm import relationship

from database.tables.abstract.deletable import DeletableAbstractTable
from database.tables.abstract.identifiable import IdentifiableAbstractTable
from database.tables.abstract.timestamped import TimestampedAbstractTable


class Attachment(DeletableAbstractTable, IdentifiableAbstractTable, TimestampedAbstractTable):
    __tablename__ = 'attachment'
    post_id = Column(Uuid, ForeignKey('post.id'))
    post = relationship('Post', back_populates='attachments')
    url = Column(String)

    @staticmethod
    def all_fields():
        return [__class__.id,
                __class__.post_id,
                __class__.url,
                __class__.created_at,
                __class__.modified_at,
                __class__.is_deleted]
