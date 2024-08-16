from .utils import get_days_games, process_game, get_game_result
from ..database.db import insert_to_db, insert_game_result_to_db
import datetime
from apscheduler.schedulers.background import BlockingScheduler
from loguru import logger
import json
import pytz
from apscheduler.triggers.cron import CronTrigger
from ..database.utils import get_games_to_update
import time

# Set up Pacific Time zone
pacific_tz = pytz.timezone("US/Pacific")


def get_pacific_date():
    return datetime.datetime.now(pacific_tz).date()


_cache = set()


def get_games_into_db():
    logger.info("Getting games into db")
    games = get_days_games(date=get_pacific_date().strftime("%Y-%m-%d"))

    to_insert = []
    for game in games:
        processed_game = process_game(game)

        if processed_game:
            cache_check = json.dumps(
                {
                    "game_pk": game["gamePk"],
                    "game_guid": game["gameGuid"],
                    "home_team": game["teams"]["away"]["team"]["name"],
                    "away_team": game["teams"]["home"]["team"]["name"],
                    "date": game["officialDate"],
                    "inning": game["linescore"]["currentInning"],
                    "is_top_inning": game["linescore"]["isTopInning"],
                    "balls": game["linescore"]["balls"],
                    "strikes": game["linescore"]["strikes"],
                    "outs": game["linescore"]["outs"],
                },
                sort_keys=True,
            )
            if cache_check not in _cache:
                to_insert.append(processed_game)
                _cache.add(cache_check)

    if to_insert:
        logger.info(f"Inserting {len(to_insert)} games into db")
        insert_to_db(to_insert)
    else:
        logger.info("No games to insert")


def get_game_results_into_db():
    game_pk_list = get_games_to_update()
    logger.info(f"Getting game results for {len(game_pk_list)} games")
    game_results = []
    for game_pk in game_pk_list:
        game_result = get_game_result(gamePk=game_pk)
        if game_result:
            game_results.append(game_result)
    if game_results:
        logger.info(f"Inserting {len(game_results)} game results into db")
        insert_game_result_to_db(game_results)
    time.sleep(60 * 60 * 5)


def clear_cache():
    global _cache
    logger.info("Clearing cache")
    _cache.clear()
    logger.info("Cache cleared")


def main():
    scheduler = BlockingScheduler(timezone=pacific_tz)
    scheduler.add_job(get_games_into_db, "interval", seconds=30)
    scheduler.add_job(clear_cache, CronTrigger(hour=2, minute=0))
    scheduler.add_job(get_game_results_into_db, CronTrigger(hour=5, minute=0))

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Shutting down")
        scheduler.shutdown()


if __name__ == "__main__":
    get_game_results_into_db()
    main()
