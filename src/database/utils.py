import duckdb
from .db import DATABASE_FILE


def get_games_to_update():
    # Get game_pk that are in game_snapshots table but not in game_results table
    query = """
    SELECT distinct game_pk from game_snapshots
    WHERE game_pk NOT IN (SELECT distinct game_pk from game_results)
    """
    conn = duckdb.connect(DATABASE_FILE).cursor()
    return [r[0] for r in conn.execute(query).fetchall()]
