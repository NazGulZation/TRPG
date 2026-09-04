import unittest
from game.engine import GameEngine
from app import app

class TestTRPGEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

    def test_initial_state(self):
        st = self.engine.get_state()
        self.assertEqual(st["player"]["name"], "Wanderer")
        self.assertEqual(st["player"]["gender"], "male")
        self.assertEqual(st["player"]["stats"]["sinew"], 13)
        self.assertEqual(st["player"]["stats"]["guile"], 12)
        self.assertEqual(st["player"]["stats"]["lucidity"], 12)
        self.assertEqual(st["location"]["id"], "gallow_square")
        self.assertTrue(len(st["location"]["npcs"]) > 0)

    def test_travel_and_inspection(self):
        # Inspect gallow square
        res = self.engine.inspect_ground()
        self.assertIn("Tarnished Iron Nail", self.engine.player.inventory)

        # Travel to ruined chantry
        res = self.engine.travel("ruined_chantry")
        self.assertEqual(res["location"]["id"], "ruined_chantry")
        vanya_found = any(n["id"] == "sister_vanya" for n in res["location"]["npcs"])
        self.assertTrue(vanya_found)

    def test_dialogue_stat_check_and_quest_acceptance(self):
        self.engine.travel("ruined_chantry")
        res = self.engine.talk_npc("sister_vanya")
        self.assertIsNotNone(res["dialogue"])
        
        # Select lucidity choice [Lucidity 11], player has 12
        res = self.engine.choose_dialogue("c_vanya_examine")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_lucidity_success")
        
        # Accept quest
        res = self.engine.choose_dialogue("c_vanya_accept_quest")
        self.assertEqual(self.engine.quests["q_mercy_hemlock"].current_stage, 1)

    def test_vanya_nectar_quest_pay_route(self):
        # Accept quest from Sister Vanya
        self.engine.travel("ruined_chantry")
        self.engine.talk_npc("sister_vanya")
        self.engine.choose_dialogue("c_vanya_help")
        self.engine.choose_dialogue("c_vanya_accept_quest_direct")
        self.assertEqual(self.engine.quests["q_mercy_hemlock"].current_stage, 1)

        # Acquire nectar from Commander Malakor with 25 sovereigns
        self.engine.travel("iron_bastion")
        self.engine.talk_npc("commander_malakor")
        self.engine.choose_dialogue("c_malakor_vanya_quest")
        init_sovereigns = self.engine.player.sovereigns
        res = self.engine.choose_dialogue("c_malakor_pay_25")
        self.assertIn("Wolfsbane Nectar", self.engine.player.inventory)
        self.assertEqual(self.engine.player.sovereigns, init_sovereigns - 25)
        self.assertEqual(self.engine.quests["q_mercy_hemlock"].current_stage, 2)

        # Return to Sister Vanya and complete quest
        self.engine.travel("ruined_chantry")
        res = self.engine.talk_npc("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_quest_complete")
        
        self.engine.choose_dialogue("c_vanya_embrace")
        self.assertEqual(self.engine.quests["q_mercy_hemlock"].current_stage, 99)
        self.assertNotIn("Wolfsbane Nectar", self.engine.player.inventory)
        self.assertIn("Silver Dawnshroud Seal", self.engine.player.inventory)

    def test_insufficient_sovereigns_blocked(self):
        self.engine.player.sovereigns = 10
        self.engine.travel("iron_bastion")
        self.engine.talk_npc("commander_malakor")
        self.engine.choose_dialogue("c_malakor_vanya_quest")
        res = self.engine.choose_dialogue("c_malakor_pay_25")
        self.assertIn("error", res)
        self.assertNotIn("Wolfsbane Nectar", self.engine.player.inventory)

    def test_romance_intimacy_and_recruitment(self):
        self.engine.travel("iron_bastion")
        malakor = self.engine.npcs["commander_malakor"]
        
        # Set relationship high to simulate devotion
        malakor.relationship = 75
        self.engine.player.party = []
        
        # Trigger recruit
        res = self.engine.recruit_party("commander_malakor")
        self.assertIn("commander_malakor", self.engine.player.party)
        self.assertTrue(malakor.is_in_party)

        # Test non-combatant rejection for child
        res = self.engine.recruit_party("little_toby")
        self.assertIn("error", res)

    def test_attack_on_sight_hostility(self):
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = -60  # Extreme negative relationship
        
        # Travel into her zone
        res = self.engine.travel("ruined_chantry")
        self.assertIsNotNone(self.engine.combat_state)
        self.assertEqual(self.engine.combat_state["npc_id"], "sister_vanya")

    def test_combat_turn_resolution(self):
        self.engine.start_combat("commander_malakor", ambush=False)
        self.assertIsNotNone(self.engine.combat_state)
        
        # Execute sinew strike
        res = self.engine.combat_action("sinew_strike")
        self.assertTrue(len(self.engine.combat_state["combat_log"]) > 0)

    def test_malakor_brother_quest_route(self):
        self.engine.travel("iron_bastion")
        self.engine.talk_npc("commander_malakor")
        self.engine.choose_dialogue("c_malakor_court")
        self.engine.choose_dialogue("c_malakor_romance_hook")
        self.engine.choose_dialogue("c_malakor_accept_quest")
        self.assertEqual(self.engine.quests["q_blood_brass"].current_stage, 1)

        # Scavenge in Gallow-Square
        self.engine.travel("gallow_square")
        self.engine.inspect_ground()
        self.assertIn("Loras's Iron Signet", self.engine.player.inventory)
        self.assertEqual(self.engine.quests["q_blood_brass"].current_stage, 2)

        # Turn in to Malakor
        self.engine.travel("iron_bastion")
        res = self.engine.talk_npc("commander_malakor")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_quest_complete")
        self.engine.choose_dialogue("c_malakor_recruit")
        self.assertEqual(self.engine.quests["q_blood_brass"].current_stage, 99)
        self.assertNotIn("Loras's Iron Signet", self.engine.player.inventory)
        self.assertIn("Wolfsbane Nectar", self.engine.player.inventory)

    def test_silve_and_toby_quest_and_dialogues(self):
        # 1. Accept from Silve
        self.engine.travel("iron_bastion")
        self.engine.travel("gilded_rat")
        self.engine.talk_npc("madame_silve")
        self.engine.choose_dialogue("c_silve_talk")
        self.engine.choose_dialogue("c_silve_accept_info")
        self.assertEqual(self.engine.quests["q_silk_cyanide"].current_stage, 1)

        # Reminder node check
        res = self.engine.talk_npc("madame_silve")
        self.assertEqual(res["dialogue"]["current_node"], "silve_quest_accepted")

        # 2. Toby comfort route
        self.engine.travel("sluice_trench")
        self.engine.travel("gallow_square")
        self.engine.talk_npc("little_toby")
        self.engine.choose_dialogue("c_toby_comfort")
        self.engine.choose_dialogue("c_toby_take_key")
        self.assertIn("Master Sluice Key", self.engine.player.inventory)
        self.assertIn("Turnkey's Stolen Ledger", self.engine.player.inventory)
        self.assertEqual(self.engine.quests["q_silk_cyanide"].current_stage, 2)

        # Repeat Toby talk
        res = self.engine.talk_npc("little_toby")
        self.assertEqual(res["dialogue"]["current_node"], "toby_saved")

        # 3. Turn in to Silve
        self.engine.travel("sluice_trench")
        self.engine.travel("gilded_rat")
        res = self.engine.talk_npc("madame_silve")
        self.assertEqual(res["dialogue"]["current_node"], "silve_quest_complete")
        self.engine.choose_dialogue("c_silve_intimacy_action")
        self.assertEqual(self.engine.quests["q_silk_cyanide"].current_stage, 99)
        self.assertNotIn("Turnkey's Stolen Ledger", self.engine.player.inventory)
        self.assertIn("Imperial Transit Pass", self.engine.player.inventory)

    def test_escape_endings(self):
        # Sluice escape
        self.engine.player.inventory.append("Master Sluice Key")
        res = self.engine.attempt_escape("sluice_gate")
        self.assertTrue(self.engine.victory)

        # Iron gate escape
        e2 = GameEngine()
        e2.player.inventory.append("Imperial Transit Pass")
        res = e2.attempt_escape("iron_gate")
        self.assertTrue(e2.victory)

    def test_flask_api_routes(self):
        client = app.test_client()
        resp = client.get("/api/state")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["player"]["name"], "Wanderer")

        # Action POST
        act_resp = client.post("/api/action", json={"action": "inspect"})
        self.assertEqual(act_resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()
