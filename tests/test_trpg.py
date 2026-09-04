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

    def test_vanya_lengthy_multi_stage_erotic_scene(self):
        # Progress Sister Vanya's narrative erotic scene (Default: Ruined Chantry)
        self.engine.travel("ruined_chantry")
        self.engine.player.inventory.append("Wolfsbane Nectar")
        self.engine.talk_npc("sister_vanya")
        
        # Turn-in and initiate intimate encounter (Step 1)
        res = self.engine.choose_dialogue("c_vanya_embrace")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_intimacy_scene")
        
        # Step 2: Unveil habit & foreplay choices
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step2")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step2_foreplay")
        
        # Step 3: Branch choice - Devoted oral worship
        res = self.engine.choose_dialogue("c_vanya_chantry_branch_oral")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step3_oral")
        
        # Step 4: Intimate Caresses & Lubrication
        res = self.engine.choose_dialogue("c_vanya_chantry_oral_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step4_caress")
        
        # Step 5: Penetration & Alignment
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step5_entry")
        
        # Step 6: Initial Cadence & Deep Friction
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step6_rhythm")
        
        # Step 7: Positional Shift & Escalation
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step7_shift")
        
        # Step 8: Fierce Cadence & Vocal Surrender
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step8_frenzy")
        
        # Step 9: The Precipice / Edging
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step9_precipice")
        
        # Step 10: Explosive Climax
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step10_climax")
        
        # Verify rewards: Dread purged to 0, romanced marked
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(self.engine.npcs["sister_vanya"].is_romanced)
        
        # Afterglow & Recruitment
        res = self.engine.choose_dialogue("c_vanya_chantry_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_afterglow")
        self.assertIn("Sister Vanya's Embroidered Rosary", self.engine.player.inventory)
        
        res = self.engine.choose_dialogue("c_vanya_post_intimacy_recruit")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_recruited")
        self.assertIn("sister_vanya", self.engine.player.party)
        self.assertTrue(self.engine.npcs["sister_vanya"].is_in_party)

    def test_silve_lengthy_multi_stage_erotic_scene(self):
        # Progress Madame Silve's narrative erotic scene (Default: Gilded Rat)
        self.engine.travel("iron_bastion")
        self.engine.travel("gilded_rat")
        self.engine.player.inventory.append("Turnkey's Stolen Ledger")
        self.engine.talk_npc("madame_silve")
        
        # Step 1: Turn-in and start boudoir encounter
        res = self.engine.choose_dialogue("c_silve_intimacy_action")
        self.assertEqual(res["dialogue"]["current_node"], "silve_intimacy_scene")
        
        # Step 2: Unveil and foreplay choices
        res = self.engine.choose_dialogue("c_silve_gilded_to_step2")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step2_foreplay")
        
        # Step 3: Branch choice - Devoted oral ecstasy
        res = self.engine.choose_dialogue("c_silve_gilded_branch_oral")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step3_oral")
        
        # Step 4: Caress & Lubrication
        res = self.engine.choose_dialogue("c_silve_gilded_oral_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step4_caress")
        
        # Step 5: Penetration on velvet divan
        res = self.engine.choose_dialogue("c_silve_gilded_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step5_entry")
        
        # Step 6: Sinuous Cadence
        res = self.engine.choose_dialogue("c_silve_gilded_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step6_rhythm")
        
        # Step 7: Positional Shift
        res = self.engine.choose_dialogue("c_silve_gilded_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step7_shift")
        
        # Step 8: Fierce Cadence & Sensual Frenzy
        res = self.engine.choose_dialogue("c_silve_gilded_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step8_frenzy")
        
        # Step 9: The Precipice / Pre-Climax
        res = self.engine.choose_dialogue("c_silve_gilded_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step9_precipice")
        
        # Step 10: Explosive Climax in the Boudoir
        res = self.engine.choose_dialogue("c_silve_gilded_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step10_climax")
        
        # Verify rewards: Dread = 0, is_romanced = True
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(self.engine.npcs["madame_silve"].is_romanced)
        
        # Afterglow and recruitment into warband
        res = self.engine.choose_dialogue("c_silve_gilded_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_afterglow")
        self.assertIn("Silve's Scented Silk Favor", self.engine.player.inventory)
        
        res = self.engine.choose_dialogue("c_silve_recruit_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "silve_recruited")
        self.assertIn("madame_silve", self.engine.player.party)
        self.assertTrue(self.engine.npcs["madame_silve"].is_in_party)

    def test_party_companion_talk_and_interactions(self):
        # Recruit Sister Vanya
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 75
        self.engine.recruit_party("sister_vanya")
        self.assertTrue(vanya.is_in_party)
        
        # Talking to in-party Vanya routes to companion hub
        res = self.engine.talk_npc("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")
        
        # Converse with companion
        res = self.engine.choose_dialogue("c_vanya_companion_talk")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_talk")
        
        # Test companion triage healing
        self.engine.player.current_hp = 20
        self.engine.player.dread = 30
        self.engine.talk_npc("sister_vanya")
        res = self.engine.choose_dialogue("c_vanya_companion_tend")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_tend")
        self.assertEqual(self.engine.player.current_hp, 35)
        self.assertEqual(self.engine.player.dread, 20)

    def test_party_companion_erotic_scene_direct_and_dialogue(self):
        # Recruit Sister Vanya
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 80
        self.engine.recruit_party("sister_vanya")
        
        # Intimacy blocked in unsuitable starting location (Gallow-Square)
        self.assertFalse(self.engine.can_initiate_companion_erotic("sister_vanya"))
        res_blocked = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertIn("error", res_blocked)
        self.assertIn("not suitable", res_blocked["error"])
        
        # Travel to suitable location: Ruined Chantry (Default scene for Vanya)
        self.engine.travel("ruined_chantry")
        self.assertTrue(self.engine.can_initiate_companion_erotic("sister_vanya"))
        
        # Trigger companion erotic scene directly (Step 1)
        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step1_initiate")
        
        # Step 2: Foreplay
        res = self.engine.choose_dialogue("c_vanya_chantry_step1_choice")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step2_foreplay")
        
        # Step 3: Branch choice - Tender
        res = self.engine.choose_dialogue("c_vanya_chantry_branch_tender")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step3_tender")
        
        # Step 4 to Step 10
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step4_caress")
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step5_entry")
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step6_rhythm")
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step7_shift")
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step8_frenzy")
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step9_precipice")
        res = self.engine.choose_dialogue("c_vanya_chantry_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step10_climax")
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(vanya.is_romanced)
        
        # Afterglow returns to companion hub
        res = self.engine.choose_dialogue("c_vanya_chantry_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_afterglow")
        res = self.engine.choose_dialogue("c_vanya_companion_return_hub")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")
        
        # Also test initiating intimacy via dialogue choice in companion hub
        res = self.engine.choose_dialogue("c_vanya_companion_intimacy")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step1_initiate")

    def test_malakor_companion_talk_and_non_romance(self):
        # Recruit Commander Malakor
        malakor = self.engine.npcs["commander_malakor"]
        malakor.relationship = 80
        self.engine.recruit_party("commander_malakor")
        
        # Talking to Malakor in party opens companion hub
        res = self.engine.talk_npc("commander_malakor")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_companion_hub")
        
        # Share drink
        self.engine.player.dread = 25
        res = self.engine.choose_dialogue("c_malakor_companion_drink")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_companion_drink")
        self.assertEqual(self.engine.player.dread, 20)
        
        # Attempting erotic scene with male warrior comrade returns error
        res = self.engine.start_party_erotic_scene("commander_malakor")
        self.assertIn("error", res)
        self.assertIn("cannot be courted intimately", res["error"])

    def test_silve_recruitment_and_companion_erotic_scene(self):
        # Recruit Madame Silve
        silve = self.engine.npcs["madame_silve"]
        silve.relationship = 80
        self.engine.recruit_party("madame_silve")
        
        # Blocked in Gallow-Square
        self.assertFalse(self.engine.can_initiate_companion_erotic("madame_silve"))
        res_blocked = self.engine.start_party_erotic_scene("madame_silve")
        self.assertIn("error", res_blocked)
        
        # Travel to suitable location: Gilded Rat (Default scene for Silve)
        self.engine.travel("iron_bastion")
        self.engine.travel("gilded_rat")
        self.assertTrue(self.engine.can_initiate_companion_erotic("madame_silve"))
        
        # Talk to Silve in party
        res = self.engine.talk_npc("madame_silve")
        self.assertEqual(res["dialogue"]["current_node"], "silve_companion_hub")
        
        # Trigger companion erotic scene directly (Step 1)
        res = self.engine.start_party_erotic_scene("madame_silve")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step1_initiate")
        
        # Step 2: Foreplay
        res = self.engine.choose_dialogue("c_silve_gilded_step1_choice")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step2_foreplay")
        
        # Step 3: Branch choice - Sensual
        res = self.engine.choose_dialogue("c_silve_gilded_branch_sensual")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step3_sensual")
        
        # Steps 4 to 10
        res = self.engine.choose_dialogue("c_silve_gilded_sensual_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step4_caress")
        res = self.engine.choose_dialogue("c_silve_gilded_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step5_entry")
        res = self.engine.choose_dialogue("c_silve_gilded_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step6_rhythm")
        res = self.engine.choose_dialogue("c_silve_gilded_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step7_shift")
        res = self.engine.choose_dialogue("c_silve_gilded_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step8_frenzy")
        res = self.engine.choose_dialogue("c_silve_gilded_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step9_precipice")
        res = self.engine.choose_dialogue("c_silve_gilded_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step10_climax")
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(silve.is_romanced)
        
        # Afterglow returns to hub
        res = self.engine.choose_dialogue("c_silve_gilded_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_afterglow")
        res = self.engine.choose_dialogue("c_silve_companion_return_hub")
        self.assertEqual(res["dialogue"]["current_node"], "silve_companion_hub")

    def test_malakor_warrior_brotherhood_blood_oath(self):
        # Malakor is male and strictly non-romanceable
        self.assertFalse(self.engine.npcs["commander_malakor"].can_romance)
        
        # Test sparring challenge
        self.engine.travel("iron_bastion")
        self.engine.talk_npc("commander_malakor")
        res = self.engine.choose_dialogue("c_malakor_spar")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_spar_challenge")
        
        # Win spar via Sinew 14
        res = self.engine.choose_dialogue("c_malakor_spar_sinew")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_spar_win")
        self.assertIn("Heavy Whetstone", self.engine.player.inventory)

        # Test blood-oath turn-in giving Drake Whetstone
        self.engine.player.inventory.append("Loras's Iron Signet")
        res = self.engine.talk_npc("commander_malakor")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_quest_complete")
        res = self.engine.choose_dialogue("c_malakor_embrace")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_intimacy_scene")
        res = self.engine.choose_dialogue("c_malakor_post_intimacy_recruit")
        self.assertIn("Malakor's Drake Whetstone", self.engine.player.inventory)

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

    def test_flask_companion_api_endpoints(self):
        client = app.test_client()
        client.get("/api/state")
        
        # 1. Test recruiting an NPC via API
        with client.session_transaction() as sess:
            from app import GAMES
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

    def test_companion_erotic_scene_location_suitability(self):
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 80
        self.engine.recruit_party("sister_vanya")
        
        # Unsuitable locations: gallow_square, iron_bastion, sluice_trench
        for loc in ["gallow_square", "iron_bastion", "sluice_trench"]:
            self.engine.player.current_location_id = loc
            self.assertFalse(self.engine.can_initiate_companion_erotic("sister_vanya"))
            res = self.engine.start_party_erotic_scene("sister_vanya")
            self.assertIn("error", res)
            self.assertIn("not suitable", res["error"])
            
        # Suitable location 1: ruined_chantry -> Chantry default scene
        self.engine.player.current_location_id = "ruined_chantry"
        self.assertTrue(self.engine.can_initiate_companion_erotic("sister_vanya"))
        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step1_initiate")
        
        # Suitable location 2: gilded_rat -> Gilded Rat unique scene
        self.engine.player.current_location_id = "gilded_rat"
        self.assertTrue(self.engine.can_initiate_companion_erotic("sister_vanya"))
        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step1_initiate")

    def test_companion_hub_intimacy_choice_hidden_in_unsuitable_locations(self):
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 80
        self.engine.recruit_party("sister_vanya")
        
        # In Gallow-Square (unsuitable)
        self.engine.player.current_location_id = "gallow_square"
        res = self.engine.talk_npc("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")
        intimacy_choices = [c for c in res["dialogue"]["choices"] if c.get("is_intimacy")]
        self.assertEqual(len(intimacy_choices), 0)
        
        # In Ruined Chantry (suitable)
        self.engine.player.current_location_id = "ruined_chantry"
        res = self.engine.talk_npc("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")
        intimacy_choices = [c for c in res["dialogue"]["choices"] if c.get("is_intimacy")]
        self.assertEqual(len(intimacy_choices), 1)
        self.assertEqual(intimacy_choices[0]["id"], "c_vanya_companion_intimacy")

    def test_silve_unique_chantry_erotic_scene(self):
        # Recruit Madame Silve and travel to Ruined Chantry (sacrilegious unique scene)
        silve = self.engine.npcs["madame_silve"]
        silve.relationship = 80
        self.engine.recruit_party("madame_silve")
        self.engine.travel("ruined_chantry")
        self.assertTrue(self.engine.can_initiate_companion_erotic("madame_silve"))
        
        # Step 1: Initiating in the Desecrated Sanctuary
        res = self.engine.start_party_erotic_scene("madame_silve")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step1_initiate")
        
        # Step 2: Foreplay
        res = self.engine.choose_dialogue("c_silve_chantry_to_step2")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step2_foreplay")
        
        # Step 3: Branch choice - Sacrilegious oral devotion
        res = self.engine.choose_dialogue("c_silve_chantry_branch_oral")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step3_oral")
        
        # Step 4: Intimate Caresses & Sacred Lubrication
        res = self.engine.choose_dialogue("c_silve_chantry_oral_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step4_caress")
        
        # Step 5: Penetration in the Moonlit Sanctuary
        res = self.engine.choose_dialogue("c_silve_chantry_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step5_entry")
        
        # Step 6: Resonant Cadence in the Nave
        res = self.engine.choose_dialogue("c_silve_chantry_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step6_rhythm")
        
        # Step 7: Positional Shift on Altar Slab
        res = self.engine.choose_dialogue("c_silve_chantry_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step7_shift")
        
        # Step 8: Sacred Frenzy & Vocal Surrender
        res = self.engine.choose_dialogue("c_silve_chantry_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step8_frenzy")
        
        # Step 9: The Edge of Absolution
        res = self.engine.choose_dialogue("c_silve_chantry_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step9_precipice")
        
        # Step 10: Climax at the Altar
        res = self.engine.choose_dialogue("c_silve_chantry_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_step10_climax")
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(silve.is_romanced)
        
        # Afterglow returns to companion hub
        res = self.engine.choose_dialogue("c_silve_chantry_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "silve_chantry_afterglow")
        res = self.engine.choose_dialogue("c_silve_chantry_return_hub")
        self.assertEqual(res["dialogue"]["current_node"], "silve_companion_hub")

    def test_vanya_unique_gilded_rat_erotic_scene(self):
        # Recruit Sister Vanya and travel to Gilded Rat (hedonistic unique scene)
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 80
        self.engine.recruit_party("sister_vanya")
        self.engine.travel("iron_bastion")
        self.engine.travel("gilded_rat")
        self.assertTrue(self.engine.can_initiate_companion_erotic("sister_vanya"))
        
        # Step 1: Initiating in the Pleasure Den
        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step1_initiate")
        
        # Step 2: Foreplay
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step2")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step2_foreplay")
        
        # Step 3: Branch choice - Spiced Plum Wine
        res = self.engine.choose_dialogue("c_vanya_gilded_branch_wine")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step3_wine")
        
        # Step 4: Intimate Caresses & Lubrication
        res = self.engine.choose_dialogue("c_vanya_gilded_wine_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step4_caress")
        
        # Step 5: Penetration on the Velvet Divan
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step5_entry")
        
        # Step 6: Sinuous Cadence on Crimson Silks
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step6_rhythm")
        
        # Step 7: Positional Shift & Intensifying Depth
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step7_shift")
        
        # Step 8: Fierce Cadence & Sensual Frenzy
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step8_frenzy")
        
        # Step 9: The Precipice / Pre-Climax
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step9_precipice")
        
        # Step 10: Explosive Climax in the Boudoir
        res = self.engine.choose_dialogue("c_vanya_gilded_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step10_climax")
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(vanya.is_romanced)
        
        # Afterglow returns to companion hub
        res = self.engine.choose_dialogue("c_vanya_gilded_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_afterglow")
        res = self.engine.choose_dialogue("c_vanya_gilded_return_hub")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")

if __name__ == "__main__":
    unittest.main()
