from pydantic import BaseModel


class GameResult(BaseModel):
    game_pk: int
    home_final_score: int
    away_final_score: int
    home_win: bool
