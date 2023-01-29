import random
import string
from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Meet(Base):
    __tablename__ = 'meets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    color = Column(String(7), nullable=False, default='#000000')
    link = Column(String(100), index=True, nullable=False)

    def __init__(self, **kwargs):
        super(Meet, self).__init__(**kwargs)

        if not self.link:
            meet_link_generator = MeetLinkGenerator()
            self.link = meet_link_generator.generate()

class MeetLinkGenerator:
    def __init__(self):
        self.characters = string.ascii_lowercase + string.digits

    def _generate_section(self, length):
        return ''.join(random.choice(self.characters) for _ in range(length))

    def generate(self):
        return '-'.join([self._generate_section(3), self._generate_section(4), self._generate_section(3)])