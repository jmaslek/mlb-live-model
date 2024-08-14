from pydantic import BaseModel


class GameSnapshot(BaseModel):
    game_pk: int
    game_guid: str
    home_team: str
    away_team: str
    date: str
    inning: int
    is_top_inning: bool
    balls: int
    strikes: int
    outs: int
    pitcher: str
    batter: str
    runner_on_first: bool
    runner_on_second: bool
    runner_on_third: bool
    home_score: int
    away_score: int
