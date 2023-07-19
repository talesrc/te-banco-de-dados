from sqlalchemy import Column, Integer, String
from database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, autoincrement=True, name="region_id")
    region = Column(String, nullable=False, name="region_name")
