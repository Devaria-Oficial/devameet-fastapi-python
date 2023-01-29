from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Meet(Base):
    __tablename__ = 'meets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    color = Column(String(7), nullable=False, default='#000000')
    link = Column(String(100), index=True, nullable=False)