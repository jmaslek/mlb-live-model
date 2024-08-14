from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

from ..models.game_snapshot import GameSnapshot
from .models import GameSnapshotDB

DATABASE_URL = "duckdb:///mlb_live.db"
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)


def insert_to_db(games: list[GameSnapshot]):
    with session() as db:
        for game in games:
            db.add(GameSnapshotDB(**game.model_dump()))
        db.commit()
