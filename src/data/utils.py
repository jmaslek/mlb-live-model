import httpx
import datetime
from ..models.game_snapshot import GameSnapshot

url = "https://statsapi.mlb.com/api/v1/schedule/games?sportId=1&hydrate=linescore&startDate={date}&endDate={date}"


def get_overview():
    response = httpx.get(url)
    return {
        "total_games_in_progress": response.json()["totalGamesInProgress"],
        "total_games": response.json()["totalGames"],
    }


def get_days_games(date: str | None = None):
    if date is None:
        date = datetime.date.today().strftime("%Y-%m-%d")

    response = httpx.get(url.format(date=date))
    games = response.json()["dates"][0]["games"]
    return games


def process_game(game: dict) -> GameSnapshot | None:
    if game["status"]["abstractGameState"] in ("Preview", "Final"):
        return
    try:
        line = game["linescore"]
        date = game["officialDate"]
        current_inning = line["currentInning"]
        is_top = line["isTopInning"]
        balls = line["balls"]
        strikes = line["strikes"]
        outs = line["outs"]
        game_pk = game["gamePk"]
        game_guid = game["gameGuid"]
        home_team = game["teams"]["away"]["team"]["name"]
        home_score = game["teams"]["home"]["score"]
        away_team = game["teams"]["home"]["team"]["name"]
        away_score = game["teams"]["away"]["score"]
        defense = line["defense"]
        pitcher = defense["pitcher"]["fullName"]

        offense = line["offense"]
        batter = offense["batter"]["fullName"]
        runner_on_first = bool(offense.get("first", False))
        runner_on_second = bool(offense.get("second", False))
        runner_on_third = bool(offense.get("third", False))
        return GameSnapshot(
            game_pk=game_pk,
            game_guid=game_guid,
            home_team=home_team,
            away_team=away_team,
            date=date,
            inning=current_inning,
            is_top_inning=is_top,
            balls=balls,
            strikes=strikes,
            outs=outs,
            runner_on_first=runner_on_first,
            runner_on_second=runner_on_second,
            runner_on_third=runner_on_third,
            pitcher=pitcher,
            batter=batter,
            home_score=home_score,
            away_score=away_score,
        )

    except KeyError:
        return None