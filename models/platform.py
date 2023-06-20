from sqlalchemy import Column, Integer, String
from database import Base


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, autoincrement=True, name="platform_id")
    name = Column(String, nullable=False, name="platform_name")
