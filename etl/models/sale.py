from sqlalchemy import Column, Integer, Float, ForeignKey
from database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True, name="sale_id")
    sales = Column(Float, nullable=False, name="sales_number")
    game_id = Column(Integer, ForeignKey('games.game_id'))
    publisher_id = Column(Integer, ForeignKey('publishers.publisher_id'))
    platform_id = Column(Integer, ForeignKey('platforms.platform_id'))
    region_id = Column(Integer, ForeignKey('regions.region_id'))
