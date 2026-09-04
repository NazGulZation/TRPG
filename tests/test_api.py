import unittest
from app import app, GAMES


class TestAPI(unittest.TestCase):
    def test_flask_api_routes(self):
        client = app.test_client()
        resp = client.get("/api/state")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["player"]["name"], "Wanderer")

    def test_flask_companion_api_endpoints(self):
        client = app.test_client()
        client.get("/api/state")

        # 1. Test recruiting an NPC via API
        with client.session_transaction() as sess:
            sess_id = sess["session_id"]
            eng = GAMES[sess_id]
            eng.npcs["sister_vanya"].relationship = 80

        resp = client.post("/api/action", json={"action": "recruit", "npc_id": "sister_vanya"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        party_ids = [p["id"] for p in data["player"]["party"]]
        self.assertIn("sister_vanya", party_ids)

        # 2. Test talking to companion via API
        resp = client.post("/api/action", json={"action": "talk", "npc_id": "sister_vanya"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["dialogue"]["current_node"], "vanya_companion_hub")

        # 3. Test attempting erotic scene in unsuitable location returns error
        resp = client.post("/api/action", json={"action": "start_erotic_scene", "npc_id": "sister_vanya"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("not suitable", data["error"])

        # 4. Travel to suitable location (Ruined Chantry) via API
        resp = client.post("/api/action", json={"action": "travel", "destination_id": "ruined_chantry"})
        self.assertEqual(resp.status_code, 200)

        # 5. Test starting erotic scene in suitable location via API
        resp = client.post("/api/action", json={"action": "start_erotic_scene", "npc_id": "sister_vanya"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["dialogue"]["current_node"], "vanya_chantry_step1_initiate")

        # 6. Test dismissing companion via API
        resp = client.post("/api/action", json={"action": "dismiss", "npc_id": "sister_vanya"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        party_ids_after = [p["id"] for p in data["player"]["party"]]
        self.assertNotIn("sister_vanya", party_ids_after)


if __name__ == "__main__":
    unittest.main()
