"""Database helper and connection management for game data SQLite DB."""

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent / "game_data.db"


def get_db_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Return a sqlite3 connection with sqlite3.Row row factory."""
    target = db_path or DB_PATH
    conn = sqlite3.connect(str(target))
    conn.row_factory = sqlite3.Row
    return conn
