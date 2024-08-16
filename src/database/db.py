from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

from ..models.game_snapshot import GameSnapshot
from .models import GameSnapshotDB, GameResultDB
from ..models.game_result import GameResult

DATABASE_FILE = "mlb_live.db"
DATABASE_URL = f"duckdb:///{DATABASE_FILE}"
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)


def insert_to_db(games: list[GameSnapshot]):
    with session() as db:
        for game in games:
            db.add(GameSnapshotDB(**game.model_dump()))
        db.commit()


def insert_game_result_to_db(game_results: list[GameResult]):
    with session() as db:
        for game_result in game_results:
            db.add(GameResultDB(**game_result.model_dump()))
        db.commit()
