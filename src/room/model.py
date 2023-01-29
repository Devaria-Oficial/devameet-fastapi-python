from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.auth.model import User
from src.meet.model import Meet

class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(100), nullable=False)
    name = Column(String(100), index=True, nullable=False)
    avatar = Column(String(100), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    orientation = Column(String, nullable=False, default='TOP')
    muted = Column(Boolean, nullable=False, default=False)
    meet_id = Column(Integer, ForeignKey(Meet.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    meet = relationship(Meet)
    user = relationship(User)

    def to_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'avatar': self.avatar,
            'x': self.x,
            'y': self.y,
            'orientation': self.orientation,
            'muted': self.muted,
            'meet': str(self.meet_id),
            'user': str(self.user_id),
            'clientId': self.client_id,
        }