import unittest
from game.engine import GameEngine


class TestCompanionsAndIntimacy(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

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

        # Step 4: Caress & Lubrication (Oral branch)
        res = self.engine.choose_dialogue("c_silve_gilded_oral_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step4_caress")

        # Step 5: Penetration on velvet divan
        res = self.engine.choose_dialogue("c_silve_oral_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step5_entry")

        # Step 6: Sinuous Cadence
        res = self.engine.choose_dialogue("c_silve_oral_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step6_rhythm")

        # Step 7: Positional Shift
        res = self.engine.choose_dialogue("c_silve_oral_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step7_shift")

        # Step 8: Fierce Cadence & Sensual Frenzy
        res = self.engine.choose_dialogue("c_silve_oral_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step8_frenzy")

        # Step 9: The Precipice / Pre-Climax
        res = self.engine.choose_dialogue("c_silve_oral_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step9_precipice")

        # Step 10: Explosive Climax in the Boudoir
        res = self.engine.choose_dialogue("c_silve_oral_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_oral_step10_climax")

        # Verify rewards: Dread = 0, is_romanced = True
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(self.engine.npcs["madame_silve"].is_romanced)

        # Afterglow and farewell (non-recruitable ally)
        res = self.engine.choose_dialogue("c_silve_oral_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_afterglow")
        self.assertIn("Silve's Scented Silk Favor", self.engine.player.inventory)

        res = self.engine.choose_dialogue("c_silve_afterglow_farewell")
        self.assertEqual(res["dialogue"]["current_node"], "silve_farewell")
        self.assertNotIn("madame_silve", self.engine.player.party)
        self.assertFalse(self.engine.npcs["madame_silve"].is_in_party)

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

        # Step 4 to Step 10 (Tender branch)
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step4_caress")
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step5_entry")
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step6_rhythm")
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step7_shift")
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step8_frenzy")
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step9_precipice")
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_tender_step10_climax")
        self.assertEqual(self.engine.player.dread, 0)
        self.assertTrue(vanya.is_romanced)

        # Afterglow returns to companion hub
        res = self.engine.choose_dialogue("c_vanya_chantry_tender_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_afterglow")
        res = self.engine.choose_dialogue("c_vanya_companion_return_hub")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")

        # Also test initiating intimacy via dialogue choice in companion hub
        res = self.engine.choose_dialogue("c_vanya_companion_intimacy")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step1_initiate")

    def test_malakor_companion_talk_and_non_romance(self):
        # Allow recruit for companion test
        malakor = self.engine.npcs["commander_malakor"]
        malakor.relationship = 80
        malakor.can_recruit = True
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
        # Allow recruit for companion erotic test
        silve = self.engine.npcs["madame_silve"]
        silve.relationship = 80
        silve.can_recruit = True
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
        self.assertGreater(self.engine.npcs["commander_malakor"].relationship, 10)

        # Test blood-oath turn-in giving Drake Whetstone
        self.engine.player.inventory.append("Loras's Iron Signet")
        res = self.engine.talk_npc("commander_malakor")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_quest_complete")
        res = self.engine.choose_dialogue("c_malakor_embrace")
        self.assertEqual(res["dialogue"]["current_node"], "malakor_intimacy_scene")
        res = self.engine.choose_dialogue("c_malakor_post_intimacy_recruit")
        self.assertIn("Malakor's Drake Whetstone", self.engine.player.inventory)

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

    def test_silve_intimacy_restricted_to_gilded_rat(self):
        # Madame Silve is non-recruitable and her intimacy is strictly restricted to Gilded Rat
        silve = self.engine.npcs["madame_silve"]
        silve.relationship = 80

        # At Ruined Chantry, cannot initiate intimacy with Silve even if in party
        self.engine.player.party = ["madame_silve"]
        silve.is_in_party = True
        self.engine.player.current_location_id = "ruined_chantry"
        self.assertFalse(self.engine.can_initiate_companion_erotic("madame_silve"))
        res_blocked = self.engine.start_party_erotic_scene("madame_silve")
        self.assertIn("error", res_blocked)

        # At Gilded Rat, intimacy is available
        self.engine.player.current_location_id = "gilded_rat"
        self.assertTrue(self.engine.can_initiate_companion_erotic("madame_silve"))

    def test_erotic_scenes_step1_leave_options(self):
        # 1. Vanya Chantry Step 1 Leave Option (from quest turn-in / intimacy scene)
        self.engine.travel("ruined_chantry")
        self.engine.player.inventory.append("Wolfsbane Nectar")
        self.engine.talk_npc("sister_vanya")
        self.engine.choose_dialogue("c_vanya_embrace")
        # Step 1: choose to decline/leave
        res = self.engine.choose_dialogue("c_vanya_quest_intimacy_leave")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_quest_complete")
        self.assertFalse(self.engine.npcs["sister_vanya"].is_romanced)

        # 2. Vanya Chantry Step 1 Leave Option (from companion initiation)
        self.engine.npcs["sister_vanya"].relationship = 80
        self.engine.recruit_party("sister_vanya")
        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step1_initiate")
        res = self.engine.choose_dialogue("c_vanya_chantry_step1_leave")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")

        # 3. Vanya Gilded Rat Step 1 Leave Option
        self.engine.travel("iron_bastion")
        self.engine.travel("gilded_rat")
        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_gilded_step1_initiate")
        res = self.engine.choose_dialogue("c_vanya_gilded_step1_leave")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")

        # 4. Silve Gilded Rat Step 1 Leave Option (from quest turn-in)
        self.engine.player.inventory.append("Turnkey's Stolen Ledger")
        self.engine.talk_npc("madame_silve")
        self.engine.choose_dialogue("c_silve_intimacy_action")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_companion_hub")
        res = self.engine.choose_dialogue("c_silve_quest_intimacy_leave")
        self.assertEqual(res["dialogue"]["current_node"], "silve_quest_complete")
        self.assertFalse(self.engine.npcs["madame_silve"].is_romanced)

    def test_all_unique_erotic_branches(self):
        # Test Vanya Chantry Dominant branch
        self.engine.player.current_location_id = "ruined_chantry"
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 80
        self.engine.player.party = ["sister_vanya"]
        vanya.is_in_party = True
        vanya.is_romanced = False

        res = self.engine.start_party_erotic_scene("sister_vanya")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step1_initiate")
        res = self.engine.choose_dialogue("c_vanya_chantry_step1_choice")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step2_foreplay")
        res = self.engine.choose_dialogue("c_vanya_chantry_branch_dominant")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_step3_dominant")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step4_caress")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step5_entry")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step6_rhythm")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step7_shift")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step8_frenzy")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step9_precipice")
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_dominant_step10_climax")
        self.assertTrue(vanya.is_romanced)
        res = self.engine.choose_dialogue("c_vanya_chantry_dom_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "vanya_chantry_afterglow")

        # Test Silve Gilded Wine branch
        self.engine.player.current_location_id = "gilded_rat"
        silve = self.engine.npcs["madame_silve"]
        silve.relationship = 80
        silve.is_romanced = False
        silve.can_recruit = True
        self.engine.player.party = ["madame_silve"]
        silve.is_in_party = True

        res = self.engine.start_party_erotic_scene("madame_silve")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step1_initiate")
        res = self.engine.choose_dialogue("c_silve_gilded_step1_choice")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step2_foreplay")
        res = self.engine.choose_dialogue("c_silve_gilded_branch_wine")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_step3_wine")
        res = self.engine.choose_dialogue("c_silve_gilded_wine_to_step4")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step4_caress")
        res = self.engine.choose_dialogue("c_silve_wine_to_step5")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step5_entry")
        res = self.engine.choose_dialogue("c_silve_wine_to_step6")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step6_rhythm")
        res = self.engine.choose_dialogue("c_silve_wine_to_step7")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step7_shift")
        res = self.engine.choose_dialogue("c_silve_wine_to_step8")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step8_frenzy")
        res = self.engine.choose_dialogue("c_silve_wine_to_step9")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step9_precipice")
        res = self.engine.choose_dialogue("c_silve_wine_to_step10")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_wine_step10_climax")
        self.assertTrue(silve.is_romanced)
        res = self.engine.choose_dialogue("c_silve_wine_to_afterglow")
        self.assertEqual(res["dialogue"]["current_node"], "silve_gilded_afterglow")

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
