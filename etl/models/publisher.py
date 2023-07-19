from sqlalchemy import Column, Integer, String
from database import Base


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, autoincrement=True, name="publisher_id")
    name = Column(String, nullable=False, name="publisher_name")
