from pydantic import BaseModel


class GameResult(BaseModel):
    game_pk: int
    home_score: int
    away_score: int
    home_win: bool
