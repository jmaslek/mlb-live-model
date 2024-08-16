from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class GameSnapshotDB(Base):
    __tablename__ = "game_snapshots"

    id = Column(Integer, Sequence("my_sequence"), primary_key=True)
    game_pk = Column(Integer)
    game_guid = Column(String)
    home_team = Column(String)
    away_team = Column(String)
    date = Column(String)
    inning = Column(Integer)
    is_top_inning = Column(Boolean)
    balls = Column(Integer)
    strikes = Column(Integer)
    outs = Column(Integer)
    pitcher = Column(String)
    batter = Column(String)
    runner_on_first = Column(Boolean)
    runner_on_second = Column(Boolean)
    runner_on_third = Column(Boolean)
    home_score = Column(Integer)
    away_score = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)


class GameResultDB(Base):
    __tablename__ = "game_results"

    id = Column(Integer, Sequence("my_sequence"), primary_key=True)
    game_pk = Column(Integer)
    home_score = Column(Integer)
    away_score = Column(Integer)
    home_win = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.datetime.now)
