import unittest
from game.data.prologue import (
    get_prologue_metadata,
    SUITABLE_INTIMACY_LOCATIONS,
    get_prologue_locations,
    get_prologue_factions,
    get_prologue_quests,
    get_prologue_npcs,
    get_prologue_items,
)


class TestDataIntegrity(unittest.TestCase):
    def test_metadata_configuration(self):
        meta = get_prologue_metadata()
        self.assertEqual(meta["chapter_id"], "prologue")
        self.assertIn("opening_log", meta)
        self.assertIn("suitable_intimacy_locations", meta)
        self.assertEqual(meta["suitable_intimacy_locations"], SUITABLE_INTIMACY_LOCATIONS)
        self.assertIn("sister_vanya", SUITABLE_INTIMACY_LOCATIONS)
        self.assertIn("madame_silve", SUITABLE_INTIMACY_LOCATIONS)

    def test_locations_configuration(self):
        locs = get_prologue_locations()
        self.assertEqual(len(locs), 5)
        for loc_id in ["gallow_square", "ruined_chantry", "iron_bastion", "gilded_rat", "sluice_trench"]:
            self.assertIn(loc_id, locs)
            loc = locs[loc_id]
            self.assertTrue(len(loc.name) > 0)
            self.assertTrue(len(loc.description) > 0)
            for conn in loc.connected_locations:
                self.assertIn(conn, locs, f"Location {loc_id} connects to non-existent location {conn}")

    def test_factions_configuration(self):
        factions = get_prologue_factions()
        self.assertIn("dawnshroud", factions)
        self.assertIn("iron_drakes", factions)
        self.assertIn("pariahs", factions)
        for f_id, f_data in factions.items():
            self.assertIn("name", f_data)
            self.assertIn("desc", f_data)
            self.assertIn("color", f_data)

    def test_quests_configuration(self):
        quests = get_prologue_quests()
        self.assertEqual(len(quests), 3)
        for q_id in ["q_mercy_hemlock", "q_blood_brass", "q_silk_cyanide"]:
            self.assertIn(q_id, quests)
            q = quests[q_id]
            self.assertTrue(len(q.title) > 0)
            self.assertTrue(len(q.stages) > 0)

    def test_npcs_and_dialogue_integrity(self):
        npcs = get_prologue_npcs()
        self.assertEqual(len(npcs), 4)
        for npc_id in ["sister_vanya", "commander_malakor", "madame_silve", "little_toby"]:
            self.assertIn(npc_id, npcs)
            npc = npcs[npc_id]
            self.assertTrue(len(npc.name) > 0)
            self.assertIn(npc.dialogue_root, npc.dialogue_nodes, f"{npc_id} missing dialogue_root {npc.dialogue_root}")

            # Check every dialogue node and its choices
            for node_id, node in npc.dialogue_nodes.items():
                self.assertEqual(node.id, node_id)
                self.assertTrue(len(node.text) > 0)
                for choice in node.choices:
                    self.assertIn(
                        choice.next_node,
                        npc.dialogue_nodes,
                        f"NPC {npc_id} node {node_id} choice {choice.id} targets non-existent next_node {choice.next_node}"
                    )
                    if choice.failure_node:
                        self.assertIn(
                            choice.failure_node,
                            npc.dialogue_nodes,
                            f"NPC {npc_id} node {node_id} choice {choice.id} targets non-existent failure_node {choice.failure_node}"
                        )

    def test_items_configuration(self):
        items = get_prologue_items()
        self.assertGreater(len(items), 0)
        core_quest_items = [
            "wolfsbane_nectar",
            "loras_signet",
            "turnkey_ledger",
            "master_sluice_key",
            "silver_seal",
            "transit_pass",
        ]
        for itm_id in core_quest_items:
            self.assertIn(itm_id, items, f"Missing core item {itm_id} in items.json")
            itm = items[itm_id]
            self.assertEqual(itm.id, itm_id)
            self.assertTrue(len(itm.name) > 0)
            self.assertTrue(len(itm.description) > 0)
            self.assertEqual(itm.item_type, "quest")


if __name__ == "__main__":
    unittest.main()
