import unittest
import sqlite3
from game.data.db import get_db_connection, DB_PATH
from game.data.prologue import (
    get_prologue_metadata,
    get_prologue_factions,
    get_prologue_items,
    get_prologue_locations,
    get_prologue_quests,
    get_prologue_npcs,
)


class TestDatabaseIntegrity(unittest.TestCase):
    def test_database_exists_and_connected(self):
        self.assertTrue(DB_PATH.exists())
        conn = get_db_connection()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()

    def test_database_table_counts(self):
        conn = get_db_connection()
        tables = ["metadata", "factions", "items", "locations", "quests", "npcs", "dialogues"]
        for tbl in tables:
            cur = conn.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = cur.fetchone()[0]
            self.assertGreater(count, 0, f"Table {tbl} should not be empty")
        conn.close()

    def test_all_dialogues_refer_to_valid_npcs(self):
        conn = get_db_connection()
        cur = conn.execute("SELECT DISTINCT npc_id FROM dialogues")
        dialogue_npc_ids = {row[0] for row in cur.fetchall()}
        cur = conn.execute("SELECT npc_id FROM npcs")
        npc_ids = {row[0] for row in cur.fetchall()}
        conn.close()
        for d_npc in dialogue_npc_ids:
            self.assertIn(d_npc, npc_ids, f"Dialogue NPC {d_npc} not found in npcs table")


if __name__ == "__main__":
    unittest.main()
