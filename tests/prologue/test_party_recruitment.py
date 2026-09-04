import unittest
from game.engine import GameEngine
from game.models import NPC, Stats


class TestPartyRecruitment(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

    def test_romance_intimacy_and_recruitment(self):
        self.engine.travel("iron_bastion")
        malakor = self.engine.npcs["commander_malakor"]
        malakor.relationship = 75
        self.engine.player.party = []

        # Attempt recruit non-recruitable Malakor -> error
        res_malakor = self.engine.recruit_party("commander_malakor")
        self.assertIn("error", res_malakor)
        self.assertIn("cannot be recruited", res_malakor["error"])
        self.assertNotIn("commander_malakor", self.engine.player.party)

        # Attempt recruit non-recruitable Silve -> error
        silve = self.engine.npcs["madame_silve"]
        silve.relationship = 75
        res_silve = self.engine.recruit_party("madame_silve")
        self.assertIn("error", res_silve)
        self.assertIn("cannot be recruited", res_silve["error"])

        # Attempt recruit non-combatant child -> error
        res_toby = self.engine.recruit_party("little_toby")
        self.assertIn("error", res_toby)

        # Sister Vanya CAN be recruited when relationship >= 50
        vanya = self.engine.npcs["sister_vanya"]
        vanya.relationship = 75
        res_vanya = self.engine.recruit_party("sister_vanya")
        self.assertIn("sister_vanya", self.engine.player.party)
        self.assertTrue(vanya.is_in_party)

    def test_default_recruitment_flags(self):
        # Only Sister Vanya can be recruited
        self.assertTrue(self.engine.npcs["sister_vanya"].can_recruit)
        self.assertFalse(self.engine.npcs["commander_malakor"].can_recruit)
        self.assertFalse(self.engine.npcs["madame_silve"].can_recruit)
        self.assertFalse(self.engine.npcs["little_toby"].can_recruit)

    def test_recruitment_restrictions_enforced(self):
        # Malakor has 100 relationship but cannot be recruited
        self.engine.npcs["commander_malakor"].relationship = 100
        res = self.engine.recruit_party("commander_malakor")
        self.assertIn("error", res)
        self.assertIn("cannot be recruited", res["error"])
        self.assertNotIn("commander_malakor", self.engine.player.party)

        # Silve has 100 relationship but cannot be recruited
        self.engine.npcs["madame_silve"].relationship = 100
        res = self.engine.recruit_party("madame_silve")
        self.assertIn("error", res)
        self.assertIn("cannot be recruited", res["error"])
        self.assertNotIn("madame_silve", self.engine.player.party)

    def test_max_party_capacity_four(self):
        self.assertEqual(self.engine.max_party_size, 4)

        # Simulate 4 companions in party
        for i in range(1, 5):
            npc_id = f"test_companion_{i}"
            self.engine.npcs[npc_id] = NPC(
                id=npc_id,
                name=f"Companion {i}",
                title="Mercenary",
                gender="male",
                faction_id="pariahs",
                description="A hired hand.",
                stats=Stats(),
                relationship=60,
                is_combatant=True,
                can_recruit=True
            )
            res = self.engine.recruit_party(npc_id)
            self.assertNotIn("error", res)
            self.assertIn(npc_id, self.engine.player.party)

        self.assertEqual(len(self.engine.player.party), 4)

        # 5th companion recruitment must be blocked
        npc_5 = "test_companion_5"
        self.engine.npcs[npc_5] = NPC(
            id=npc_5,
            name="Companion 5",
            title="Mercenary",
            gender="female",
            faction_id="pariahs",
            description="Another hired hand.",
            stats=Stats(),
            relationship=60,
            is_combatant=True,
            can_recruit=True
        )
        res5 = self.engine.recruit_party(npc_5)
        self.assertIn("error", res5)
        self.assertIn("Party is full", res5["error"])
        self.assertEqual(len(self.engine.player.party), 4)


if __name__ == "__main__":
    unittest.main()
