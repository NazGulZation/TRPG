import unittest
from game.engine import GameEngine


class TestEngineCore(unittest.TestCase):
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

    def test_insufficient_sovereigns_blocked(self):
        self.engine.player.sovereigns = 10
        self.engine.travel("iron_bastion")
        self.engine.talk_npc("commander_malakor")
        self.engine.choose_dialogue("c_malakor_vanya_quest")
        res = self.engine.choose_dialogue("c_malakor_pay_25")
        self.assertIn("error", res)
        self.assertNotIn("Wolfsbane Nectar", self.engine.player.inventory)

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

    def test_functional_item_effects_and_usability(self):
        # Test Sister Vanya's Rosary: +2 Lucidity in stat checks and halving Dread increases
        self.engine.player.inventory.append("Sister Vanya's Embroidered Rosary")
        base_luc = self.engine.player.stats.lucidity
        eff_luc = self.engine.get_effective_stat("lucidity")
        self.assertEqual(eff_luc, base_luc + 2)

        # Test Malakor's Drake Whetstone: +2 Sinew and +4 combat damage
        self.engine.player.inventory.append("Malakor's Drake Whetstone")
        eff_sinew = self.engine.get_effective_stat("sinew")
        self.assertEqual(eff_sinew, self.engine.player.stats.sinew + 2)

        # Test Silve's Silk Favor: +2 Guile and 25% discount
        self.engine.player.inventory.append("Silve's Scented Silk Favor")
        eff_guile = self.engine.get_effective_stat("guile")
        self.assertEqual(eff_guile, self.engine.player.stats.guile + 2)
        disc_cost = self.engine.apply_sovereign_discount(100)
        self.assertEqual(disc_cost, 75)

        # Test item usage: Spiced Plum Wine restores 12 HP & removes 15 Dread
        self.engine.player.inventory.append("Spiced Plum Wine")
        self.engine.player.current_hp = 20
        self.engine.player.dread = 40
        res = self.engine.use_item("Spiced Plum Wine")
        self.assertEqual(self.engine.player.current_hp, 32)
        self.assertEqual(self.engine.player.dread, 25)
        self.assertNotIn("Spiced Plum Wine", self.engine.player.inventory)

        # Test Crowbar usage in Sluice Trench
        self.engine.player.inventory.append("Corroded Crowbar")
        self.engine.player.current_location_id = "sluice_trench"
        init_rep = self.engine.player.faction_reputation["pariahs"]
        res = self.engine.use_item("Corroded Crowbar")
        self.assertEqual(self.engine.player.faction_reputation["pariahs"], init_rep + 10)

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


if __name__ == "__main__":
    unittest.main()
