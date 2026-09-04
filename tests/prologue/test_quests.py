import unittest
from game.engine import GameEngine


class TestQuests(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

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
        self.engine.choose_dialogue("c_malakor_embrace")
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

    def test_toby_mentorship_and_safehouse(self):
        self.engine.travel("gallow_square")
        self.engine.talk_npc("little_toby")
        # Teach Toby stealth
        res = self.engine.choose_dialogue("c_toby_teach")
        self.assertEqual(res["dialogue"]["current_node"], "toby_taught")

        # Toby comfort and safehouse dispatch
        self.engine.player.inventory.append("Charred Rations")
        res = self.engine.choose_dialogue("c_toby_back_after_taught")
        self.engine.choose_dialogue("c_toby_comfort")
        res = self.engine.choose_dialogue("c_toby_send_safehouse")
        self.assertEqual(res["dialogue"]["current_node"], "toby_safehouse")
        self.assertIn("Master Sluice Key", self.engine.player.inventory)
        self.assertIn("Turnkey's Stolen Ledger", self.engine.player.inventory)

    def test_patient_triage_ward(self):
        self.engine.travel("ruined_chantry")
        self.engine.talk_npc("sister_vanya")
        res = self.engine.choose_dialogue("c_vanya_triage")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_triage_ward")

        # Triage soldier with Sinew 12
        res = self.engine.choose_dialogue("c_vanya_triage_soldier")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_triage_soldier_success")


if __name__ == "__main__":
    unittest.main()
