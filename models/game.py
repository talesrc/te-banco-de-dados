from sqlalchemy import Column, Integer, String
from database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True, name="game_id")
    name = Column(String, nullable=False, name="game_name")
    year = Column(Integer, nullable=False, name="game_year")
    genre = Column(String, nullable=False, name="game_genre")
