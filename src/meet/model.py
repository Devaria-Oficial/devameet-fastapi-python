import random
import string
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base
    

class Meet(Base):
    __tablename__ = 'meets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    color = Column(String(7), nullable=False, default='#000000')
    link = Column(String(100), index=True, nullable=False)

    object_meets = relationship("ObjectMeet", back_populates="meet")

    def __init__(self, **kwargs):
        super(Meet, self).__init__(**kwargs)

        if not self.link:
            meet_link_generator = MeetLinkGenerator()
            self.link = meet_link_generator.generate()



class ObjectMeet(Base):
    __tablename__ = 'object_meet'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z_index = Column(Integer, nullable=False)
    orientation = Column(String, nullable=False, default='TOP')
    meet_id = Column(Integer, ForeignKey(Meet.id), nullable=False)

    meet = relationship(Meet, back_populates="object_meets")


class MeetLinkGenerator:
    def __init__(self):
        self.characters = string.ascii_lowercase + string.digits

    def _generate_section(self, length):
        return ''.join(random.choice(self.characters) for _ in range(length))

    def generate(self):
        return '-'.join([self._generate_section(3), self._generate_section(4), self._generate_section(3)])