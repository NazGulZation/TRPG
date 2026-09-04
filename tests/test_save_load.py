import os
import unittest
from pathlib import Path
from game.engine import GameEngine
from app import app


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

    def test_engine_save_load_dict(self):
        self.engine.player.current_hp = 18
        self.engine.player.dread = 66
        self.engine.player.sovereigns = 142
        self.engine.player.inventory.append("Mysterious Key")
        self.engine.bell_toll = 11
        self.engine.npcs["sister_vanya"].relationship = 92
        self.engine.npcs["sister_vanya"].is_romanced = True

        data = self.engine.save_to_dict()
        self.assertEqual(data["player"]["current_hp"], 18)
        self.assertEqual(data["player"]["dread"], 66)
        self.assertEqual(data["player"]["sovereigns"], 142)
        self.assertEqual(data["bell_toll"], 11)

        new_engine = GameEngine()
        ok = new_engine.load_from_dict(data)
        self.assertTrue(ok)
        self.assertEqual(new_engine.player.current_hp, 18)
        self.assertEqual(new_engine.player.dread, 66)
        self.assertEqual(new_engine.player.sovereigns, 142)
        self.assertIn("Mysterious Key", new_engine.player.inventory)
        self.assertEqual(new_engine.bell_toll, 11)
        self.assertEqual(new_engine.npcs["sister_vanya"].relationship, 92)
        self.assertTrue(new_engine.npcs["sister_vanya"].is_romanced)

    def test_engine_save_load_file(self):
        slot = "test_save_unit"
        self.engine.player.name = "GrimTestWanderer"
        self.engine.player.sovereigns = 777
        saved_path = self.engine.save_to_file(slot)
        self.assertTrue(os.path.exists(saved_path))

        new_engine = GameEngine()
        ok = new_engine.load_from_file(slot)
        self.assertTrue(ok)
        self.assertEqual(new_engine.player.name, "GrimTestWanderer")
        self.assertEqual(new_engine.player.sovereigns, 777)

        # Cleanup
        if os.path.exists(saved_path):
            os.remove(saved_path)

    def test_flask_save_load_continue_api(self):
        client = app.test_client()

        # Save via /api/save
        save_resp = client.post("/api/save", json={"slot": "api_test_slot"})
        self.assertEqual(save_resp.status_code, 200)
        data = save_resp.get_json()
        self.assertTrue(data.get("success"))

        # Check /api/saves
        saves_resp = client.get("/api/saves")
        self.assertEqual(saves_resp.status_code, 200)
        saves_list = saves_resp.get_json().get("saves", [])
        self.assertTrue(any(s["slot"] == "api_test_slot" for s in saves_list))

        # Continue via /api/continue
        cont_resp = client.post("/api/continue")
        self.assertEqual(cont_resp.status_code, 200)
        cont_data = cont_resp.get_json()
        self.assertTrue(cont_data.get("success"))

        # Load via /api/load
        load_resp = client.post("/api/load", json={"slot": "api_test_slot"})
        self.assertEqual(load_resp.status_code, 200)

        # Clean test file
        test_file = Path("saves/api_test_slot.json")
        if test_file.exists():
            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
